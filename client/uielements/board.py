from typing import Any, Callable, Dict, List, Tuple
import pygame

from constants.constants import BOARD_BLACK, BOARD_WHITE, PIECE_BLACK, PIECE_WHITE
from uielements.piece import Piece


class Board:
    def __init__(self, position: 'Tuple[int, int]', size: int, rows: int,
                 canvas: 'pygame.Surface', action: 'Callable[[int, int, str], bool]'):
        self.CANVAS = canvas
        self.POS = position
        self.SIZE = size
        self.ROWS = rows
        self.SQ_SIZE = int(self.SIZE / self.ROWS)
        self.action = action
        self.is_playing = False

    def draw(self):
        self.draw_squares()
        self.draw_pieces()

    def draw_squares(self):
        pygame.draw.rect(self.CANVAS, BOARD_BLACK,
                         (self.POS[0], self.POS[1], self.SIZE, self.SIZE))
        for row in range(self.ROWS):
            for col in range(row % 2, self.ROWS, 2):
                pygame.draw.rect(self.CANVAS, BOARD_WHITE, (self.POS[0] + row*self.SQ_SIZE,
                                 self.POS[1] + col * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def draw_pieces(self):
        if not self.is_playing:
            return
        for piece in self.PIECES.values():
            piece.draw()

    def event(self, event: pygame.event.Event):
        if not self.is_playing:
            return
        for piece in self.PIECES.values():
            piece.event(event)

    def initialize_pieces(self, pieces: 'Dict[Any, Any]'):
        self.PIECES: Dict[str, Piece] = {}
        for key, value in pieces.items():
            row = value['row']
            column = value['column']
            pos = self.colrow_to_xy((column, row))
            self.PIECES[key] = Piece(
                pos, self.SQ_SIZE, self.CANVAS, self.move_piece, key)
        print(self.PIECES)

    def move_piece(self, old_pos: 'Tuple[int, int]', new_pos: 'Tuple[int, int]', key: str):
        print(key)
        colrow = self.xy_to_colrow(new_pos)
        if not (self.is_on_board(new_pos) and self.action(colrow[1], colrow[0], key)):
            colrow = self.xy_to_colrow(old_pos)
        self.PIECES[key].set_pos(self.colrow_to_xy(colrow))

    def xy_to_colrow(self, pos: 'Tuple[int, int]') -> 'Tuple[int, int]':
        offset_x = pos[0] - self.POS[0]
        offset_y = pos[1] - self.POS[1]
        print(offset_x, offset_y)
        return (offset_x // self.SQ_SIZE, offset_y // self.SQ_SIZE)

    def colrow_to_xy(self, colrow: 'Tuple[int, int]') -> 'Tuple[int, int]':
        col = self.POS[0] + colrow[0] * self.SQ_SIZE
        row = self.POS[1] + colrow[1] * self.SQ_SIZE
        return (col, row)

    def is_on_board(self, pos: 'Tuple[int, int]') -> bool:
        return False if (pos[0] < self.POS[0] or
                        pos[0] > self.POS[0] + self.SIZE or
                        pos[1] < self.POS[1] or
                        pos[1] > self.POS[1] + self.SIZE) else True

    def setup_pieces(self, data: Any, player_1_id: int):
        if data == None:
            self.is_playing = False
            return
        if self.is_playing == False:
            self.is_playing = True
            self.initialize_pieces(data['figures'])
        for key, value in data['figures'].items():
            row = value['row']
            column = value['column']
            is_killed = value['is_killed']
            # piece_type = value['type']
            player_id = value['player_id']
            color = PIECE_WHITE if player_id == player_1_id else PIECE_BLACK
            pos = self.colrow_to_xy((column, row))
            try:
                self.PIECES[str(key)].set(pos, color, is_killed)
            except:
                pass

    def delete_pieces(self):
        self.PIECES: Dict[str, Piece] = {}
