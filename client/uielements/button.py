from typing import Callable, Tuple
from constants.constants import LIGHT_BLUE, RED, WHITE
import pygame


class Button():
    def __init__(self, position: 'Tuple[int, int]', size: 'Tuple[int, int]',
                 label: str, canvas: 'pygame.Surface', action: 'Callable[[], None]'):
        self.CANVAS = canvas
        self.action = action
        self.is_active = False
        self.is_pressed = False
        self.active_color = LIGHT_BLUE
        self.def_color = RED
        self.text_color = WHITE
        # Background
        self.bckg_rect = pygame.Rect(position, size)
        # Label
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.text_surface = self.font.render(label, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(
            center=self.bckg_rect.center)

    def draw(self):
        rect_color = self.active_color if self.is_active else self.def_color
        pygame.draw.rect(self.CANVAS, rect_color,
                         self.bckg_rect, border_radius=4)
        self.CANVAS.blit(self.text_surface, self.text_rect)

    def event(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.bckg_rect.collidepoint(mouse_pos):
            self.is_active = True
            if pygame.mouse.get_pressed()[0]:
                self.is_pressed = True
            elif self.is_pressed == True:
                self.is_pressed = False
                self.action()
        else:
            self.is_active = False
