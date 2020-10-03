from flask import Flask, render_template, request, redirect
from cs50 import SQL

app = Flask(__name__)
db = SQL("sqlite:///lecture.db")

@app.route("/")
def index():
    row = db.execute("SELECT * FROM registrants;")
    return render_template("index.html", row=row)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("name")
        if not name:
            return render_template("apology.html", message="You must provide a name")
        email = request.form.get("email")
        if not email:
            return render_template("apology.html", message="You must provide an email")
        db.execute("INSERT INTO registrants (name, email) VALUES (:pluginname, :pluginemail)", pluginname=name, pluginemail=email)
        return redirect("/")
