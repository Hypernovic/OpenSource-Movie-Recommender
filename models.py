from flask_sqlalchemy import inspect
from flask_login import UserMixin
from app import db



class User(UserMixin,db.Model):
    __tablename__='Users'
    id=db.Column(db.Integer, primary_key=True)
    userName=db.Column(db.String(50), nullable=False)
    password=db.Column(db.Text, nullable=False)
    pic=db.Column(db.Text, nullable=False)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class MovieList(db.Model):
    __tablename__="MovieList"
    id=db.Column(db.Integer,primary_key=True)
    userId=db.Column(db.Integer, db.ForeignKey("Users.id", ondelete='CASCADE'), nullable=False)
    movieName=db.Column(db.Text, nullable=False)
    pic=db.Column(db.Text, nullable=False)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }