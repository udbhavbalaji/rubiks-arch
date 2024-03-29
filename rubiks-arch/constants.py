from enum import Enum, auto


class Colours:
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
