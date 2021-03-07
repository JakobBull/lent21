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
    hash = db.Column(db.String, nullable=False)

@dataclass
class Questions(db.Model):

    question_id: int
    level: str
    subject: str
    topic: str
    question_filename: str
    

    question_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    level = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    topics = db.Column(db.String, nullable=False)
    question_filename = db.Column(db.String, nullable=False, unique=True)