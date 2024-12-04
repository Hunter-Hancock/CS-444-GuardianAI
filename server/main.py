import pandas as pd
from detoxify import Detoxify
from flask import Flask, request

model = Detoxify("original")


app = Flask(__name__)

app.config["DEBUG"] = False
app.config["ENV"] = "production"


@app.route("/", methods=["POST"])
def home():
    data = request.get_json()
    text = data.get("text", "")

    print(text)

    words = text.split()

    predictions = {}

    for word in words:
        results = model.predict([word])

        predictions[word] = results
        
    return {"text": text, "predictions": predictions}


if __name__ == "__main__":
    app.run()
