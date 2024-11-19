from flask import Flask

app = Flask(__name__)

app.config["DEBUG"] = False
app.config["ENV"] = "production"


@app.route("/")
def home():
    return {"message": "Api Running"}


if __name__ == "__main__":
    app.run()
