from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from helpers import apology, login_required
from datetime import date

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///neetya_news.db")

@app.route("/profile2", methods=["GET", "POST"])
@login_required
def profile2():
    profiles = db.execute("SELECT education, username FROM users WHERE request = 'On Hold';")
    return render_template("owner.html", profiles=profiles)

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    user_id = session['user_id']
    if user_id == 1:
        return redirect('/')
    rows = db.execute("SELECT request, news_title, name FROM own_news WHERE user_id = ?", user_id)
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]['username']
    return render_template("index.html", username=username, rows=rows)

@app.route("/home1", methods=["GET", "POST"])
@login_required
def home1():
    if request.method == "GET":
        rows = db.execute("SELECT news_title, name, article, user_id FROM own_news WHERE request = 'On Hold';")
        return render_template("owner2.html", rows=rows)
    else:
        title = request.form.get("title")
        db.execute("UPDATE own_news SET request = 'Approved' WHERE news_title = ?", title)
        return redirect("/")

@app.route("/add_news", methods=["GET", "POST"])
@login_required
def add_news():
    if request.method == 'GET':
        return render_template("add_news.html")
    else:
        user_id = session["user_id"]
        title = request.form.get("title")
        article = request.form.get("article")
        if article == "" or title == "":
            return apology("Title and/or Article is REQUIRED")
        exist = db.execute("SELECT COUNT(*) AS counter FROM own_news WHERE news_title = ?", title)[0]['counter']
        if exist > 0:
            return apology("Title aldready exists :(")
        username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]['username']
        db.execute("INSERT INTO own_news (news_title, article, user_id, request, name, views, likes, time) VALUES (?, ?, ?, 'On Hold', ?, 0, 0, ?)", title, article, user_id, username, date.today())
        return redirect("/")

@app.route("/profiles", methods=["GET", "POST"])
@login_required
def profiles():
    if request.method == "GET":
        rows = db.execute("SELECT education, username FROM users WHERE request = 'Approved';")
        return render_template("profile.html", rows=rows)
    else:
        username = request.form.get("username")
        db.execute("DELETE FROM users WHERE username = ?;", username)
        return redirect("/")

@app.route("/")
def index():
    popular = db.execute("SELECT news_title, name, views FROM own_news WHERE request = 'Approved' ORDER BY views DESC LIMIT 5;")
    rows = db.execute("SELECT news_title, name, views FROM own_news WHERE request ='Approved' ORDER BY DATE(time) DESC;")
    return render_template("news.html", rows=rows, populars=popular)

@app.route("/approval", methods=["GET", "POST"])
def approval():
    if request.method == "GET":
        return render_template("register.html")
    else:
        education = request.form.get("education")
        username = request.form.get("username")
        password = request.form.get("password")

        #Error check
        if username == "" or password == "":
            return apology("Username and/or password required!!")

        exist = db.execute("SELECT COUNT(*) AS counter FROM users WHERE username = ? AND request = 'Approved';", username)[0]['counter']
        if exist > 0:
            return apology("Username aldready exists!")

        if len(username) > 30 or len(password) > 30:
            return apology("Username and/or password have to be max 30 characters")

        db.execute("INSERT INTO users (username, password, education, request) VALUES (?, ?, ?, ?);", username, generate_password_hash(password), education, 'On Hold')

        return redirect("/")


@app.route("/like", methods=["GET", "POST"])
def like():
    title = request.form.get("title")
    views = db.execute('SELECT views FROM own_news WHERE news_title = ?;', title)[0]['views']
    l = db.execute("SELECT likes FROM own_news WHERE news_title = ?", title)[0]['likes']
    l = l + 1
    db.execute("UPDATE own_news SET likes = ? WHERE news_title = ?;", l, title)
    likes = db.execute('SELECT likes FROM own_news WHERE news_title = ?;', title)[0]['likes']
    comments = db.execute("SELECT comments.comment, comments.adjective FROM comments JOIN own_news ON comments.news_id = own_news.id WHERE news_title = ?", title)
    article = db.execute("SELECT article FROM own_news WHERE news_title = ?", title)[0]['article']
    return render_template("read_news.html", article=article, title=title, comments=comments, views=views, likes=likes)

