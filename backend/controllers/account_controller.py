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


def sign_up():
    if request.method == 'POST':
        json_data = request.get_json()
        flag, data = account_validator.sign_up(json_data)

        if not flag:
            return {'is_authenticated': False, 'message': data}, 400

        data['password_salt'] = ''.join(random.choice(utils.characters) for i in range(10))
        data['password'] = utils.hash_password(data['password'], data['password_salt'])

        user = User(**data)
        db.session.add(user)
        db.session.commit()

        main_ranking = {'user_id': user.user_id}

        main_ranking = Ranking(**main_ranking)
        db.session.add(main_ranking)
        db.session.commit()

        return {'is_authenticated': False, 'message': 'Konto zostało utworzone pomyślnie. '}, 200

    else:
        return {'message': 'Bad request. '}, 400


def account_data():
    if request.method == 'POST':
        json_data = request.get_json()
        response, status_code = utils.is_authenticated(json_data, False)

        if status_code != 200:
            return response, status_code

        user = db.session.query(User).filter_by(user_id=json_data['user_id']).first()
        rankings = db.session.query(Ranking).filter_by(user_id=json_data['user_id']).all()

        data = {'username': user.username,
                'rankings': [{
                    'ranking_name': ranking.ranking_name,
                    'points': ranking.points} for ranking in rankings]}

        response['data'] = data
        status_code = 200

        return response, status_code

    else:
        return {'message': 'Bad request. '}, 400


def rankings():
    if request.method == 'POST':
        json_data = request.get_json()
        response, status_code = utils.is_authenticated(json_data, False)

        if status_code != 200:
            return response, status_code

        users = db.session.query(User).all()
        rankings = db.session.query(Ranking).all()

        users_dict = {str(user.user_id): {'user_id': user.user_id, 'username': user.username} for user in users}

        rankings_dict = {ranking.ranking_name: {} for ranking in rankings}

        for ranking in rankings:
            rankings_dict[ranking.ranking_name][str(ranking.user_id)] = {'username': users_dict[str(ranking.user_id)]['username'], 'points': ranking.points, 'user_id': ranking.user_id}

        response['data'] = rankings_dict
        status_code = 200

        return response, status_code

    else:
        return {'message': 'Bad request. '}, 400
