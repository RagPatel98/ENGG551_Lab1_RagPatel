from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class accounts(Base):
    __tablename__ = "accounts"
    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.username
    
    def is_unique(self):
        return True


    def is_active(self):
        return True
    def is_anon(self):
        return False


class books(Base):
    __tablename__ = "books"
    isbn = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published = Column(Integer, nullable=False)


class Comment(Base):
    __tablename__ = "gen_comments"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    body = Column(String)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.now)
    

    def __init__(self, name, body, timestamp):
        self.name = name
        self.body = body
        self.timestamp = timestamp

class bookComments(Base):
    __tablename__ = "book_comments"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    body = Column(String)
    rating = Column(String, nullable = False)
    isbn = Column(String, nullable=False)
    
    def __init__(self, name, body, rating, isbn):
        self.name = name
        self.body = body
        self.rating = rating
        self.isbn = isbn
