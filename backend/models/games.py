from sqlalchemy.sql import func
from sqlalchemy import Boolean

from db import db


class Game(db.Model) :
    __tablename__ = 'games'

    game_id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.ForeignKey('rooms.room_id'), nullable=False)

    type = db.Column(db.Enum('Main'), server_default='Main')
    size = db.Column(db.Enum('8x8', '12x12', '16x16'), server_default='8x8', nullable=False)

    player_1_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
    player_1_points = db.Column(db.Integer, nullable=False)
    player_1_end_confirmation = db.Column(Boolean, default=False, nullable=False)

    player_2_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
    player_2_points = db.Column(db.Integer, nullable=False)
    player_2_end_confirmation = db.Column(Boolean, default=False, nullable=False)

    winner_id = db.Column(db.ForeignKey('users.user_id'), nullable=True, default=None)
    is_over = db.Column(Boolean, default=False, nullable=False)

    figures = db.relationship('Figure', backref='games', lazy=True)
    moves = db.relationship('Move', backref='games', lazy=True)

    create_time = db.Column(db.DateTime, nullable=False, server_default=func.now())
    update_time = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


