from sqlalchemy.sql import func

from db import db


class Session(db.Model) :
    __tablename__ = 'sessions'

    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
    token = db.Column(db.String(80), nullable=False)

    signed_out_time = db.Column(db.DateTime, nullable=True)

    create_time = db.Column(db.DateTime, nullable=False, server_default=func.now())
    update_time = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
