from typing import Callable
import requests


class Auth():
    def __init__(self, base_url: str, create_url: 'Callable[[str], str]') -> None:
        self.base_url = base_url
        self.default_values()
        self.create_url = create_url

    def sign_up(self, username: str, password: str, cpassword: str) -> bool:  # rejestracja
        req_body = {
            "username": username,
            "password": password,
            "confirm_password": cpassword
        }
        url = self.create_url("sign-up")
        res = requests.post(url, json=req_body)
        print(res.status_code)
        return res.ok

    def sign_in(self, username: str, password: str):  # logowanie
        try:
            req_body = {
                "username": username,
                "password": password,
            }
            url = self.create_url("sign-in")
            res = requests.post(url, json=req_body)
            res_body = res.json()
            if res_body['is_authenticated'] == True:
                self.set_values(True, username, res_body['data']['token'],
                                res_body['data']['session_id'], res_body['data']['user_id'])
                return True
        except:
            print("connection issues")
        return False

    def is_authenticated(self):
        pass

    def sign_out(self):
        try:
            req_body = {
                "session_id": self.session_id,
                "token": self.token,
                "user_id": self.user_id
            }
            url = self.create_url("sign-out")
            res = requests.post(url, json=req_body)
            self.default_values()
            return res.ok
        except:
            print("connection issues")
        return False

    def set_values(self, is_logged_in: bool, username: str,
                   token: str, session_id: int, user_id: int):
        self.is_logged_in = is_logged_in
        self.username = username
        self.session_id = session_id
        self.token = token
        self.user_id = user_id
        self.header = {
            "session_id": self.session_id,
            "token": self.token,
            "user_id": self.user_id
        }
        print(self.header)

    def default_values(self):
        self.set_values(False, "", "", -1, -1)
