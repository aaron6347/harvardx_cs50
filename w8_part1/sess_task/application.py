from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def tasks():
    # if the cookies data not in session, then create
    if "tasknames" not in session:
        session["tasknames"] = []
    return render_template("tasks.html", tasknames=session["tasknames"])

# accept multiple request method (GET, POST)
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        # get from <form> so use form
        taskname = request.form.get("taskname")
        session["tasknames"].append(taskname)
        # redirect to which route instead of writing render_template which
        return redirect("/")
