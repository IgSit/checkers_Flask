from typing import Any, Callable, Dict, Tuple

import pygame

from constants.constants import BLACK, LIGHT_BLUE
from uielements.button import Button
from uielements.label import Label


class GameOptions():
    def __init__(self, position: 'Tuple[int, int]', size: 'Tuple[int, int]',
                 canvas: 'pygame.Surface', action_manage_places: 'Callable[[], None]',
                 action_start: 'Callable[[], None]', action_end: 'Callable[[], None]'):
        self.CANVAS = canvas
        self.POS = position
        self.SIZE = size
        self.WIDTH, self.HEIGHT = size
        self.is_playing = False
        self.is_over = False
        self.action_manage_places = action_manage_places
        self.action_start = action_start
        self.action_end = action_end
        self.data: 'Dict[str, Any]' = {}
        self.initialize_ui()
        self.bckg_rect = pygame.Rect(position, size)

    def draw(self):
        pygame.draw.rect(self.CANVAS, LIGHT_BLUE, self.bckg_rect, 2)
        self.player1_label.draw()
        self.player1_accept.draw()
        self.player2_label.draw()
        if not self.is_playing:
            self.start_game.draw()
        if self.is_over:
            self.end_game_btn.draw()
            self.game_result_label.draw()

    def event(self):
        self.player1_accept.event()
        if not self.is_playing:
            self.start_game.event()
        if self.is_over:
            self.end_game_btn.event()

    def initialize_ui(self):
        self.player1_label = Label(
            (self.POS[0] + 20, self.POS[1] + 40), (0, 40), "player1", self.CANVAS, BLACK)
        self.player2_label = Label(
            (self.POS[0] + 20, self.POS[1] + 80), (0, 40), "player2", self.CANVAS, BLACK)
        self.player1_accept = Button(
            (self.POS[0] + 20, self.POS[1] + 120), (200, 40), "Accept/Discard", self.CANVAS, self.action_manage_places)
        self.start_game = Button(
            (self.POS[0] + 20, self.POS[1] + 180), (200, 40), "Start Game", self.CANVAS, self.action_start)
        
        self.game_result_label = Label(
            (self.POS[0] + 20, self.POS[1] + 280), (0, 40), "", self.CANVAS, BLACK)
        self.end_game_btn = Button(
            (self.POS[0] + 20, self.POS[1] + 320), (200, 40), "End Game", self.CANVAS, self.action_end)

    def set_data(self, data: 'Dict[str, Any]'):
        self.data = data
        player1_acc = " | OK" if self.data['player_1_accepted'] else " | NO"
        player2_acc = " | OK" if self.data['player_2_accepted'] else " | NO"
        self.player1_label.set_label(str(self.data['player_1']) + player1_acc)
        self.player2_label.set_label(str(self.data['player_2']) + player2_acc)
        # set_is_playing
        self.is_playing = True if self.data['current_game'] != None else False
        if self.data['current_game']:
            self.is_over = self.data['current_game_data']['is_over']
        else:
            self.is_over = False

        if self.is_over == True:
            for key, value in self.data['current_game_data']['figures'].items():
                if value['player_id'] == data['player_1_id'] and not value['is_killed']:
                    self.game_result_label.set_label(f"Player {self.data['player_1']} won")
                    break
                if value['player_id'] == data['player_2_id'] and not value['is_killed']:
                    self.game_result_label.set_label(f"Player {self.data['player_2']} won")
                    break
                


