import random
import json
import hashlib
from datetime import datetime, timedelta

with open('./../backend_config.json') as backend_config :
    backend_config = json.load(backend_config)

from db import db

from models.figures import Figure
from models.games import Game
from models.moves import Move
from models.rankings import Ranking
from models.rooms import Room
from models.sessions import Session
from models.users import User

characters = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'


def hash_password(password, password_salt) :
    password = hashlib.pbkdf2_hmac(
        'sha512',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        password_salt.encode('utf-8'),  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        100
    )
    return password.hex()[:80]


def is_authenticated(data, sign_out):
    session = db.session.query(Session).filter_by(session_id=data['session_id'] if 'session_id' in data else None).filter_by(
        user_id=data['user_id'] if 'user_id' in data else None).filter_by(token=data['token'] if 'token' in data else None).filter_by(signed_out_time=None).first()

    if session is None :
        return {'is_authenticated' : False, 'message' : 'Ta sesja jest nieprawidłowa. '}, 401

    now = datetime.now()

    if session.update_time + timedelta(days=backend_config['max_inactivity']) < now :
        return {'is_authenticated' : False, 'message' : 'Ta sesja wygasła. '}, 401

    setattr(session, 'update_time', now)

    if sign_out:
        setattr(session, 'signed_out_time', now)

    db.session.commit()

    return {'is_authenticated' : True, 'message' : 'Sesja jest zautoryzowana. '}, 200