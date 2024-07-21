import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session.get("user_id")

    cash_row = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_row[0]["cash"]

    sum = 0  # Sum of individual stock values
    TOTAL = 0  # Total portfolio value including cash
    rows = db.execute(
        "SELECT symbol, total_shares FROM shareholding WHERE user_id = ?", user_id
    )
    for row in rows:
        look = lookup(row["symbol"])
        row["symbol"] = look["symbol"]
        row["price"] = look["price"]

        row["total"] = row["price"] * row["total_shares"]

        sum += row["total"]

    TOTAL = cash + sum

    return render_template("index.html", rows=rows, cash=cash, TOTAL=TOTAL)
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if symbol == "":
            return apology("MISSING SYMBOL")
        elif shares.isdigit() == False:
            return apology("INVALID NUMBER OF SHARES")
        else:
            # Get stock information using lookup function
            look = lookup(symbol)
            if look == None:
                return apology("INVALID SYMBOL")
            else:
                symbol = look["symbol"]
                price = look["price"]
                user_id = session.get("user_id")
                cash = db.execute(
                    "SELECT cash FROM users WHERE id = ?", user_id)
                total_amount = float(shares) * price

                if float(cash[0]["cash"]) >= total_amount:
                    new_cash = float(cash[0]["cash"]) - total_amount
                    balance = float(cash[0]["cash"]) - total_amount
                    db.execute(
                        "INSERT INTO transactions(user_id,symbol,type, shares,price,transaction_date) VALUES (?,?,?,?,?,?)",
                        user_id, symbol, "buy", shares, price, datetime.now(),
                    )
                    db.execute(
                        "UPDATE users SET cash = ? WHERE id = ?", balance, user_id,)
                    row = db.execute(
                        "SELECT symbol FROM shareholding WHERE user_id = ? AND symbol = ?",
                        user_id,
                        symbol,
                    )
                    if len(row) != 1:
                        db.execute(
                            "INSERT INTO shareholding(user_id, symbol, total_shares) VALUES (?,?,?)",
                            user_id,
                            symbol,
                            shares,
                        )
                    else:
                        row = db.execute(
                            "SELECT total_shares FROM shareholding WHERE user_id = ? AND symbol = ?",
                            user_id,
                            symbol,
                        )
                        old_shares = row[0]["total_shares"]
                        new_shares = old_shares + int(shares)
                        db.execute(
                            "UPDATE shareholding SET total_shares = ? WHERE user_id = ? AND symbol = ?",
                            new_shares,
                            user_id,
                            symbol,
                        )
                        db.execute(
                            "UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id
                        )
                    return redirect("/")
                else:
                    return apology("CAN'T AFFORD")
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session.get("user_id")
    stocks = db.execute(
        "SELECT symbol,shares,price,transaction_date FROM transactions WHERE user_id = ?",
        user_id,
    )
    return render_template("history.html", stocks=stocks)
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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
        # Display the quote form for GET requests
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        print("symbol:")
        print(symbol)
        if symbol == "":
            return apology("MISSING SYMBOL")
        else:
            quote = lookup(symbol)

            if quote == None:
                return apology("INVALID SYMBOL")
            else:
                return render_template(
                    "quoted.html",
                    symbol=quote["symbol"],
                    price=usd(quote["price"])
                )
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Access form data
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        existing_user = db.execute(
            "SELECT username FROM users WHERE username = ?", username
        )

        if username == "" or existing_user:
            return apology("Username is not available")
        elif password == "":
            return apology("MISSING PASSWORD")
        elif confirmation == "" or (password != confirmation):
            return apology("PASSWORDS DON'T MATCH")

        password_hash = generate_password_hash(
            password, method="pbkdf2", salt_length=16
        )

        result = db.execute(
            "INSERT INTO users(username, hash) VALUES (?, ?)", username, password_hash
        )

        if result:
            user_data = db.execute(
                "SELECT id FROM users WHERE username = ?", username)
            if user_data:
                user_id = user_data[0]["id"]
                session["user_id"] = user_id

                return redirect("/")

        return apology("Registration failed")
    return render_template("register.html")
    return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session.get("user_id")

    quotes = db.execute(
        "SELECT symbol FROM shareholding WHERE user_id = ? ", user_id)
    if request.method == "GET":
        return render_template("sell.html", quotes=quotes)
    else:
        symbol = request.form.get("symbol")
        look = lookup(symbol)
        price = look["price"]
        shares_sell = request.form.get("shares")

        # Check for invalid number of shares (non-numeric input)
        if shares_sell.isdigit() == False:
            return apology("INVALID NUMBER OF SHARES")

        rows = db.execute(
            "SELECT total_shares FROM shareholding WHERE user_id = ? and symbol = ?",
            user_id,
            symbol,
        )
        total_shares = rows[0]["total_shares"]

        if int(shares_sell) > total_shares:
            return apology("TOO MANY SHARES")
        else:
            new_shares = total_shares - int(shares_sell)
            if new_shares == 0:
                db.execute(
                    "DELETE FROM shareholding WHERE user_id =? AND symbol =?",
                    user_id,
                    symbol,
                )
            else:
                db.execute(
                    "UPDATE shareholding SET total_shares = ? WHERE user_id = ? and symbol = ?",
                    new_shares,
                    user_id,
                    symbol,
                )

            cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
            new_cash = float(cash[0]["cash"]) + (int(shares_sell) * price)
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id
            )
            db.execute(
                "UPDATE shareholding SET total_shares = ? WHERE user_id = ? and symbol = ?",
                new_shares,
                user_id,
                symbol,
            )

            db.execute(
                "INSERT INTO transactions(user_id, symbol,type,shares,price,transaction_date) VALUES (?,?,?,?,?,?)",
                user_id,
                symbol,
                "sell",
                -int(shares_sell),
                price,
                datetime.now(),
            )

            flash("Sold!", "success")
            return redirect("/")
    return apology("TODO")
