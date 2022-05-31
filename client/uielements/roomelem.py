from typing import Callable, Tuple
import pygame
from constants.constants import BLACK, LIGHT_BLUE

from uielements.button import Button
from uielements.label import Label


class RoomElem():
    def __init__(self, position: 'Tuple[int, int]', size: 'Tuple[int, int]',
                 canvas: 'pygame.Surface', action: 'Callable[[int], None]'):
        self.CANVAS = canvas
        self.POS = position
        self.action = action
        self.is_active = False
        self.is_pressed = False
        self.room_id = -1
        # Background
        self.bckg_rect = pygame.Rect(position, size)
        self.initialize_ui()

    def event(self):
        self.join_btn.event()

    def draw(self):
        pygame.draw.rect(self.CANVAS, LIGHT_BLUE, self.bckg_rect, 2)
        self.room_id_label.draw()
        self.player_1_label.draw()
        self.player_2_label.draw()
        self.current_game_label.draw()
        self.join_btn.draw()

    def initialize_ui(self):
        self.room_id_label = Label((self.POS[0] + 10, self.POS[1] + 10),
                                   (20, 20), "#00000", self.CANVAS, BLACK)
        self.player_1_label = Label((self.POS[0] + 210, self.POS[1] + 10),
                                    (20, 20), "username1:", self.CANVAS, BLACK)
        self.player_2_label = Label((self.POS[0] + 410, self.POS[1] + 10),
                                    (20, 20), "username2:", self.CANVAS, BLACK)
        self.current_game_label = Label((self.POS[0] + 610, self.POS[1] + 10),
                                        (20, 20), "game", self.CANVAS, BLACK)
        self.join_btn = Button((self.POS[0] + 1010, self.POS[1] + 5),
                               (100, 30), "Join >", self.CANVAS, lambda: self.action(self.room_id))

    def set_labels(self, room_id: int, player_1: str, player_2: str, current_game: str):
        self.room_id = room_id
        self.room_id_label.set_label(str(room_id))
        self.player_1_label.set_label(player_1)
        self.player_2_label.set_label(player_2)
        self.current_game_label.set_label(current_game)
