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

start_positions = [(0, 0), (0, 2), (0, 4), (0, 6),
                   (1, 1), (1, 3), (1, 5), (1, 7),
                   (2, 0), (2, 2), (2, 4), (2, 6)]


def start_game():
    #########################################################
    def start():
        nonlocal json_data, room, response, status_code

        player_1_ranking = db.session.query(Ranking).filter_by(ranking_name=room.game_type).filter_by(
            user_id=room.player_1_id).first()
        player_2_ranking = db.session.query(Ranking).filter_by(ranking_name=room.game_type).filter_by(
            user_id=room.player_2_id).first()

        game = {'room_id': room.room_id,
                'type': room.game_type,
                'size': room.game_size,
                'player_1_id': room.player_1_id,
                'player_1_points': player_1_ranking.points,
                'player_2_id': room.player_2_id,
                'player_2_points': player_2_ranking.points}

        game = Game(**game)
        db.session.add(game)
        db.session.commit()

        setattr(room, 'current_game', game.game_id)
        db.session.commit()

        player_1_figures = [{'game_id': game.game_id,
                             'player_id': game.player_1_id,
                             'row': position[0],
                             'column': position[1]
                             } for position in start_positions]

        player_2_figures = [{'game_id': game.game_id,
                             'player_id': game.player_2_id,
                             'row': 7 - position[0],
                             'column': 7 - position[1]
                             } for position in start_positions]

        for figure in player_1_figures:
            figure = Figure(**figure)
            db.session.add(figure)
        for figure in player_2_figures:
            figure = Figure(**figure)
            db.session.add(figure)
        db.session.commit()

        response['message'] = 'Gra została rozpoczęta. '
        status_code = 201

        return response, status_code

    #

    if request.method == 'POST':
        json_data = request.get_json()
        response, status_code = utils.is_authenticated(json_data, False)

        if status_code != 200:
            return response, status_code

        room = db.session.query(Room).filter_by(player_1_id=json_data['user_id']).all()
        room.extend(db.session.query(Room).filter_by(player_2_id=json_data['user_id']).all())

        if len(room) != 1:
            response['message'] = 'Błąd! '
            status_code = 400
            return response, status_code

        room = room[0]

        if room.current_game is not None:
            response['message'] = 'W tym pokoju już trwa gra. '
            status_code = 400
            return response, status_code

        if room.player_1_id == json_data['user_id']:
            setattr(room, 'player_1_accepted', True)
            db.session.commit()

            if room.player_2_id is not None and room.player_2_accepted:
                return start()
            else:
                response['message'] = 'Zgłoszono chęć zaczęcia gry. '
                status_code = 201
                return response, status_code

        elif room.player_2_id == json_data['user_id']:
            setattr(room, 'player_2_accepted', True)
            db.session.commit()

            if room.player_1_id is not None and room.player_1_accepted:
                return start()
            else:
                response['message'] = 'Zgłoszono chęć zaczęcia gry. '
                status_code = 201
                return response, status_code

        else:
            response['message'] = 'Impossible case. '
            status_code = 400
            return response, status_code

    else:
        return {'message': 'Bad request. '}, 400


