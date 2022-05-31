from typing import TYPE_CHECKING
from constants.constants import BLACK
from states.authmenu import AuthMenu
from states.game_state import GameState
from uielements.button import Button
from uielements.label import Label

if TYPE_CHECKING:
    from game import Game


class Ranking(GameState):
    def __init__(self, game: 'Game') -> None:
        super().__init__(game)
        self.initialize_buttons()
        self.fetch_ranking()

    def update(self):
        super().update()
        self.return_btn.draw()
        self.title_label.draw()
        for l in self.ranking_labels:
            l.draw()

    def check_events(self):
        self.return_btn.event()
        super().check_events()

    def initialize_buttons(self):
        self.return_btn = Button((20, 20), (200, 40), "< Return",
                                 self.game.CANVAS, self.handle_return_btn)
        self.title_label = Label(
            (600, 30), (0, 40), "RANKING", self.game.CANVAS, BLACK)
        self.ranking_labels = [Label(
            (20, 80 + i* 40), (0, 0), "", self.game.CANVAS, BLACK) for i in range(5)]

    def handle_return_btn(self):
        self.exit_state()

    def fetch_ranking(self):
        ok, data, msg = self.game.CONNECTION.rankings()
        if ok:
            ranks = list(data['Main'].values())
            print(ranks)
            ranks.sort(reverse=True, key=lambda x: int(x['points']))
            self.clear_labels()
            for i in range(min(5, len(ranks))):
                self.ranking_labels[i].set_label(
                    f"Player: {ranks[i]['username']} | Points: {ranks[i]['points']}")
        else:
            self.clear_labels()
            self.ranking_labels[0].set_label(msg)

    def clear_labels(self):
        for l in self.ranking_labels:
            l.set_label("")
