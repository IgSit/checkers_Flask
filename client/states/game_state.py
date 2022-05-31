from typing import TYPE_CHECKING
import pygame

from constants.constants import WHITE

if TYPE_CHECKING:
    from game import Game


class GameState():
    def __init__(self, game: 'Game'):
        self.game = game
        self.loop_switch = False
        self.prev_state = None
        self.net_thread = None

    def loop(self):
        self.loop_switch = True
        while self.loop_switch:
            self.check_events()
            self.update()
            self.render()
        print("end of loop")

    def check_events(self):
        for event in pygame.event.get():
            self.quit_event(event)

    def update(self):
        self.game.CANVAS.fill(WHITE)

    def render(self):
        self.game.WINDOW.blit(self.game.CANVAS, (0, 0))
        pygame.display.flip()

    def enter_state(self, state: 'GameState'):
        self.game.state_stack.append(state)
        self.loop_switch = False

    def exit_state(self):
        self.game.state_stack.pop()
        self.loop_switch = False

    def quit_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.loop_switch = False
            self.game.is_running = False
