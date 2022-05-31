from flask import request
from datetime import datetime, timedelta
import random

from db import db
import utils

from models.figures import Figure
from models.games import Game
from models.moves import Move
from models.rankings import Ranking
from models.rooms import Room
from models.sessions import Session
from models.users import User

from validators import account_validator

max_rooms_amount = 10


def rooms():
    if request.method == 'POST':
        json_data = request.get_json()
        print(json_data)
        response, status_code = utils.is_authenticated(json_data, False)

        if status_code != 200:
            return response, status_code

        rooms = db.session.query(Room).all()
        user_ids_dict = {}

        for room in rooms:
            if room.player_1_id is not None:
                user_ids_dict[room.player_1_id] = ''
            if room.player_2_id is not None:
                user_ids_dict[room.player_2_id] = ''

        user_ids = list(user_ids_dict.keys())

        users = db.session.query(User).filter(User.user_id.in_(user_ids)).all()

        users_dict = {}

        for user in users:
            users_dict[user.user_id] = {'username': user.username}

        rooms_dict = {}

        for room in rooms:
            rooms_dict[room.room_id] = {'room_id': room.room_id,
                                        'player_1_id': room.player_1_id,
                                        'player_1': users_dict[room.player_1_id][
                                            'username'] if room.player_1_id is not None else None,
                                        'player_1_accepted': room.player_1_accepted,
                                        'player_2_id': room.player_2_id,
                                        'player_2': users_dict[room.player_2_id][
                                            'username'] if room.player_2_id is not None else None,
                                        'player_2_accepted': room.player_2_accepted,
                                        'current_game': room.current_game,
                                        # 'all_games': [{"game_id": game.game_id,
                                        #                "room_id": game.room_id,
                                        #                "type": game.type,
                                        #                "size": game.size,
                                        #                "player_1_id": game.player_1_id,
                                        #                "player_1_points": game.player_1_points,
                                        #                "player_2_id": game.player_2_id,
                                        #                "player_2_points": game.player_2_points,
                                        #                "winner_id": game.winner_id,
                                        #                "is_over": game.is_over,
                                        #                "figures": {str(figure.figure_id): {
                                        #                    "figure_id": figure.figure_id,
                                        #                    "game_id": figure.game_id,
                                        #                    "player_id": figure.player_id,
                                        #                    "row": figure.row,
                                        #                    "column": figure.column,
                                        #                    "type": figure.type,
                                        #                    "is_killed": figure.is_killed
                                        #                } for figure in game.figures},
                                        #                "moves": game.moves,
                                        #                "create_time": game.create_time,
                                        #                "update_time": game.update_time
                                        #                } for game in room.all_games]
                                        }
        response['data'] = rooms_dict

        return response, status_code

    else:
        return {'message': 'Bad request. '}, 400


def create_room():
    if request.method == 'POST':
        json_data = request.get_json()
        response, status_code = utils.is_authenticated(json_data, False)

        if status_code != 200:
            return response, status_code

        rooms = db.session.query(Room).all()

        if len(rooms) >= max_rooms_amount:
            response['message'] = 'Nie można utworzyć nowego pokoju, znajdź jakiś wolny. '
            status_code = 400
            return response, status_code

        room = Room(**{})
        db.session.add(room)
        db.session.commit()

        response['message'] = 'Pokój został utworzony. '
        response['data'] = {}
        response['data']['room_id'] = room.room_id
        status_code = 201

        return response, status_code

    else:
        return {'message': 'Bad request. '}, 400


