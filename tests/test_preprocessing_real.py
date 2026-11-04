import os
import sys

import nltk
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from preprocessing import SMSParser


@pytest.fixture(scope="module", autouse=True)
def setup_nltk_resources():
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)


@pytest.fixture
def parser():
    return SMSParser()


def test_empty_message(parser):
    assert parser.parse("") == ""


def test_non_string_message(parser):
    assert parser.parse(None) == ""


def test_html_is_removed(parser):
    assert parser.strip_tags("<b>FREE</b>") == "FREE"


def test_url_is_removed(parser):
    result = parser.parse("Visit http://example.com now")
    assert "http" not in result


def test_punctuation_is_removed(parser):
    result = parser.parse("Hello, world!")
    assert "," not in result
    assert "!" not in result


@pytest.mark.parametrize("input_text", ["SPAM", "Hello World", "FREE PRIZE"])
def test_parse_returns_string(parser, input_text):
    assert isinstance(parser.parse(input_text), str)
