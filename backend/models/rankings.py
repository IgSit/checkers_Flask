from sqlalchemy.sql import func
from sqlalchemy import PrimaryKeyConstraint

from db import db


class Ranking(db.Model) :
    __tablename__ = 'rankings'

    ranking_name = db.Column(db.Enum('Main'), server_default='Main')
    user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
    points = db.Column(db.Integer, default=1000)

    update_time = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        PrimaryKeyConstraint(ranking_name, user_id),
        {},
    )