def show_room():
    def game_data(game_id):
        current_game = db.session.query(Game).filter_by(game_id=game_id).first()

        current_game_dict = {
            "game_id": current_game.game_id,
            "room_id": current_game.room_id,
            "type": current_game.type,
            "size": current_game.size,
            "player_1_id": current_game.player_1_id,
            "player_1_points": current_game.player_1_points,
            "player_2_id": current_game.player_2_id,
            "player_2_points": current_game.player_2_points,
            "winner_id": current_game.winner_id,
            "is_over": current_game.is_over,
            "figures": {str(figure.figure_id): {
                "figure_id": figure.figure_id,
                "game_id": figure.game_id,
                "player_id": figure.player_id,
                "row": figure.row,
                "column": figure.column,
                "type": figure.type,
                "is_killed": figure.is_killed
            } for figure in current_game.figures},
            "moves": {str(move.move_id): {
                "move_id": move.move_id,
                "game_id": move.game_id,
                "figure_id": move.figure_id,
                "killed_figure_id": move.killed_figure_id,
                "from_row": move.from_row,
                "to_row": move.to_row,
                "from_column": move.from_column,
                "to_column": move.to_column,
                "create_time": move.create_time,
                "update_time": move.update_time
            } for move in current_game.moves
            }}
        return current_game_dict

    if request.method == 'POST':
        json_data = request.get_json()
        response, status_code = utils.is_authenticated(json_data, False)

        if status_code != 200:
            return response, status_code

        room_id = json_data['room_id'] if 'room_id' in json_data else None

        if room_id is None or not isinstance(room_id, int):
            response['message'] = 'Ten pokój nie istnieje. '
            status_code = 400
            return response, status_code

        room = db.session.query(Room).filter_by(room_id=room_id).first()

        player_1 = db.session.query(User).filter_by(
            user_id=room.player_1_id).first() if room.player_1_id is not None else None
        player_2 = db.session.query(User).filter_by(
            user_id=room.player_2_id).first() if room.player_2_id is not None else None

        response['data'] = {'room_id': room.room_id,
                            'player_1': player_1.username if player_1 is not None else None,
                            'player_1_id': room.player_1_id,
                            'player_1_accepted': room.player_1_accepted,
                            'player_2': player_2.username if player_2 is not None else None,
                            'player_2_id': room.player_2_id,
                            'player_2_accepted': room.player_2_accepted,
                            'current_game': room.current_game,
                            # 'all_games': [{"game_id": game.game_id,
                            #                "room_id": game.room_id,
                            #                "type": game.type,
                            #                "size": game.size,
                            #                "player_1_id": game.player_1_id,
                            #                "player_1_points": game.player_1_points,
                            #                "player_2_id": game.player_2_id,
                            #                "player_2_points": game.player_2_points,
                            #                "winner_id": game.winner_id,
                            #                "is_over": game.is_over,
                            #                "figures": {str(figure.figure_id): {
                            #                    "figure_id": figure.figure_id,
                            #                    "game_id": figure.game_id,
                            #                    "player_id": figure.player_id,
                            #                    "row": figure.row,
                            #                    "column": figure.column,
                            #                    "type": figure.type,
                            #                    "is_killed": figure.is_killed
                            #                } for figure in game.figures},
                            #                "moves": game.moves,
                            #                "create_time": game.create_time,
                            #                "update_time": game.update_time
                            #                } for game in room.all_games],  # .__dict__
                            }

        if room.current_game is not None:
            response['data']['current_game_data'] = game_data(room.current_game)

        status_code = 200

        return response, status_code

    else:
        return {'message': 'Bad request. '}, 400


def manage_places():
    if request.method == 'POST':
        json_data = request.get_json()
        response, status_code = utils.is_authenticated(json_data, False)

        if status_code != 200:
            return response, status_code

        room_id = json_data['room_id'] if 'room_id' in json_data else None

        if room_id is None or not isinstance(room_id, int):
            response['message'] = 'Ten pokój nie istnieje. '
            status_code = 400
            return response, status_code

        room = db.session.query(Room).filter_by(room_id=room_id).first()

        if room.current_game is not None:
            response['message'] = 'W tym pokoju trwa gra, poczekaj aż się zakończy. '
            status_code = 400
            return response, status_code

        if room.player_1_id is None and room.player_2_id != json_data['user_id']:
            rooms_where_user_as_player_1 = db.session.query(Room).filter_by(player_1_id=json_data['user_id']).all()
            rooms_where_user_as_player_2 = db.session.query(Room).filter_by(player_2_id=json_data['user_id']).all()
            if len(rooms_where_user_as_player_1) == 0 and len(rooms_where_user_as_player_2) == 0:
                setattr(room, 'player_1_id', json_data['user_id'])
                db.session.commit()
                response['message'] = 'Zająłeś miejsce 1. '
                status_code = 201
                return response, status_code
            else:
                response['message'] = 'Zająłeś już miejsce w innym pokoju. '
                status_code = 400
                return response, status_code

        elif room.player_1_id == json_data['user_id']:
            setattr(room, 'player_1_id', None)
            setattr(room, 'player_1_accepted', False)
            setattr(room, 'player_2_accepted', False)
            db.session.commit()
            response['message'] = 'Zwolniłeś miejsce 1. '
            status_code = 201
            return response, status_code

        elif room.player_2_id is None:
            rooms_where_user_as_player_1 = db.session.query(Room).filter_by(player_1_id=json_data['user_id']).all()
            rooms_where_user_as_player_2 = db.session.query(Room).filter_by(player_2_id=json_data['user_id']).all()
            if len(rooms_where_user_as_player_1) == 0 and len(rooms_where_user_as_player_2) == 0:
                setattr(room, 'player_2_id', json_data['user_id'])
                db.session.commit()
                response['message'] = 'Zająłeś miejsce 2. '
                status_code = 201
                return response, status_code
            else:
                response['message'] = 'Zająłeś już miejsce w innym pokoju. '
                status_code = 400
                return response, status_code

        elif room.player_2_id == json_data['user_id']:
            setattr(room, 'player_2_id', None)
            setattr(room, 'player_1_accepted', False)
            setattr(room, 'player_2_accepted', False)
            db.session.commit()
            response['message'] = 'Zwolniłeś miejsce 2. '
            status_code = 201
            return response, status_code

        else:
            response['message'] = 'Ten pokój jest zajęty. '
            status_code = 200
            return response, status_code

    else:
        return {'message': 'Bad request. '}, 400
