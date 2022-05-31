from typing import Callable, Tuple
import pygame

from constants.constants import BLACK, GREY, LIGHT_BLUE, RED


class TextField():
    def __init__(self, position: 'Tuple[int, int]', size: 'Tuple[int, int]',
                 placeholder: str, canvas: 'pygame.Surface', action: 'Callable[[str], None]') -> None:
        self.CANVAS = canvas
        self.action = action
        self.placeholder = placeholder
        self.is_active = False
        self.input_text = ""
        self.action(self.input_text)
        self.MAX_LENGTH = 20
        self.font_size = 20
        self.text_pos = (position[0] + self.font_size / 2,
                         position[1] + size[1] / 2 - self.font_size / 2)
        self.def_color = LIGHT_BLUE
        self.active_color = RED
        self.text_color = BLACK
        self.placeholder_color = GREY
        # Background
        self.bckg_rect = pygame.Rect(position, size)
        # Label
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)

    def event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.bckg_rect.collidepoint(event.pos):
                self.is_active = True
            else:
                self.is_active = False
        if event.type == pygame.KEYDOWN and self.is_active == True:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif len(self.input_text) < self.MAX_LENGTH:
                self.input_text += event.unicode
            self.action(self.input_text)

    def draw(self):
        rect_color = self.active_color if self.is_active else self.def_color
        pygame.draw.rect(self.CANVAS, rect_color,
                         self.bckg_rect, 2, border_radius=4)
        if (len(self.input_text) > 0):
            text_surface = self.font.render(
                self.input_text, True, self.text_color)
        else:
            text_surface = self.font.render(
                self.placeholder, True, self.placeholder_color)
        self.CANVAS.blit(text_surface, self.text_pos)
