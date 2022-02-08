import csv
import os

from flask import Flask, render_template, request

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://jawwcttbtdbrwd:d680a8f23a515f4352869ad725456ca2e19a9310d2168ed00c2a91e7a6bf9861@ec2-52-200-188-218.compute-1.amazonaws.com:5432/d6jne5fv4cp198"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(blind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    header = next(reader)

    for isbn, title, author, published in reader:
        db.execute(
            book = books(isbn=isbn, title=title, author=author, published=published)
        )
    db.commut()

if __name__ == "__main__":
    main()


#Base.init_app(app)


#def main():
#    f = open("books.csv")
#    reader = csv.reader(f)
#    header = next(reader)
#    for isbn, title, author, published in reader:
#        book = books(isbn=isbn, title=title, author=author, published=published)
#        Base.session.add(book)
#    Base.session.commit()

#if __name__ == "__main__":
#    with app.app_context():
#        main()

