"""
Jacob Dirkx 
CS 211 - 1/29/24
The game state and logic (model component) of 512, 
a game based on 2048 with a few changes. 
This is the 'model' part of the model-view-controller
construction plan.  It must NOT depend on any
particular view component, but it produces event 
notifications to trigger view updates. 
"""

from game_element import GameElement, GameEvent, EventKind
from typing import List, Tuple, Optional
import random

# Configuration constants
GRID_SIZE = 4

class Vec():
    """A Vec is an (x,y) or (row, column) pair that
    represents distance along two orthogonal axes.
    Interpreted as a position, a Vec represents
    distance from (0,0).  Interpreted as movement,
    it represents distance from another position.
    Thus we can add two Vecs to get a Vec.
    """
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y
    
    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.x+other.x, self.y+other.y)
    
    def __eq__(self, other: "Vec") -> bool:
        return(self.x==other.x and self.y==other.y)
    
    def __repr__(self):
        return f"Vec({self.x}, {self.y})"


class Tile(GameElement):
    """A slidy numbered thing."""

    def __init__(self, pos: Vec, value: int):
        super().__init__()
        self.row = pos.x
        self.col = pos.y
        self.value = value

    def __repr__(self):
        """Not like constructor --- more useful for debugging"""
        return f"Tile[{self.row},{self.col}]:{self.value}"

    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other: "Tile") -> bool:
        return self.value == other.value
    
    def move_to(self, new_pos: Vec):
        self.row = new_pos.x
        self.col = new_pos.y
        self.notify_all(GameEvent(EventKind.tile_updated, self))
    
    def merge(self, other: "Tile"):
        # This tile incorporates the value of the other tile
        self.value = self.value + other.value
        self.notify_all(GameEvent(EventKind.tile_updated, self))
        # The other tile has been absorbed.  Resistance was futile.
        other.notify_all(GameEvent(EventKind.tile_removed, other))


class Board(GameElement):
    """The game grid.  Inherits 'add_listener' and 'notify_all'
    methods from game_element.GameElement so that the game
    can be displayed graphically.
    """
    def __init__(self, rows=4, cols=4):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.tiles = [ ]
        for row in range(rows):
            row_tiles = [ ]
            for col in range(cols):
                row_tiles.append(None)
            self.tiles.append(row_tiles)

    def __getitem__(self, pos: Vec) -> Tile:
        return self.tiles[pos.x][pos.y] if self.in_bounds(pos) else None

    def __setitem__(self, pos: Vec, tile: Tile):
        self.tiles[pos.x][pos.y] = tile
        print(f"Tile set at {pos}: {tile}")

    def _empty_positions(self) -> list[Vec]:
        """Return a list of positions of None values,
        i.e., unoccupied spaces.
        """
        empties = []
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                if self.tiles[row][col] is None:
                    empties.append(Vec(row, col))
        return empties

    def has_empty(self) -> bool:
        """Is there at least one grid element without a tile?"""
        return bool(self._empty_positions()) 

    def place_tile(self, value=None):
        """Place a tile on a randomly chosen empty square."""
        empties = self._empty_positions()
        assert len(empties) > 0
        choice = random.choice(empties)
        row, col = choice.x, choice.y
        if value is None:
            # 0.1 probability of 4
            if random.random() < 0.1:
                value = 4
            else:
                value = 2
        new_tile = Tile(Vec(row, col), value)
        self.tiles[row][col] = new_tile
        self.notify_all(GameEvent(EventKind.tile_created, new_tile))

    def to_list(self) -> List[List[int]]:
        """Test scaffolding: represent each Tile by its
        integer value and empty positions as 0
        """
        result = []
        for row in range(self.rows):
            row_values = []
            for col in range(self.cols):
                tile = self[Vec(row, col)]
                if tile is None:
                    row_values.append(0)
                else:
                    row_values.append(tile.value)
            result.append(row_values)
        return result

    def from_list(self, values: List[List[int]]):
        """Test scaffolding: set board tiles to the
        given values, where 0 represents an empty space.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                value = values[row][col]
                if value != 0:
                    new_tile = Tile(Vec(row, col), value)
                    self[Vec(row, col)] = new_tile

    def in_bounds(self, pos: Vec) -> bool:
        """Is position (pos.x, pos.y) a legal position on the board?"""
        return bool(0 <= pos.x < len(range(self.rows)) and 0 <= pos.y < len(range(self.cols)))
    
    def _move_tile(self, old_pos: Vec, new_pos: Vec):
        tile1 = self[old_pos]
        tile1.move_to(new_pos)
        print(f"Tile moved: {tile1} from {old_pos} to {new_pos}")

    def slide(self, pos: Vec,  dir: Vec):
        """Slide tile at row,col (if any)
        in direction (dx,dy) until it bumps into
        another tile or the edge of the board.
        """
        if self[pos] is None:
            return
        print(f"Initial position: {pos}")
        print(f"Direction: {dir}")
        while self.in_bounds(pos):
            new_pos = pos + dir
            print(f"New position: {new_pos}")
            if not self.in_bounds(new_pos):
                break
            print(f"Before sliding: {self.to_list()}")
            if self[new_pos] is None:
                self._move_tile(pos, new_pos)
            elif self[pos] == self[new_pos]:
                self[pos].merge(self[new_pos])
                self._move_tile(pos, new_pos)
                break  # Stop moving when we merge with another tile
            else:
                # Stuck against another tile
                break
            print(f"After sliding: {self.to_list()}")
            pos = new_pos

            

    def score(self) -> int:
        """Calculate a score from the board.
        (Differs from classic 1024, which calculates score
        based on sequence of moves rather than state of
        board.
        """
        return 0
        #FIXME


