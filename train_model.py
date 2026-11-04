import json
import pickle
import sys
from pathlib import Path

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from preprocessing import SMSParser


PROJECT_DIR = Path(__file__).resolve().parent
DATASET_PATH = PROJECT_DIR / "smspamcoll" / "SMSSpamCollection"


def load_dataset(path=DATASET_PATH):
    messages = []
    labels = []

    with path.open("r", encoding="latin-1") as file:
        for line in file:
            parts = line.rstrip("\n").split("\t", 1)
            if len(parts) == 2:
                labels.append(parts[0].strip())
                messages.append(parts[1].strip())

    return messages, labels


def main():
    for resource in ("stopwords", "punkt", "punkt_tab"):
        nltk.download(resource, quiet=True)

    messages, labels = load_dataset()
    parser = SMSParser()
    processed_messages = [parser.parse(message) for message in messages]

    train_messages, test_messages, train_labels, test_labels = train_test_split(
        processed_messages,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    vectorizer = TfidfVectorizer()
    train_vectors = vectorizer.fit_transform(train_messages)
    test_vectors = vectorizer.transform(test_messages)

    model = SVC(kernel="linear", class_weight="balanced")
    model.fit(train_vectors, train_labels)
    predictions = model.predict(test_vectors)

    metrics = {
        "accuracy": accuracy_score(test_labels, predictions),
        "confusion_matrix": confusion_matrix(test_labels, predictions, labels=["ham", "spam"]).tolist(),
        "classification_report": classification_report(test_labels, predictions, output_dict=True),
        "train_messages": len(train_messages),
        "test_messages": len(test_messages),
        "vocabulary_size": len(vectorizer.get_feature_names_out()),
        "random_state": 42,
    }

    with (PROJECT_DIR / "tfidf_vectorizer.pkl").open("wb") as file:
        pickle.dump(vectorizer, file)
    with (PROJECT_DIR / "svm_model.pkl").open("wb") as file:
        pickle.dump(model, file)
    with (PROJECT_DIR / "training_metrics.json").open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    sys.exit(main())
