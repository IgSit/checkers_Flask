from sqlalchemy.sql import func

from db import db


class User(db.Model) :
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    password_salt = db.Column(db.String(10), nullable=False)
    rankings = db.relationship('Ranking', backref='users', lazy=True)

    create_time = db.Column(db.DateTime, nullable=False, server_default=func.now())
    update_time = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
