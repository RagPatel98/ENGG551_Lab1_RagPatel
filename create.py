import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from models import *

engine = create_engine(os.getenv("DATABASE_URL"))
Base.metadata.create_all(engine)

#app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://jawwcttbtdbrwd:d680a8f23a515f4352869ad725456ca2e19a9310d2168ed00c2a91e7a6bf9861@ec2-52-200-188-218.compute-1.amazonaws.com:5432/d6jne5fv4cp198"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#db.init_app(app)
#db = SQLAlchemy(app)


#def main():
#    db.create_all()

#if __name__ == "__main__":
#    with app.app_context():
#        main()
