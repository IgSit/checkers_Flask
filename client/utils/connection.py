from typing import Any, Tuple
from utils.auth import Auth
import requests
from urllib.parse import urljoin


class Connection():
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.AUTH = Auth(base_url, self.create_url)

    def refresh_rooms(self) -> 'Tuple[bool, Any, str]':
        try: 
            url = self.create_url("rooms")
            res = requests.post(url, json=self.AUTH.header)
            res_body = res.json()
            if res.ok:
                return True, res_body['data'], res_body['message']
            else:
                return False, None, res_body['message']
        except:
            print("connection issues")
            return False, None, "Connection issues."

    def create_room(self) -> 'Tuple[bool, Any, str]':
        try: 
            url = self.create_url("create-room")
            res = requests.post(url, json=self.AUTH.header)
            res_body = res.json()
            if res.ok:
                return True, res_body['data'], ""
            else:
                return False, None, res_body['message']
        except:
            print("connection issues")
            return False, None, "Connection issues."

    def show_room(self, room_id: int) -> 'Tuple[bool, Any, str]':
        try: 
            url = self.create_url("show-room")
            req = self.AUTH.header.copy()
            req['room_id'] = room_id
            res = requests.post(url, json=req)
            res_body = res.json()
            if res.ok:
                return True, res_body['data'], res_body['message']
            else:
                return False, None, res_body['message']
        except:
            print("connection issues")
            return False, None, "Connection issues."

    def manage_places(self, room_id: int) -> 'Tuple[bool, str]':
        try: 
            url = self.create_url("manage-places")
            req = self.AUTH.header.copy()
            req['room_id'] = room_id
            res = requests.post(url, json=req)
            res_body = res.json()
            if res.ok:
                return True, res_body['message']
            else:
                return False, res_body['message']
        except:
            print("connection issues")
            return False, "Connection issues."

    def start_game(self):
        try: 
            url = self.create_url("start-game")
            req = self.AUTH.header.copy()
            res = requests.post(url, json=req)
            res_body = res.json()
            if res.ok:
                return True, res_body['message']
            else:
                return False, res_body['message']
        except:
            print("connection issues")
            return False, "Connection issues."

    def move(self, row: int, column: int, figure_id: str) -> 'Tuple[bool, str]':
        try: 
            url = self.create_url("move")
            req = self.AUTH.header.copy()
            req['row'] = row
            req['column'] = column
            req['figure_id'] = figure_id
            print("Send...")
            res = requests.post(url, json=req)
            print("Received...")
            res_body = res.json()
            print(res_body)
            if res.ok:
                return True, res_body['message']
            else:
                return False, res_body['message']
        except:
            print("connection issues")
            return False, "Connection issues."

    def end_game(self, room_id: int) -> 'Tuple[bool, str]':
        try: 
            url = self.create_url("end-game")
            req = self.AUTH.header.copy()
            req['room_id'] = room_id
            res = requests.post(url, json=req)
            res_body = res.json()
            if res.ok:
                return True, res_body['message']
            else:
                return False, res_body['message']
        except:
            print("connection issues")
            return False, "Connection issues."

    def rankings(self) -> 'Tuple[bool, Any, str]':
        try: 
            url = self.create_url("rankings")
            req = self.AUTH.header.copy()
            res = requests.post(url, json=req)
            res_body = res.json()
            if res.ok:
                return True, res_body['data'], res_body['message']
            else:
                return False, None, res_body['message']
        except:
            print("connection issues")
            return False, None, "Connection issues."

    def create_url(self, relative_url: str) -> str:
        return urljoin(self.base_url, relative_url)