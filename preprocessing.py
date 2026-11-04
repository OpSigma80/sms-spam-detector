import re
import string
from html.parser import HTMLParser

from nltk import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


ENGLISH_STOPWORDS = frozenset(stopwords.words("english"))
STEMMER = PorterStemmer()


class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


class SMSParser:
    def strip_tags(self, text):
        stripper = HTMLStripper()
        stripper.feed(text)
        stripped = ''.join(stripper.parts)
        return stripped or text

    def remove_urls(self, text):
        return re.sub(r"https?://\S+|www\.\S+", " ", text)

    def clean_text(self, tokens):
        punct = set(string.punctuation) | {"\n", "\t"}

        return [
            STEMMER.stem(token.lower())
            for token in tokens
            if token.lower() not in ENGLISH_STOPWORDS
            and token.lower() not in punct
            and token.isalpha()
        ]

    def parse(self, text):
        if not isinstance(text, str):
            return ""
        text = self.strip_tags(text)
        text = self.remove_urls(text)
        return " ".join(self.clean_text(word_tokenize(text)))
