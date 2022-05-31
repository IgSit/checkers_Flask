from sqlalchemy.sql import func
from sqlalchemy import Boolean

from db import db


class Room(db.Model) :
    __tablename__ = 'rooms'

    room_id = db.Column(db.Integer, primary_key=True)

    game_type = db.Column(db.Enum('Main'), server_default='Main')
    game_size = db.Column(db.Enum('8x8', '12x12', '16x16'), server_default='8x8', nullable=False)

    player_1_id = db.Column(db.ForeignKey('users.user_id'), nullable=True, default=None)
    player_1_accepted = db.Column(Boolean, default=False, nullable=False)

    player_2_id = db.Column(db.ForeignKey('users.user_id'), nullable=True, default=None)
    player_2_accepted = db.Column(Boolean, default=False, nullable=False)

    current_game = db.Column(db.Integer, nullable=True, default=None)
    all_games = db.relationship('Game', backref='rooms', lazy=True)

    create_time = db.Column(db.DateTime, nullable=False, server_default=func.now())
    update_time = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
