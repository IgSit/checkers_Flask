# pyright: reportImportCycles = false
from typing import List, TYPE_CHECKING
import pygame
import json
from states.mainmenu import MainMenu
from utils.connection import Connection
from utils.delta_time import DeltaTime
if TYPE_CHECKING:
    from states.game_state import GameState
with open('./../client_config.json') as client_config :
    client_config = json.load(client_config)
    baseURL = client_config['authorization_server']

class Game():
    def __init__(self) -> None:
        # Setup global game variables
        self.is_running = True
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
        self.state_stack: List['GameState'] = []
        self.deltatime = DeltaTime()
        self.CONNECTION = Connection(baseURL)
        # Pygame setup
        pygame.init()
        self.CANVAS = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.WINDOW = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Checkers")
        self.FONT = pygame.font.Font(pygame.font.get_default_font(), 20)
        # Load game
        self.load_states()

    def main_loop(self):
        while self.is_running:
            if (len(self.state_stack) > 0):
                self.state_stack[-1].loop()
            else:
                self.is_running = False

    def load_states(self):
        game_menu = MainMenu(self)
        self.state_stack.append(game_menu)

    def quit(self):
        for state in self.state_stack:
            if state.net_thread:
                state.net_thread.join()
        pygame.display.quit() # pygame bug, pygame.quit() not quiting display
        pygame.quit()
