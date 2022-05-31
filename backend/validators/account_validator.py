from db import db

from models.users import User


def sign_up(data):
    flag, message, validated_data = True, '', {}

    key = 'username'
    if key in data:
        user_exist = db.session.query(User).filter_by(username=data[key]).first()

        if user_exist is None:
            validated_data[key] = data[key]
        else:
            flag = False
            message += 'Ta nazwa użytkownika jest już zajęta. \n'
    else:
        flag = False
        message += 'Nazwa użytkownika jest wymagana. \n'

    key = 'password'
    if key in data :
        if 'confirm_' + key in data:
            if data[key] == data['confirm_' + key]:
                validated_data[key] = data[key]
            else :
                flag = False
                message += 'Podane hasła muszą być takie same. \n'
        else :
            flag = False
            message += 'Potwierdzenie hasła jest wymagane. \n'
    else :
        flag = False
        message += 'Hasło jest wymagane. \n'

    return flag, validated_data if flag else message
