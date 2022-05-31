import threading
from typing import TYPE_CHECKING

import pygame
from constants.constants import RED
from states.game_state import GameState
from uielements.board import Board
from uielements.button import Button
from uielements.gameoptions import GameOptions
from uielements.label import Label
from utils.delta_time import DeltaTime
if TYPE_CHECKING:
    from game import Game


class GameRoom(GameState):
    def __init__(self, game: 'Game', room_id: int):
        super().__init__(game)
        self.initialize_ui_elements()
        self.dt = DeltaTime()
        self.room_id = room_id
        self.is_playing = False
        self.REFRESH_RATE = 500

    def loop(self):
        self.loop_switch = True
        self.net_thread = threading.Thread(target=self.fetch_data)
        self.net_thread.start()
        super().loop()

    def check_events(self):
        self.return_btn.event()
        self.options.event()
        for event in pygame.event.get():
            self.board.event(event)
            self.quit_event(event)

    def update(self):
        super().update()
        self.return_btn.draw()
        self.options.draw()
        self.board.draw()
        self.warning_label.draw()

    def initialize_ui_elements(self):
        self.board = Board((520, 20), 640, 8, self.game.CANVAS, self.handle_move)
        self.options = GameOptions((20, 80), (360, self.game.SCREEN_HEIGHT - 60 - 80),
                                   self.game.CANVAS, self.handle_manage_places, self.handle_start, self.handle_end)
        # Buttons
        self.return_btn = Button((20, 20), (200, 40), "< Return",
                                 self.game.CANVAS, self.handle_return_btn)
        self.warning_label = Label((20, self.game.SCREEN_HEIGHT - 40), (0, 40),
                                   "All warnings will be displayed here.", self.game.CANVAS, RED)

    def fetch_data(self):
        self.dt.measure = 0
        while self.loop_switch:
            if self.dt.measure_dt(self.REFRESH_RATE) == True:
                print(".", end="")
                ok, data, msg = self.game.CONNECTION.show_room(
                    self.room_id)
                if ok:
                    self.options.set_data(data)
                    if data['current_game']:
                        self.board.setup_pieces(data['current_game_data'], data['player_1_id'])
                    else:
                        self.board.setup_pieces(None, -1)
                else:
                    self.warning_label.set_label(msg)

    def handle_manage_places(self):
        ok, msg = self.game.CONNECTION.manage_places(self.room_id)
        if ok:
            self.warning_label.set_label(msg)
        else:
            self.warning_label.set_label(msg)

    def handle_start(self):
        ok, msg = self.game.CONNECTION.start_game()
        if ok:
            self.warning_label.set_label(msg)
        else:
            self.warning_label.set_label(msg)

    def handle_end(self):
        ok, msg = self.game.CONNECTION.end_game(self.room_id)
        if ok:
            self.warning_label.set_label(msg)
            self.board.delete_pieces()
        else:
            self.warning_label.set_label(msg)

    def handle_move(self, col, row, key) -> bool:
        ok, msg = self.game.CONNECTION.move(col, row, key)
        self.warning_label.set_label(msg)
        if ok:
            return True
        else:
            return False

    def handle_return_btn(self):
        self.exit_state()
