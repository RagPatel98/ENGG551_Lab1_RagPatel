import os
import sys
import requests
import json

from flask import Flask, session, request, jsonify, redirect, url_for, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.sql.expression import cast
import sqlalchemy

from flask import render_template
from flask_table import Table, Col

app = Flask(__name__)


from data import *
from models import *

# Set up database

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://jawwcttbtdbrwd:d680a8f23a515f4352869ad725456ca2e19a9310d2168ed00c2a91e7a6bf9861@ec2-52-200-188-218.compute-1.amazonaws.com:5432/d6jne5fv4cp198"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#db.init_app(app)
#Initialize DB
db = SQLAlchemy(app)

@app.route("/", methods = ["GET", "POST"])
def index():
    if not session.get('logged_in'):
        return render_template("homepage.html")
    else:
        comments = Comment.query.filter().all()
        return render_template("signedin.html", name=session.get('username'), comments=comments)

@app.route("/home", methods = ["GET","POST"])
def home():
    if not session.get('logged_in'):
        return render_template("homepage.html")
    comments = Comment.query.filter().all()
    return render_template("signedin.html", name=session.get('username'), comments = comments)

@app.route("/signup", methods = ["GET","POST"])
def signup():
    return render_template("signup.html")

@app.route("/signedin", methods = ["POST"])
def signedin():

    if request.method == 'POST':
        session['username'] = request.form.get("name")
        session['password'] = request.form.get("password")
        check_username = accounts.query.filter(accounts.username.like(session.get('username'))).first()
    else:
        return render_template("homepage.html")

    if (check_username is None) or (check_username.username == session.get('username') and check_username.password != session.get('password')):
        session.pop('username', None)
        return render_template("incorrect_login.html", check_user=check_username)
    else:
        session['logged_in'] = True
        comments = Comment.query.filter().all()
        return render_template("signedin.html", name=session.get('username'), comments=comments)
    

@app.route("/books", methods = ["GET", "POST"])
def bookpage():
    book = books.query.filter().all()
    table = Data(book)

    if not session.get('logged_in'):
        return render_template("signup.html")
    
    return render_template("books.html", table=table)

@app.route("/results", methods = ["GET", "POST"])
def results():
    qry=request.form.get("query")
    
    result = books.query.filter((books.isbn.contains(qry)) | (books.title.contains(qry)) | (books.author.contains(qry)) | (cast(books.published, sqlalchemy.String).contains(qry))).all()
    selected_book = result
    result=Data(result)

    return render_template("results.html",query=qry, result=result, selected_book=selected_book)

@app.route("/created_account", methods = ["POST"])
def created_account():
    user = request.form.get("username")
    password = request.form.get("password")
    
    check_user = accounts.query.filter(accounts.username.like(user)).first()

    if check_user is None:
        new_account = accounts(username=user, password=password)
        db.session.add(new_account)
        db.session.commit()
        return render_template("created_account.html", name=user)
    else:
        return render_template("incorrect_login.html", check_user=check_user)

@app.route("/loggedout", methods = ["GET", "POST"])
def loggedout():
    session.clear()
    return render_template("loggedout.html")

@app.route("/gen_comments", methods = ["POST"])
def gen_comments():

    if not session.get('logged_in'):
        return render_template("signup.html")
    else:
        comment = request.form.get("comment")
        new_comment = Comment(name=session.get('username'), body=comment, timestamp=datetime.datetime.now())
        db.session.add(new_comment)
        db.session.commit()
    
    
        new_comment = Comment.query.filter().all()
        table = commentdis(new_comment)

        return render_template("signedin.html", table=table, name=session.get('username'), comments=new_comment)

@app.route('/bookpage/<string:isbn>', methods = ["GET", "POST"])
def book_page(isbn):

    current_book = books.query.filter(books.isbn.like(isbn)).first()

    res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": "isbn:080213825X"})
    print(res.json())       

    average_rating=res.json()['books'][0]['average_rating']
    work_ratings_count=res.json()['books'][0]['work_ratings_count']
    
    if not session.get('logged_in'):
        return render_template("signup.html")


    if request.method=="POST":
        check_review = bookComments.query.filter(bookComments.name.like(session.get('username')), bookComments.isbn.like(isbn)).first()
        if check_review is None:
            body = request.form.get("book_comment")
            rating = request.form.get("rating")
            new_review = bookComments(name=session.get('username'), body=body, rating=rating, isbn=isbn)
            db.session.add(new_review)
            db.session.commit()
            book_comment = bookComments.query.filter(bookComments.isbn.like(isbn)).all()
            return render_template("googlebooks.html", current_book=current_book, average_rating=average_rating, work_ratings_count=work_ratings_count, book_comment=book_comment)
        else:
            if check_review.name==session.get('username') and check_review.isbn==isbn:
                return jsonify("error: Already gave a review for the book"), 422
    else:
        book_comment = bookComments.query.filter(bookComments.isbn.like(isbn)).all()
        return render_template("googlebooks.html", current_book=current_book, average_rating=average_rating, work_ratings_count=work_ratings_count, book_comment=book_comment)
    


@app.route("/api/<string:isbn>", methods = ["GET", "POST"])
def api(isbn):
    current_book = books.query.filter(books.isbn.like(isbn)).first()
    if current_book is None:
        return render_template("404.html")

    res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": "isbn:080213825X"})      

    average_rating=res.json()['books'][0]['average_rating']
    work_ratings_count=res.json()['books'][0]['work_ratings_count']

    book = {
        "title": current_book.title,
        "author": current_book.author,
        "year": current_book.published,
        "isbn": current_book.isbn,
        "review_count": work_ratings_count,
        "average_score": average_rating
    }

    api = json.dumps(book)
    return render_template("api.json", api=api)

