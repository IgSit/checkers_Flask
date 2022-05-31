from typing import Tuple
import pygame


class Label():
    def __init__(self, position: 'Tuple[int, int]', size: 'Tuple[int, int]',
                 label: str, canvas: 'pygame.Surface', text_color: 'Tuple[int, int, int]') -> None:
        self.text_color = text_color
        self.pos = position
        self.size = size
        self.label = label
        self.CANVAS = canvas
        # Label
        self.bckg_rect = pygame.Rect(position, size)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.text_surface = self.font.render(self.label, True, self.text_color)

    def draw(self):
        self.CANVAS.blit(self.text_surface, self.pos)

    def set_label(self, label: str):
        self.label = label
        self.text_surface = self.font.render(label, True, self.text_color)

    def set_color(self, text_color: 'Tuple[int, int, int]'):
        self.text_color = text_color
        self.text_surface = self.font.render(self.label, True, self.text_color)

    
