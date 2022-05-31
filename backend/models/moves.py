from sqlalchemy.sql import func

from db import db


class Move(db.Model) :
    __tablename__ = 'moves'

    move_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.ForeignKey('games.game_id'), nullable=False)
    figure_id = db.Column(db.ForeignKey('figures.figure_id'), nullable=False)

    killed_figure_id = db.Column(db.ForeignKey('figures.figure_id'), nullable=True)

    from_row = db.Column(db.Integer, nullable=False)
    to_row = db.Column(db.Integer, nullable=False)
    from_column = db.Column(db.Integer, nullable=False)
    to_column = db.Column(db.Integer, nullable=False)

    create_time = db.Column(db.DateTime, nullable=False, server_default=func.now())
    update_time = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
