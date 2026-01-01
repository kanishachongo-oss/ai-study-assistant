from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_paid = db.Column(db.Boolean, default=False)
    messages_today = db.Column(db.Integer, default=0)
    last_reset = db.Column(db.Date, default=date.today)
