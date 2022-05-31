from typing import TYPE_CHECKING
import threading
from constants.constants import RED, WHITE
from states.game_state import GameState
from states.gameroom import GameRoom
from uielements.button import Button
from uielements.label import Label
from uielements.roomlist import RoomList
from utils.delta_time import DeltaTime

if TYPE_CHECKING:
    from game import Game


class RoomMenu(GameState):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.initialize_ui_elements()
        self.dt = DeltaTime()
        self.refresh_rate = 1000

    def loop(self):
        self.loop_switch = True
        self.net_thread = threading.Thread(target=self.fetch_roomlist)
        self.net_thread.start()
        super().loop()

    def check_events(self):
        self.return_btn.event()
        self.create_room_btn.event()
        self.roomlist.event()
        super().check_events()

    def update(self):
        self.game.CANVAS.fill(WHITE)
        self.roomlist.draw()
        self.return_btn.draw()
        self.create_room_btn.draw()
        self.warning_label.draw()

    def initialize_ui_elements(self):
        roomlist_pos = (self.game.SCREEN_WIDTH - 40,
                        self.game.SCREEN_HEIGHT - 100)
        self.roomlist = RoomList((20, 80), roomlist_pos,
                                 self.game.CANVAS, self.handle_roomlist)
        # Buttons
        self.return_btn = Button((20, 20), (200, 40), "< Return",
                                 self.game.CANVAS, self.handle_return_btn)
        self.create_room_btn = Button((240, 20), (200, 40), "Create new game",
                                      self.game.CANVAS, self.handle_create_room_btn)
        # Labels
        self.warning_label = Label((460, 30), (0, 40), "All warnings will be displayed here.",
                                   self.game.CANVAS, RED)

    def handle_create_room_btn(self):
        # self.enter_state(GameRoom(self.game, 0))
        ok, data, msg = self.game.CONNECTION.create_room()
        print(data)
        if ok:
            self.warning_label.set_label(msg)
            self.enter_state(GameRoom(self.game, data['room_id']))
        else:
            self.warning_label.set_label(msg)

    def handle_roomlist(self, room_id: int):
        ok, _, msg = self.game.CONNECTION.show_room(room_id)
        if ok:
            self.enter_state(GameRoom(self.game, room_id))
        else:
            self.warning_label.set_label(msg)

    def handle_return_btn(self):
        self.exit_state()

    def fetch_roomlist(self):
        while self.loop_switch:
            if self.dt.measure_dt(self.refresh_rate) == True:
                ok, data, msg = self.game.CONNECTION.refresh_rooms()
                if ok:
                    self.roomlist.set_data(data)
                else:
                    self.warning_label.set_label(msg)
