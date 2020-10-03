import random
from flask import Flask, render_template, request

app = Flask(__name__)

# default route
@app.route("/")
def index():
    number = random.randint(1, 10)
    number2 = random.randint(0, 1)
    # render_template from templates(must be same) and pass parameter as jinja
    return render_template("index.html", number=number, name="Emma", number2=number2)

@app.route("/goodbye")
def bye():
    return "Goodbye!"

@app.route("/hello")
def hello():
    # get name="name2" from html
    name2 = request.args.get("name2")
    if not name2:
        return render_template("failure.html")
    return render_template("hello.html", name2=name2)