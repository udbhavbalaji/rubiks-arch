from enum import Enum, auto


class Colours(Enum):
    BLUE = 'Blue'
    RED = 'Red'
    ORANGE = 'Orange'
    WHITE = 'White'
    GREEN = 'Green'
    YELLOW = 'Yellow'

    
class Orientation(Enum):
    FRONT = auto()
    BACK = auto()
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()


class FacePositions:
    TOP_LEFT = (0, 0)
    TOP_CENTER = (0, 1)
    TOP_RIGHT = (0, 2)
    MID_LEFT = (1, 0)
    CENTER = (1, 1)
    MID_RIGHT = (1, 2)
    BOTTOM_LEFT = (2, 0)
    BOTTOM_CENTER = (2, 1)
    BOTTOM_RIGHT = (2, 2)

    TOP_ROW = 0
    BOTTOM_ROW = 2
    
    LEFT_COL = 0
    RIGHT_COL = 2

    
class PieceTypes(Enum):
    CENTER = auto()
    EDGE = auto()
    CORNER = auto()