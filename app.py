#Neetya, You need to make ownStocks as a table cuz in history you need to show all transactions

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    if request.method == "GET":
        user_id = session['user_id']
        rows = db.execute("SELECT shares, price FROM ownStocks WHERE user_id = ?", user_id)
        total_cash = db.execute("SELECT cash FROM users WHERE id == ?", user_id)[0]['cash']
        total = total_cash
        for row in rows:
            total += row['shares'] * row['price']
        return render_template("cash.html", cash = total_cash, total = total)
    else:
        user_id = session['user_id']
        cash = request.form.get('cash')
        rows = db.execute("SELECT shares, price FROM ownStocks WHERE user_id = ?", user_id)
        total_cash = db.execute("SELECT cash FROM users WHERE id == ?", user_id)[0]['cash']
        total = total_cash
        for row in rows:
            total += row['shares'] * row['price']
        if not cash:
            return apology("Amount of Cash is required!")
        cash = int(cash)
        wanted_total = total + cash
        if wanted_total > 20000:
            return apology("Maximum Valuation is $20000")

        db.execute("UPDATE users SET cash = ? WHERE id = ?", total_cash + cash, user_id)
        return redirect("/")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]['username']
    name = username.split(".")
    name = name[0].split(" ")
    name = name[0]
    transactions_db = db.execute("SELECT symbol, name, shares, price FROM ownstocks WHERE user_id = ?", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?;", user_id)[0]['cash']
    total = cash
    for row in transactions_db:
        total += row["shares"] * row["price"]

    return render_template("index.html", user_exchanges = transactions_db, cash = cash, total = total, username = name.capitalize())

@app.route("/buy", methods=["GET", "POST"])
@login_required

def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol is required")
        shares = request.form.get("shares")
        if not shares:
            return apology("No. of shares are required!")
        shares = int(shares)
        if shares < 1:
            return apology("Enter a VALID no. of shares")
        stock = lookup(symbol.upper())
        if stock == None or stock['name'] == "":
            return apology("Symbol doesn't exist")

        user_id = session['user_id']
        cash = db.execute("SELECT cash FROM users WHERE id == ?;", user_id)[0]['cash']
        remain = cash - shares * stock['price']
        if remain < 0:
            return apology("Cannot Afford")
        db.execute("UPDATE users SET cash = ? WHERE id = ?;", remain, user_id)
        symbols = db.execute("SELECT COUNT(?) AS symbols FROM ownStocks WHERE symbol = ?", symbol, symbol)[0]['symbols']
        if symbols == 0:
            db.execute("INSERT INTO ownstocks (user_id, symbol, shares, price, name) VALUES (?, ?, ?, ?, ?);", user_id, stock['symbol'], shares, stock['price'], stock['name'])
        else:
            total_shares = db.execute("SELECT shares FROM ownStocks WHERE symbol LIKE ? AND user_id = ?", symbol, user_id)[0]['shares']
            db.execute("UPDATE ownStocks SET shares = ? WHERE symbol LIKE ? AND user_id = ?", total_shares + shares, symbol, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date, name, type) VALUES (?, ?, ?, ?, ?, ?, ?);", user_id, stock['symbol'], shares, stock['price'], datetime.now(), lookup(symbol)['name'], 'buy')
        flash("Bought!")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    rows = db.execute("SELECT symbol, shares, price, date, name, type FROM transactions WHERE user_id = ?", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]['cash']
    return render_template("history.html", rows = rows, cash = cash)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?;", request.form.get("username"))

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
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Must provide symbol")

        stock = lookup(symbol.upper())
        if stock == None or stock['name'] == "":
            return apology("Symbol doesn't exist!")

        return render_template("quoted.html", name = stock["name"], price = stock["price"], symbol = stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or len(db.execute("SELECT * FROM users WHERE username == ?;", username)) > 0:
            return apology("must provide a unique username")

        if not password or password != confirmation:
            return apology("must provde password that matches the confirmation")

        new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", username, generate_password_hash(confirmation))
        session["user_id"] = new_user

        return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        user_id = session['user_id']
        rows = db.execute("SELECT symbol FROM ownStocks WHERE user_id = ?;", user_id)
        stocks = db.execute("SELECT symbol, price, name, shares FROM ownStocks WHERE user_id = ?;", user_id)
        return render_template("sell.html", symbols = [row["symbol"] for row in rows], db = stocks)
    else:
        user_id = session['user_id']
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol is required")
        shares = request.form.get("shares")
        if not shares:
            return apology("No. of shares are required!")
        shares = int(shares)
        if shares < 1:
            return apology("Enter a VALID no. of shares")
        stocks = db.execute("SELECT symbol FROM ownStocks WHERE user_id = ?;", user_id)
        symbols = []
        for stock in stocks:
            symbols.append(stock["symbol"])
        if not symbol in symbols:
            return apology("You do not own that symbol")
        total_shares = db.execute("SELECT shares FROM ownStocks WHERE symbol = ? AND user_id = ?;", symbol, user_id)[0]['shares']
        if int(total_shares) < shares:
            return apology("You don't have as many shares!")
        price = lookup(symbol)['price']
        db.execute("UPDATE ownStocks SET shares = ? WHERE user_id = ? AND symbol = ?", total_shares - shares, user_id, symbol)
        db.execute("DELETE FROM ownStocks WHERE shares = 0 AND user_id = ?", user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date, name, type) VALUES (?, ?, ?, ?, ?, ?, ?);", user_id, symbol, shares, price, datetime.now(), lookup(symbol)['name'], 'sell')
        cash = db.execute("SELECT cash FROM users WHERE id == ?;", user_id)[0]['cash']
        db.execute("UPDATE users SET cash = ? WHERE id = ?;", cash + shares * price, user_id)
        flash("Sold!")
        return redirect("/")