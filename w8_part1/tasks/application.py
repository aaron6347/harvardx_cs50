from flask import Flask, redirect, render_template, request

app = Flask(__name__)

tasknames = []

@app.route("/")
def tasks():
    return render_template("tasks.html", tasknames=tasknames)

# accept multiple request method (GET, POST)
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        # get from <form> so use form
        taskname = request.form.get("taskname")
        tasknames.append(taskname)
        # redirect to which route instead of writing render_template which
        return redirect("/")
