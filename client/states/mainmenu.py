from typing import TYPE_CHECKING
from constants.constants import WHITE
from states.authmenu import AuthMenu
from states.game_state import GameState
from states.ranking import Ranking
from states.roommenu import RoomMenu
from uielements.button import Button

if TYPE_CHECKING:
    from game import Game


class MainMenu(GameState):
    def __init__(self, game: 'Game') -> None:
        super().__init__(game)
        self.napis = ""
        self.initialize_buttons()

    def check_events(self):
        # if self.game.AUTH.is_logged_in:
        self.start_btn.event()
        self.ranking_btn.event()
        if not self.game.CONNECTION.AUTH.is_logged_in:
            self.auth_btn.event()
        else:
            self.sign_out_btn.event()
        super().check_events()

    def update(self):
        self.game.CANVAS.fill(WHITE)
        # if self.game.AUTH.is_logged_in:
        self.start_btn.draw()
        self.ranking_btn.draw()
        if not self.game.CONNECTION.AUTH.is_logged_in:
            self.auth_btn.draw()
        else:
            self.sign_out_btn.draw()

    def initialize_buttons(self):
        self.start_btn = Button((50, 50), (200, 40), "Start Game",
                                   self.game.CANVAS, self.handle_btn_action)
        self.ranking_btn = Button((50, 100), (200, 40), "Rankings",
                                 self.game.CANVAS, self.handle_ranking_btn)
        self.auth_btn = Button((50, 150), (200, 40), "Sign in / Sign up",
                              self.game.CANVAS, self.handle_auth_btn)
        self.sign_out_btn = Button((50, 150), (200, 40), "Sign out",
                              self.game.CANVAS, self.handle_sign_out_btn)

    def handle_btn_action(self):
        self.enter_state(RoomMenu(self.game))

    def handle_ranking_btn(self):
        self.enter_state(Ranking(self.game))

    def handle_auth_btn(self):
        self.enter_state(AuthMenu(self.game))

    def handle_sign_out_btn(self):
        self.game.CONNECTION.AUTH.sign_out()
        

