import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    records = []
    bigtotal = 0

    # get dictionary of symbol and shares that user owns
    rows = db.execute("SELECT symbol, shares FROM stonks where id = :id;", id = session['user_id'])

    # get current price and total
    for each in rows:
        answer = lookup(each['symbol'])
        name = answer['name']
        price = float(answer['price'])
        total = float(price*int(each['shares']))
        records.append([each['symbol'], name, each['shares'], usd(price), usd(total)])
        bigtotal += total

    # get cash that user owns
    cash = db.execute("SELECT cash from users WHERE id=:id;", id=session['user_id'])[0]['cash']

    bigtotal += cash
    return render_template("index.html", records=records, bigtotal=usd(bigtotal), cash=usd(cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # if request is get, user request to key in symbol and shares
    if request.method == "GET":
        return render_template("buy.html")

    # if request is post, user request to buy the symbol
    else:

        symbol = request.form.get("symbol").upper()
        # if the symbol is blank
        if not symbol:
            return apology("The symbol cannot be blank", 400)

        answer = lookup(symbol)
        # if the symbol doesn't exist
        if not answer:
            return apology("The symbol doesn't exist", 403)

        # if the symbol exist
        else:

            # if shares is blank
            if not request.form.get("shares"):
                return apology("The shares cannot be blank", 400)

            # if shares is not blank
            else:

                quantity = request.form.get("shares")
                # if the shares is not int
                try:
                    quantity = int(quantity)
                except ValueError as e:
                    return apology("Shares must be an integer", 403);

                total = float(answer['price']*quantity)

                # get cash that user owns
                cash = db.execute("SELECT cash FROM users WHERE id = :id;", id=session['user_id'])[0]['cash']

                # if the cash is insufficient to purchase
                if cash < total:
                    return apology("Your cash is insufficient to purchase the shares", 403)

                # if cash is sufficient for the shares
                else:

                    # get time
                    from datetime import datetime
                    now = datetime.now()
                    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

                    # create table trans if doesnt exist
                    # trans is for the records of every purchase and selling
                    db.execute("CREATE TABLE IF NOT EXISTS 'trans' ( \
                        identifier INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                        id INTEGER NOT NULL, \
                        symbol TEXT NOT NULL, \
                        shares INTEGER NOT NULL, \
                        prices NUMERIC NOT NULL, \
                        tran_date DATETIME NOT NULL);")
                    # create index if doesnt exist
                    db.execute("CREATE UNIQUE INDEX IF NOT EXISTS 'AK_id_symbol_datetime' ON 'trans'(\"id\", \"symbol\", \"tran_date\")")

                    # insert the transaction
                    db.execute("INSERT INTO 'trans' (id, symbol, shares, prices, tran_date) VALUES (?, ?, ?, ?, ?);", \
                        session['user_id'], symbol, quantity, total, formatted_date)

                    # create table stonks if doesnt exist
                    # stonks is for the remembering the current shares that you have
                    # (created due to trans table will be more heavy and not suitable for finding sum of shares,
                    # which is needed when showing portfolio and selling shares)
                    db.execute("CREATE TABLE IF NOT EXISTS 'stonks' ( \
                        identifier INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                        id INTEGER NOT NULL, \
                        symbol TEXT NOT NULL, \
                        shares INTEGER NOT NULL);")

                    # create index if doesnt exist
                    db.execute("CREATE UNIQUE INDEX IF NOT EXISTS 'AK_id_symbol' ON 'stonks'(\"id\", \"symbol\");")

                    # select the shares to see if it exists
                    shares = db.execute("SELECT shares FROM stonks WHERE id=:id AND symbol=:symbol;", id=session['user_id'], symbol=symbol)

                    # if the shares doesnt exist
                    if len(shares) == 0:

                        # insert the transaction
                        db.execute("INSERT INTO 'stonks' (id, symbol, shares) VALUES (?, ?, ?);", \
                            session['user_id'], symbol, quantity)

                    # if there is an amount of shares
                    else:
                        shares = int(shares[0]['shares'])

                        # insert the transaction
                        db.execute("UPDATE 'stonks' SET shares=:new_shares WHERE id=:id AND symbol=:symbol;", \
                            id=session['user_id'], symbol=symbol, new_shares=quantity+shares)

                    # update user's cash
                    db.execute("UPDATE users SET cash=:remain WHERE id=:id;", remain=cash-total, id=session['user_id'])
                    flash("Bought!")
                    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    records = []

    # get dictionary of symbol and shares that user owns
    rows = db.execute("SELECT symbol, shares, prices, tran_date FROM trans where id = :id ORDER BY tran_date;", id = session['user_id'])

    # change dictionary to list and all into rows of records
    for each in rows:
        records.append([each['symbol'], each['shares'], usd(each['prices']), each['tran_date']])
    return render_template("history.html", records=records)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # if request is get, user request to key in symbol
    if request.method == "GET":
        return render_template("quote.html")

    # if request is post, user request to submit quoted symbol
    else:

        # if symbol is blank
        if not request.form.get("symbol"):
            return apology("The symbol cannot be blank", 400)

        answer = lookup(request.form.get("symbol"))
        # if the symbol doesn't exist
        if not answer:
            return apology("The symbol doesn't exist", 403)

       #if the symbol exist
        return render_template("quoted.html", symbol_fullname=answer['name'], price=usd(answer['price']), symbol=answer['symbol'])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # if the request is get, user request to register account
    if request.method == "GET":
        return render_template("register.html")

    # if the request is post, user request to submit acount registration
    else:

        submitted_username = request.form.get("username")
        # if the username is blank
        if not submitted_username:
            return apology("Username cannot be blank", 400)

        same_username = db.execute("SELECT username FROM users WHERE username=:username; ", username=submitted_username)
        # if the username is pre-existed
        if len(same_username) != 0:
            return apology("Username is already existed", 403)

        submitted_password = request.form.get("password")
        submitted_confirmation = request.form.get("confirmation")

        # if the password is blank
        if not submitted_password:
            return apology("Password cannot be blank", 400)

        # if the confirmation password is blank
        if not submitted_password:
            return apology("Confirmation Password cannot be blank", 400)

        # if password and confirmation do not match
        if submitted_password != submitted_confirmation:
            return apology("Password and Confirmation Password do not match", 403)

        # if password doesn't meet requirement, contain at least one letter, number and symbol
        if not valid_pass(submitted_password):
            return apology("The password must contain at least one letter, number and symbol combination", 403)

        # if username and password validations are correct
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashp)", \
            username=submitted_username, hashp=generate_password_hash(submitted_password))

        # get the id
        id_now = db.execute("SELECT id FROM users WHERE username=:username;", username=submitted_username)[0]['id']

        session["user_id"] = id_now
        flash("Registered!")
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # if request is get, user request to select symbol
    if request.method == "GET":

        # get dictionary of all symbols
        answer = db.execute("SELECT DISTINCT(symbol) FROM stonks WHERE id=:id;", id=session['user_id'])
        options = [each['symbol'] for each in answer]
        return render_template("sell.html", options=options)

    # if the request is post, user request to sell symbol
    else:

        selected = request.form.get("symbol")
        # if the symbol is empty
        if not selected:
            return apology("A symbol is must be selected", 400)

        # if the shares is blank
        if not request.form.get("shares"):
            return apology("Shares cannot be blank", 400)


        # if symbol is selected and shares is positive
        else:
            # get total available shares to sell of specific symbol
            available = int(db.execute("SELECT shares FROM stonks WHERE id=:id AND symbol=:selected;", id=session['user_id'], selected=selected)[0]['shares'])
            shares = request.form.get("shares")

            # if the shares is not integer
            try:
                shares = int(shares)
            except ValueError as e:
                return apology("Shares must be an integer", 403)


            # if shares is more than available
            if shares > available:
                return apology("Cannot sell more shares than you owned", 403)

            # else shares is less or equal than available:
            else:

                # look for current price
                prices = lookup(selected)['price']

                # get time
                from datetime import datetime
                now = datetime.now()
                formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

                # insert the transaction
                db.execute("INSERT INTO 'trans' (id, symbol, shares, prices, tran_date) VALUES (?, ?, ?, ?, ?);", \
                    session['user_id'], selected, -shares, float(prices*shares), formatted_date)

                # get user's cash
                cash = float(db.execute("SELECT cash FROM users WHERE id=:id;", id=session['user_id'])[0]['cash'])

                # update user's cash
                db.execute("UPDATE users SET cash=:cash WHERE id=:id;", id=session['user_id'], cash=float(prices*shares)+cash)

                # if the amount of avaialble shares to sell and to be sold is the same
                if shares == available:

                    # delete the row from stonks
                    db.execute("DELETE FROM stonks WHERE id=:id AND symbol=:selected AND shares=:shares;", \
                        id=session['user_id'], selected=selected, shares=shares)

                # if the amount of available shares to sell and to be sold isnt the same (logically there is remaining amount after selling)
                else:

                    # update the stonks
                    db.execute("UPDATE stonks SET shares=:remain WHERE id=:id AND symbol=:selected;", \
                        id=session['user_id'], selected=selected, remain=available-shares)
                flash("Sold!")
                return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


# Change Password
@app.route("/change", methods=["GET", "POST"])
@login_required
def change():

    # if the request is GET, user request to key in new password
    if request.method == "GET":
        return render_template("change.html")
    # if the request is POST, user request to change the password
    else:

        # get current password
        oldpass = db.execute("SELECT hash FROM users WHERE id=:ids;", ids=session['user_id'])[0]['hash']

        password = request.form.get("password")
        # if current password is blank
        if not password:
            return apology("The current password cannot be blank", 400)

        # if current password doesn't match
        if not check_password_hash(oldpass, password):
            return apology("The current password doesn't match", 403)

        new_password = request.form.get("new_password")
        # if new password is blank
        if not new_password:
            return apology("The new password cannot be blank", 400)

        new_password2 = request.form.get("new_password2")
        # if new password is blank
        if not new_password2:
            return apology("The new confirmed password cannot be blank", 400)

        # if new password and new confirmed password don't match
        if new_password != new_password2:
            return apology("The new password and new confirmed password don't match", 403)

        # if password doesn't meet requirement, contain at least one letter, number and symbol
        if not valid_pass(new_password):
            return apology("The password must contain at least one letter, number and symbol combination", 403)

        # if current password matched, new passwords matched
        db.execute("UPDATE users SET hash=:new_hash WHERE id=:ids;", new_hash=generate_password_hash(new_password), ids=session['user_id'])
        flash("Changed password!")
        return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    # if the request is GET, the user request to key in amount
    if request.method == "GET":
        return render_template("add.html")

    # if the request is POST, the user request to add cash
    else:

        amount = request.form.get("amount")
        # if the amount is blank
        if not amount:
            return apology("The amount cannot be blank", 400)

        # if the amount is zero
        if float(amount) == 0.00:
            return apology("The amount cannot be zero", 403)

        # if the amount is acceptable
        else:

            # get user's cash
            cash = db.execute("SELECT cash FROM users WHERE id=:ids;", ids=session["user_id"])[0]['cash']

            # add cash to user
            db.execute("UPDATE users SET cash=:new_cash WHERE id=:ids;", ids=session["user_id"], new_cash=float(amount)+cash)

            flash("Added Cash!")
            return redirect("/")

def valid_pass(password):
    import re

    # if password contain at least one letter, number and symbol
    if bool(re.search('[a-zA-Z]', password)) and bool(re.search('[0-9]', password)) and bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', password)):
        return True
    return False