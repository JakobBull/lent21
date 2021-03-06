from dataclasses import dataclass
from datetime import datetime   
from . import db

@dataclass
class Users(db.Model):

    user_id: int
    user_name: str
    password: str

    user_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

@dataclass
class Questions(db.Model):

    question_id: int
    question_name: str
    subject: str
    topic: str
    

    question_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    question_name = db.Column(db.String, nullable=False, unique=True)
    subject = db.Column(db.String, nullable=False)
    topic = db.Column(db.String, nullable=False)
    topic = 