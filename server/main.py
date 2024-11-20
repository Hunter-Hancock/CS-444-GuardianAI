from flask import Flask, request

app = Flask(__name__)

app.config["DEBUG"] = False
app.config["ENV"] = "production"


@app.route("/")
def home():
    text = request.args.get("text")
    return {"message": f"You sent: {text}"}


if __name__ == "__main__":
    app.run()
