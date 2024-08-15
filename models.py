from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from config import CHATGPT_BASIC

db = SQLAlchemy()

with open("prompt.txt", "r", encoding="utf-8") as f:
    bprompt = f.read()


class Model(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer)
    model_name = db.Column(db.String, default=CHATGPT_BASIC)


class Prompt(db.Model):
    __tablename__ = 'prompts'
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer)
    prompt = db.Column(db.String, default=bprompt)
