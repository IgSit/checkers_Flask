from typing import Any, Callable, Dict, List, Tuple
from constants.constants import BLACK, LIGHT_BLUE
import pygame

from uielements.label import Label
from uielements.roomelem import RoomElem


class RoomList():
    def __init__(self, position: 'Tuple[int, int]', size: 'Tuple[int, int]',
                 canvas: 'pygame.Surface', action: 'Callable[[int], None]'):
        self.CANVAS = canvas
        self.POS = position
        self.SIZE = size
        self.WIDTH, self.HEIGHT = size
        self.action = action
        self.data = []
        self.roomelems: List[RoomElem] = []
        self.labels: List[Label] = []
        self.initialize_ui()
        # Background
        self.bckg_rect = pygame.Rect(position, size)
        # Label
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.text_surface = self.font.render("a", True, LIGHT_BLUE)
        self.text_rect = self.text_surface.get_rect(
            center=self.bckg_rect.center)

    def draw(self):
        pygame.draw.rect(self.CANVAS, LIGHT_BLUE, self.bckg_rect, 2)
        for l in self.labels:
            l.draw()
        for i in range(len(self.data)):
            self.roomelems[i].draw()

    def event(self):
        for i in range(len(self.data)):
            self.roomelems[i].event()

    def initialize_ui(self):
        self.labels = [
            Label((self.POS[0] + 10, self.POS[1] + 10),
                  (20, 20), "Room ID:", self.CANVAS, BLACK),
            Label((self.POS[0] + 210, self.POS[1] + 10),
                  (20, 20), "Player 1:", self.CANVAS, BLACK),
            Label((self.POS[0] + 410, self.POS[1] + 10),
                  (20, 20), "Player 2:", self.CANVAS, BLACK),
            Label((self.POS[0] + 610, self.POS[1] + 10),
                  (20, 20), "Current Game:", self.CANVAS, BLACK)
        ]
        self.roomelems = [
            RoomElem((self.POS[0], self.POS[1] + 50 * i),
                     (self.SIZE[0], 40), self.CANVAS, lambda x: self.action(x))
            for i in range(1, 11)
        ]

    def set_data(self, data: 'Dict[str, Dict[str, Any]]'):
        self.data = list(data.values())
        for i, val in enumerate(self.data):
            self.roomelems[i].set_labels(val['room_id'],
                                         str(val['player_1']),
                                         str(val['player_2']),
                                         str(val['current_game']))
