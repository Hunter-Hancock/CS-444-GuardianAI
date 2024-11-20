import pandas as pd
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.model_selection import train_test_split
import tensorflow as tf

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

model = TFBertForSequenceClassification.from_pretrained(
    "bert-base-uncased", num_labels=6
)


def tokenize(text, labels, tokenizer):
    encodings = tokenizer(
        text["comment_text"].tolist(),
        truncation=True,
        padding=True,
        max_length=128,
        return_tensors="tf",
    )
    return {
        "input_ids": encodings["input_ids"],
        "attention_mask": encodings["attention_mask"],
        "labels": tf.convert_to_tensor(labels, dtype=tf.float32),
    }


df = pd.read_csv("./data/train.csv")

feature = ["comment_text"]
targets = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

X = df[feature]
y = df[targets]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
