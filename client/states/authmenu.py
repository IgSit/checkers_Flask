from typing import TYPE_CHECKING

import pygame
from constants.constants import GREEN, RED, WHITE
from states.game_state import GameState
from uielements.button import Button
from uielements.label import Label
from uielements.text_field import TextField

if TYPE_CHECKING:
    from game import Game


class AuthMenu(GameState):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.inputs = {
            "sign_in_username": "",
            "sign_in_pass": "",
            "sign_up_username": "",
            "sign_up_pass": "",
            "sign_up_cpass": "",
        }
        self.initialize_ui()

    def check_events(self):
        self.sign_in_btn.event()
        self.sign_up_btn.event()
        self.return_btn.event()
        for event in pygame.event.get():
            self.quit_event(event)
            self.sign_in_username.event(event)
            self.sign_in_pass.event(event)
            self.sign_up_username.event(event)
            self.sign_up_pass.event(event)
            self.sign_up_cpass.event(event)

    def update(self):
        self.game.CANVAS.fill(WHITE)
        self.return_btn.draw()
        self.sign_in_username.draw()
        self.sign_in_pass.draw()
        self.sign_in_btn.draw()
        self.sign_up_username.draw()
        self.sign_up_pass.draw()
        self.sign_up_cpass.draw()
        self.sign_up_btn.draw()
        self.label.draw()

    def initialize_ui(self):
        self.return_btn = Button((50, 50), (200, 40), "< Return",
                                 self.game.CANVAS, self.handle_return_btn)
        self.sign_in_username = TextField((50, 150), (200, 40), "username",
                                          self.game.CANVAS, lambda x: self.handle_inputs(x, "sign_in_username"))
        self.sign_in_pass = TextField((50, 200), (200, 40), "password",
                                      self.game.CANVAS, lambda x: self.handle_inputs(x, "sign_in_pass"))
        self.sign_in_btn = Button((50, 250), (200, 40), "Sign in",
                                  self.game.CANVAS, self.handle_sign_in_button)
        self.sign_up_username = TextField((300, 100), (200, 40), "username",
                                          self.game.CANVAS, lambda x: self.handle_inputs(x, "sign_up_username"))
        self.sign_up_pass = TextField((300, 150), (200, 40), "password",
                                      self.game.CANVAS, lambda x: self.handle_inputs(x, "sign_up_pass"))
        self.sign_up_cpass = TextField((300, 200), (200, 40), "password",
                                       self.game.CANVAS, lambda x: self.handle_inputs(x, "sign_up_cpass"))
        self.sign_up_btn = Button((300, 250), (200, 40), "Sign up",
                                  self.game.CANVAS, self.handle_sign_up_button)
        self.label = Label((50, 300), (200, 40), "", self.game.CANVAS, RED)

    def handle_inputs(self, input_text: str, field: str):
        self.inputs[field] = input_text
        print(self.inputs)

    def handle_sign_in_button(self):
        if self.game.CONNECTION.AUTH.sign_in(self.inputs["sign_in_username"], self.inputs["sign_in_pass"]):
            self.exit_state()
        else:
            self.label.set_color(RED)
            self.label.set_label("Logowanie nie powiodło się")

    def handle_sign_up_button(self):
        if self.game.CONNECTION.AUTH.sign_up(self.inputs["sign_up_username"],
                                             self.inputs["sign_up_pass"], self.inputs["sign_up_cpass"]):
            self.label.set_color(GREEN)
            self.label.set_label("Rejestracja powiodła się")
        else:
            self.label.set_color(RED)
            self.label.set_label("Rejestracja nie powiodła się")

    def handle_return_btn(self):
        self.exit_state()
