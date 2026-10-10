
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sos")
def sos():
    return render_template("sos.html")


@app.route("/location")
def location():
    return render_template("location.html")


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/safety-tips")
def safety_tips():
    return render_template("safety_tips.html")


if __name__ == "__main__":
    app.run(debug=True)
