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


def sign_in() :
    if request.method == 'POST' :
        json_data = request.get_json()
        user = db.session.query(User).filter_by(username=json_data['username']).first()

        if user is None or user.password != utils.hash_password(json_data['password'], user.password_salt) :
            return {'is_authenticated' : False, 'message' : 'Nazwa użytkownika lub hasło jest nieprawidłowe. '}, 400

        session = {'user_id' : user.user_id,
                   'token'   : ''.join(random.choice(utils.characters) for i in range(80))}
        session = Session(**session)
        db.session.add(session)
        db.session.commit()

        return {'is_authenticated' : True, 'message' : 'Zostałeś zalogowany pomyślnie. ',
                'data'             : {'session_id' : session.session_id,
                                      'token'      : session.token,
                                      'user_id'    : session.user_id}}, 201

    else :
        return {'message' : 'Bad request. '}, 400


def is_authenticated() :
    if request.method == 'POST' :
        json_data = request.get_json()
        return utils.is_authenticated(json_data, False)

    else :
        return {'message' : 'Bad request. '}, 400


def sign_out() :
    if request.method == 'POST' :
        json_data = request.get_json()
        response, status_code = utils.is_authenticated(json_data, True)

        if status_code != 200:
            return response, status_code

        return {'is_authenticated' : True, 'message' : 'Zostałeś wylogowany pomyślnie. '}, 200

    else :
        return {'message' : 'Bad request. '}, 400
