from typing import Callable, Tuple
from constants.constants import PIECE_BLACK, PIECE_WHITE
import pygame


class Piece():
    def __init__(self, position: 'Tuple[int, int]', size: int, canvas: 'pygame.Surface',
                 action: 'Callable[[Tuple[int, int], Tuple[int, int], str], None]', figure_id: str) -> None:
        self.CANVAS = canvas
        self.action = action
        self.pos = position
        self.is_killed = True
        self.figure_id = figure_id
        self.SIZE = size
        self.color = PIECE_BLACK
        self.RADIUS = int(self.SIZE / 2 - self.SIZE / 8)
        self.bckg_rect = pygame.Rect(self.pos, (size, size))
        self.old_rect = pygame.Rect(self.pos, (size, size))
        self.is_active = False
        self.offset_x, self.offset_y = 0, 0

    def draw(self):
        if self.is_killed:
            return
        pygame.draw.circle(self.CANVAS, self.color,
                           self.bckg_rect.center, self.RADIUS)
        pygame.draw.circle(self.CANVAS, PIECE_WHITE if self.color == PIECE_BLACK else PIECE_BLACK,
                           self.bckg_rect.center, self.RADIUS, 1)

    def event(self, event: 'pygame.event.Event'):
        if self.is_killed:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.bckg_rect.collidepoint(event.pos):
                self.is_active = True
                self.old_rect = self.bckg_rect.copy()
                self.offset_x = self.bckg_rect.x - event.pos[0]
                self.offset_y = self.bckg_rect.y - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_active == True:
                self.action(self.old_rect.center, self.bckg_rect.center, self.figure_id)
                self.is_active = False
        elif event.type == pygame.MOUSEMOTION:
            if self.is_active:
                self.bckg_rect.x = event.pos[0] + self.offset_x
                self.bckg_rect.y = event.pos[1] + self.offset_y

    def set_pos(self, pos: 'Tuple[int, int]'):
        self.pos = pos
        self.bckg_rect.x = pos[0]
        self.bckg_rect.y = pos[1]

    def set(self, pos: 'Tuple[int, int]', color: Tuple[int, int, int], is_killed: bool):
        if self.is_active:
            self.old_rect.x = pos[0]
            self.old_rect.y = pos[1]
        else:
            self.set_pos(pos)
        self.color = color
        self.is_killed = is_killed

