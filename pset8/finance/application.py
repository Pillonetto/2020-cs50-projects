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
    cash = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
    #select what was bought in this account
    query = "SELECT symbol, SUM(shares) FROM transactions WHERE user_id = ? AND type = 1 GROUP BY symbol;"
    bought = db.execute(query, session["user_id"])
    if len(bought) == 0:
        return render_template("index.html", present=present, cash=cash, total="You don't have shares yet.")

    #start count of grand total
    grand=cash[0]["cash"]
    #list to keep track of info to present
    present={}
    #for every buy

    for row in bought:
        #get sells from the current user and compare it to what was bought
        query = "SELECT SUM(shares) FROM transactions WHERE user_id=? AND type = 0 AND symbol=? GROUP BY symbol;"
        sells = db.execute(query, session["user_id"], row["symbol"])

        if len(sells) == 0:
            buys = row["SUM(shares)"]
        else:
            buys = row["SUM(shares)"] - sells[0]["SUM(shares)"]

        if buys > 0:
            total = round(buys * lookup(row["symbol"])["price"], 2)
            grand+=total
            #create a list with the info you want to present
            present[row["symbol"]] = [row["symbol"], buys, lookup(row["symbol"])["price"], total]


    grand = round(grand, 2)
    return render_template("index.html", present=present, cash=cash[0]["cash"], total=grand)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Insert a valid symbol.", 403)

        if not request.form.get("shares"):
            return apology("Insert a number os shares", 403)

        shares = int(request.form.get("shares"))

        if shares < 1:
            return apology("You must buy at least one share.", 403)

        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Symbol not found.", 403)
        current_money = int(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])

        shares = shares * stock["price"]

        if shares > current_money:
            return apology("You can't afford this number of shares at the current price.", 403)

        current_money -= shares


        result = db.execute("INSERT INTO transactions (user_id, price, type, symbol, shares, date) VALUES (?, ?, 1, ?, ?, CURRENT_TIMESTAMP);", session["user_id"], stock["price"], stock["symbol"], request.form.get("shares"))

        result = db.execute("UPDATE users SET cash = ? WHERE id = ?;", current_money, session["user_id"])


        return redirect("/")

    else:
        return render_template("buy.html")

    return apology(500)


@app.route("/history")
@login_required
def history():
    transactions = []
    query = 'SELECT symbol, price, type, date, shares FROM transactions WHERE user_id =?;'
    query = db.execute(query, session["user_id"])
    if len(query) == 0:
        return apology("You don't have any recorded transactions", 403)


    for row in query:
        #if it was bought
        if row["type"] == 1:
            #add dict to list
            transactions.append({'symbol': row["symbol"], 'price': row["price"], 'type':'Bought', 'date': row["date"], 'shares': row["shares"]})

        else:
            transactions.append({'symbol': row["symbol"], 'price': row["price"], 'type':'Sold', 'date': row["date"], 'shares': row["shares"]})


    return render_template("history.html", transactions=transactions)

    """Show history of transactions"""
    return apology("TODO")


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


@app.route("/passwordchange", methods=["GET", "POST"])
@login_required
def change_pass():
    if request.method == "GET":
        return render_template("password.html")

    #check the current password
    user = db.execute("SELECT hash FROM users WHERE id=?;", session["user_id"])

    if len(user) == 0 or not check_password_hash(user[0]["hash"], request.form.get("password")):
        return apology("Invalid username and/or password", 403)

    if request.form.get("new_pass") != request.form.get("confirmation"):
        return apology("The passwords don't match", 403)

    #gen hash for the new inserted one
    new_pass = generate_password_hash(request.form.get("new_pass"))
    #update out database
    result = db.execute("UPDATE users SET hash=? WHERE id=?", new_pass, session["user_id"])
    #take the user back to front page

    session.clear()

    return redirect("/")


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
    if request.method == "POST":
        return_v = lookup(request.form.get("symbol"))
        if return_v != None:
            name, price, symbol = return_v["name"], return_v["price"], return_v["symbol"]
            return render_template("quoted.html", symbol = symbol, name = name, price = price)
        else:
            return apology("Symbol does not exist/wasn't found.", 403)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            return apology("Insert a valid Username/password.", 403)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("The passwords don't match.", 403)
        else:
            result = "SELECT username FROM users WHERE username = ?"
            check = db.execute(result, request.form.get("username"))
            if check:
                return apology("That username is already in use.", 403)

            result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", request.form.get("username"), generate_password_hash(request.form.get("password")))
            return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Insert a valid symbol", 400)
        elif int(request.form.get("shares")) <= 0:
            return apology("Insert a valid number of shares.", 400)
        elif not lookup(request.form.get("symbol")):
            return apology("Insert a valid symbol", 400)


        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        asset = "SELECT SUM(shares) FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol;"
        asset = db.execute(asset, session["user_id"], symbol)

        if shares > asset[0]["SUM(shares)"]:
            return apology("You don't have that many shares to sell.", 403)

        else:
            result = db.execute("INSERT INTO transactions (user_id, price, symbol, date, type, shares) VALUES (?, ?, ?, CURRENT_TIMESTAMP, 0, ?);", session["user_id"], lookup(symbol)["price"], symbol, shares)

            new_cash = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
            gain = shares * lookup(symbol)["price"]
            new_cash = round(new_cash[0]["cash"] + gain, 2)
            result = db.execute("UPDATE users SET cash = ? WHERE id = ?;", new_cash, session["user_id"])

            return redirect("/")

    else:
        stocks=[]

        query = "SELECT symbol, SUM(shares) FROM transactions WHERE user_id = ? AND type = 1 GROUP BY symbol;"
        bought = db.execute(query, session["user_id"])

        if len(bought) == 0:
            return apology("You don't have stocks yet.", 403)

        for row in bought:

            query = "SELECT SUM(shares) FROM transactions WHERE user_id=? AND type = 0 AND symbol=? GROUP BY symbol;"
            sells = db.execute(query, session["user_id"], row["symbol"])

            if len(sells) == 0:
                stocks.append(row["symbol"])
            else:
                if row["SUM(shares)"] > sells[0]["SUM(shares)"]:
                    stocks.append(row["symbol"])

        return render_template("sell.html", stocks=stocks)

    return apology("Unknown Error.", 500)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
