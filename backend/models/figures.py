from sqlalchemy.sql import func
from sqlalchemy import Boolean

from db import db


class Figure(db.Model) :
    __tablename__ = 'figures'

    figure_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.ForeignKey('games.game_id'), nullable=False)
    player_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)

    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum('Pawn', 'Queen'), server_default='Pawn', nullable=False)
    is_killed = db.Column(Boolean, default=False, nullable=True)  # if None then is killed

    _table_args_ = (
        db.UniqueConstraint('row', 'column', 'game_id', 'is_killed', name='the_same_position'),
    )