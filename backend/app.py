from flask import Flask
import json

from db import db

from controllers import account_controller
from controllers import session_controller
from controllers import room_controller
from controllers import game_controller

with open('./../backend_config.json') as backend_config :
    backend_config = json.load(backend_config)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + backend_config['database']['user'] + \
                                        ':' + backend_config['database']['password'] + \
                                        '@' + backend_config['database']['host'] + \
                                        '/' + backend_config['database']['name']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# reset database tables
if 'reset_database' in backend_config and backend_config['reset_database']:
    with app.app_context() :
        db.drop_all()
        db.create_all()
#

methods = ['GET', 'POST']

app.add_url_rule('/sign-up', 'sign_up', account_controller.sign_up, methods=methods)  #
app.add_url_rule('/account-data', 'account_data', account_controller.account_data, methods=methods)
app.add_url_rule('/rankings', 'rankings', account_controller.rankings, methods=methods)

app.add_url_rule('/sign-in', 'sign_in', session_controller.sign_in, methods=methods)  #
app.add_url_rule('/is-authenticated', 'is_authenticated', session_controller.is_authenticated, methods=methods)  #
app.add_url_rule('/sign-out', 'sign_out', session_controller.sign_out, methods=methods)  #

app.add_url_rule('/rooms', 'rooms', room_controller.rooms, methods=methods)  #
app.add_url_rule('/create-room', 'create_room', room_controller.create_room, methods=methods)  #
app.add_url_rule('/show-room', 'show_room', room_controller.show_room, methods=methods)  #
app.add_url_rule('/manage-places', 'manage_places', room_controller.manage_places, methods=methods)  #

app.add_url_rule('/start-game', 'start_game', game_controller.start_game, methods=methods)
app.add_url_rule('/move', 'move', game_controller.move, methods=methods)
app.add_url_rule('/end-game', 'end_game', game_controller.end_game, methods=methods)


if __name__ == '__main__' :
    app.run(host='0.0.0.0')



# curl -X POST -d '{"username": "1", "password": "1", "confirm_password": "1"}' -H 'Content-Type: application/json' "http://localhost:5000/sign-up"
# curl -X POST -d '{"username": "1", "password": "1"}' -H 'Content-Type: application/json' "http://localhost:5000/sign-in"
# curl -X POST -d '{"session_id": 1, "token": "831fDFcAqeIMk2P52yzkOdfQeq9TEZIR63l6uG18FZrpzLvn894UH12ZPSvVEIv77BLRYeE4gVGQQlUh", "user_id": 1}' -H 'Content-Type: application/json' "http://localhost:5000/is-authenticated"
# curl -X POST -d '{"session_id": 1, "token": "831fDFcAqeIMk2P52yzkOdfQeq9TEZIR63l6uG18FZrpzLvn894UH12ZPSvVEIv77BLRYeE4gVGQQlUh", "user_id": 1}' -H 'Content-Type: application/json' "http://localhost:5000/sign-out"
#
#
#
#