def move():
    if request.method == 'POST':
        json_data = request.get_json()
        response, status_code = utils.is_authenticated(json_data, False)

        if status_code != 200:
            return response, status_code

        figure = db.session.query(Figure).filter_by(figure_id=json_data['figure_id']).first()
        game = db.session.query(Game).filter_by(game_id=figure.game_id).first()

        def validate(row, column):
            nonlocal json_data, figure, game
            flag = True
            if flag:
                n_rows, n_columns = game.size.split('x')
                n_rows, n_columns = int(n_rows), int(n_columns)

                if figure.player_id != json_data['user_id']:
                    return False, 'Nie możesz ruszyć się nie swoją figurą. '

                latest_move = db.session.query(Move).filter_by(game_id=figure.game_id).order_by(Move.move_id.desc()).limit(1).first()
                latest_moved_figure = None
                if latest_move is not None:
                    latest_moved_figure = db.session.query(Figure).filter_by(figure_id=latest_move.figure_id).first()

                if (latest_move is None and json_data['user_id'] != game.player_1_id) or (latest_moved_figure is not None and latest_moved_figure.player_id == json_data['user_id']):
                    return False, 'Poczekaj na swoją kolej. '

                if figure.is_killed:
                    return False, 'Ta figura została już zbita. '

                if row < 0 or column < 0 or row >= n_rows or column >= n_columns:
                    return False, 'To pole jest poza mapą. '

                possible_figure = db.session.query(Figure).filter_by(game_id=figure.game_id).filter_by(row=row).filter_by(
                    column=column).filter_by(is_killed=False).first()

                if possible_figure is not None:
                    return False, 'To pole jest zajęte. '

                if figure.type == 'Pawn':
                    if abs(row - figure.row) == 1 and abs(column - figure.column) == 1:
                        return True, ''
                    elif abs(row - figure.row) == 2 and abs(column - figure.column) == 2:
                        figure_to_kill = db.session.query(Figure).filter_by(game_id=figure.game_id).filter_by(
                            row=(figure.row + row) // 2).filter_by(column=(figure.column + column) // 2).filter_by(is_killed=False).first()
                        if figure_to_kill is not None and figure_to_kill.player_id != figure.player_id:
                            return True, 'kill'
                        else:
                            return False, 'Ten ruch jest nieprawidłowy. '
                    else:
                        return False, 'Ten ruch jest niedozwolony. '
                elif figure.type == 'Queen':
                    return False, 'Królowych narazie nie obsługujemy. '
                else:
                    return False, 'Dziwna figura. '

            else:
                return True, ''

        def make_move(message, row, column):
            nonlocal json_data, figure, game

            killed_figure_id = None

            if message == 'kill':
                figure_to_kill = db.session.query(Figure).filter_by(game_id=figure.game_id).filter_by(
                    row=(figure.row + row) // 2).filter_by(column=(figure.column + column) // 2).filter_by(is_killed=False).first()
                setattr(figure_to_kill, 'is_killed', True)
                killed_figure_id = figure_to_kill.figure_id

            new_move = {
                "game_id": figure.game_id,
                "figure_id": figure.figure_id,
                "killed_figure_id": killed_figure_id,
                "from_row": figure.row,
                "to_row": row,
                "from_column": figure.column,
                "to_column": column,
            }
            new_move = Move(**new_move)
            db.session.add(new_move)

            setattr(figure, 'row', row)
            setattr(figure, 'column', column)

            player_1_figures = db.session.query(Figure).filter_by(game_id=figure.game_id).filter_by(player_id=game.player_1_id).filter_by(is_killed=False).all()
            player_2_figures = db.session.query(Figure).filter_by(game_id=figure.game_id).filter_by(player_id=game.player_2_id).filter_by(is_killed=False).all()

            if len(player_1_figures) == 0 or len(player_2_figures) == 0:
                setattr(game, 'is_over', True)
                setattr(game, 'winner_id', game.player_1_id if len(player_2_figures) == 0 else game.player_2_id)

            db.session.commit()

        can_move, message = validate(json_data['row'], json_data['column'])

        if can_move:
            make_move(message, json_data['row'], json_data['column'])

            response['message'] = 'Ruch został wykonany. '
            status_code = 201
            return response, status_code
        else:
            response['message'] = message
            status_code = 400
            return response, status_code




    else:
        return {'message': 'Bad request. '}, 400




def end_game():
    #########################################################
    def end():
        nonlocal json_data, room, game, response, status_code

        player_1_ranking = db.session.query(Ranking).filter_by(ranking_name=room.game_type).filter_by(
            user_id=room.player_1_id).first()
        player_2_ranking = db.session.query(Ranking).filter_by(ranking_name=room.game_type).filter_by(
            user_id=room.player_2_id).first()

        setattr(room, 'current_game', None)
        setattr(room, 'player_1_accepted', False)
        setattr(room, 'player_2_accepted', False)

        multiplier = 1 if game.winner_id == game.player_1_id else -1

        setattr(player_1_ranking, 'points', player_1_ranking.points + multiplier * 50)
        setattr(player_2_ranking, 'points', player_2_ranking.points - multiplier * 50)
        db.session.commit()

        response['message'] = 'Gra została zakończona. '
        status_code = 201

        return response, status_code

    #

    if request.method == 'POST':
        json_data = request.get_json()
        response, status_code = utils.is_authenticated(json_data, False)

        if status_code != 200:
            return response, status_code

        room = db.session.query(Room).filter_by(player_1_id=json_data['user_id']).all()
        room.extend(db.session.query(Room).filter_by(player_2_id=json_data['user_id']).all())

        if len(room) != 1:
            response['message'] = 'Błąd! '
            status_code = 400
            return response, status_code

        room = room[0]

        if room.current_game is None:
            response['message'] = 'W tym pokoju nie trwa żadna gra. '
            status_code = 400
            return response, status_code

        game = db.session.query(Game).filter_by(game_id=room.current_game).first()

        if not game.is_over:
            response['message'] = 'Gra nie może zakończyć się bez wygranego. '
            status_code = 400
            return response, status_code

        if room.player_1_id == json_data['user_id']:
            setattr(game, 'player_1_end_confirmation', True)
            db.session.commit()

            if room.player_2_id is None or game.player_2_end_confirmation:
                return end()
            else:
                response['message'] = 'Potwierdzono zakończenie gry. '
                status_code = 201
                return response, status_code

        elif room.player_2_id == json_data['user_id']:
            setattr(game, 'player_2_end_confirmation', True)
            db.session.commit()

            if room.player_1_id is None or game.player_1_end_confirmation:
                return end()
            else:
                response['message'] = 'Potwierdzono zakończenie gry. '
                status_code = 201
                return response, status_code

        else:
            response['message'] = 'Impossible case. '
            status_code = 400
            return response, status_code

    else:
        return {'message': 'Bad request. '}, 400