@app.route("/read_news", methods=["GET", "POST"])
def read_news():
    on_hold=False
    title = request.form.get("title")
    if db.execute("SELECT request FROM own_news WHERE news_title = ?", title)[0]['request'] == 'On Hold':
        on_hold = True
    likes = db.execute("SELECT likes FROM own_news WHERE news_title = ?", title)[0]['likes']
    v = db.execute('SELECT views FROM own_news WHERE news_title = ?;', title)[0]['views'] + 1
    db.execute("UPDATE own_news SET views = ? WHERE news_title = ?;", v, title)
    views = db.execute('SELECT views FROM own_news WHERE news_title = ?;', title)[0]['views']
    comments = db.execute("SELECT comments.comment, comments.adjective FROM comments JOIN own_news ON comments.news_id = own_news.id WHERE news_title = ?", title)
    article = db.execute("SELECT article FROM own_news WHERE news_title = ?", title)[0]['article']
    return render_template("read_news.html", article=article, title=title, comments=comments, views=views, likes=likes, on_hold=on_hold)

@app.route("/search_news", methods=["GET", "POST"])
def search():
    no_results = False
    title = request.form.get("title")
    results = []
    if title=="":
        return apology("Please fill in reqired box before searching")
    rows = db.execute("SELECT news_title FROM own_news")
    for row in rows:
        if title.upper() in row['news_title'].upper():
            result = db.execute("SELECT news_title, name, views FROM own_news WHERE news_title = ?", row['news_title'])
            results.append(result)
    if len(results) > 0:
        return render_template("news.html", results=results, no_results=no_results)
    result = None
    return render_template("news.html", result=result, title=title, no_results=True)

@app.route("/comment", methods=["GET", "POST"])
def comment():
    title = request.form.get("title")
    views = db.execute('SELECT views FROM own_news WHERE news_title = ?;', title)[0]['views']
    likes = db.execute("SELECT likes FROM own_news WHERE news_title = ?", title)[0]['likes']
    adjective = request.form.get("adjective").strip()
    if adjective == '':
        return apology("Please choose an appropriate name")
    comment = request.form.get("comment")
    if comment == "":
        return apology("Comment is missing!")
    article = db.execute("SELECT article FROM own_news WHERE news_title = ?", title)[0]['article']
    news_id = db.execute("SELECT id FROM own_news WHERE news_title = ?", title)[0]['id']
    db.execute("INSERT INTO comments (news_id, comment, adjective) VALUES (?, ?, ?)", news_id, comment, adjective)
    comments = db.execute("SELECT comments.comment, comments.adjective FROM comments JOIN own_news ON comments.news_id = own_news.id WHERE news_title = ?", title)
    return render_template("read_news.html", title=title, comments=comments, article=article, views=views, likes=likes)


@app.route("/login", methods=["GET", "POST"])
def login():

    #Forget any user_id
    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "" or password == "":
            return apology("Please provide username and/or password!")

        rows = db.execute("SELECT * FROM users WHERE username = ? AND request = 'Approved';", username)
        if len(rows) != 1 or not check_password_hash(rows[0]['password'], password):
            return apology("Username and/or passoword doesn't exist!")

        #Remember user
        session['user_id'] = rows[0]['id']

        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("name")
    db.execute("UPDATE users SET request = 'Approved' WHERE username = ?;", username)
    return redirect("/home")

@app.route("/delete_news", methods=["GET", "POST"])
@login_required
def delete_news():
    title = request.form.get("title")
    db.execute("DELETE FROM own_news WHERE news_title = ?", title)
    return redirect("/")

@app.route("/delete_profile", methods=["GET", "POST"])
@login_required
def delete_profile():
    username = request.form.get("name")
    db.execute("DELETE FROM users WHERE username = ?", username)
    return redirect("/home")

@app.route("/list_news")
@login_required
def list_news():
    titles = db.execute("SELECT news_title FROM own_news WHERE request = 'Approved';")
    return render_template("list_news.html", titles=titles)

@app.route("/delete_comment", methods=["GET", "POST"])
@login_required
def delete_comment():
    comment = request.form.get("comment")
    db.execute("DELETE FROM comments WHERE comment = ?", comment)
    return redirect("/")

