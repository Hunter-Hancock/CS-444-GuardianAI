import pandas as pd
from transformers import BertTokenizer, TFBertForSequenceClassification, create_optimizer
from sklearn.model_selection import train_test_split
import tensorflow as tf

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=6)

def tokenize(text, labels, tokenizer) :
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
        "labels": tf.convert_to_tensor(labels.values, dtype=tf.float32),
    }

df = pd.read_csv("./train.csv")
feature = ["comment_text"]
targets = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

X = df[feature]
y = df[targets]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

train_data = tokenize(X_train, y_train, tokenizer)
test_data = tokenize(X_test, y_test, tokenizer)

def create_dataset(data, batch_size=16):
    dataset = tf.data.Dataset.from_tensor_slices(
        (
            {"input_ids": data["input_ids"], "attention_mask": data["attention_mask"]},
            data["labels"],
        )
    )
    return dataset

train_dataset = create_dataset(train_data)
test_dataset = create_dataset(test_data)

batch_size = 16
epochs = 3
steps_per_epoch = len(train_dataset)
num_train_steps = steps_per_epoch * epochs
optimizer, lr_schedule = create_optimizer(init_lr=2e-5, num_train_steps=num_train_steps, num_warmup_steps=0)
loss_fn = tf.keras.losses.BinaryCrossentropy(from_logits=True)

model.compile(optimizer=optimizer, loss=loss_fn, metrics=["accuracy"])

model.fit(train_dataset, validation_data=test_dataset, epochs=epochs)

model.save_pretrained("./trained_model")
tokenizer.save_pretrained("./trained_model")
