import pandas as pd
from detoxify import Detoxify
from flask import Flask, request

model = Detoxify('original')


app = Flask(__name__)

app.config["DEBUG"] = False
app.config["ENV"] = "production"


@app.route("/", methods=["POST"])
def home():
    data = request.get_json()
    text = [data.get('text', '')]

    print(text[0])

    results = model.predict(text[0])

    df = pd.DataFrame(results, index=text)

    filtered = [df[column].iloc[0].item() for column in df.columns]

    return {
        "text": text[0],
        "labels": filtered
    }


if __name__ == "__main__":
    app.run()
