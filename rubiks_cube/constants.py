from enum import Enum, auto


class Colours(Enum):
    BLUE: str = 'Blue'
    RED: str = 'Red'
    ORANGE: str = 'Orange'
    WHITE: str = 'White'
    GREEN: str = 'Green'
    YELLOW: str = 'Yellow'

    
class Orientation(Enum):
    FRONT = auto()
    BACK = auto()
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()


class FacePositions:
    TOP_LEFT: tuple[int, int] = (0, 0)
    TOP_CENTER: tuple[int, int] = (0, 1)
    TOP_RIGHT: tuple[int, int] = (0, 2)
    MID_LEFT: tuple[int, int] = (1, 0)
    CENTER: tuple[int, int] = (1, 1)
    MID_RIGHT: tuple[int, int] = (1, 2)
    BOTTOM_LEFT: tuple[int, int] = (2, 0)
    BOTTOM_CENTER: tuple[int, int] = (2, 1)
    BOTTOM_RIGHT: tuple[int, int] = (2, 2)

    TOP_ROW: int = 0
    BOTTOM_ROW: int = 2
    
    LEFT_COL: int = 0
    RIGHT_COL: int = 2

    
class PieceTypes(Enum):
    CENTER = auto()
    EDGE = auto()
    CORNER = auto()

    
class Operations(Enum):
    ROTATE_UP: str = 'Rotating Up'
    ROTATE_DOWN: str = 'Rotating Down'
    ROTATE_LEFT_VERTICALLY: str = 'Rotating Left Vertically'
    ROTATE_LEFT_HORIZONTALLY: str = 'Rotating Left Horizontally'
    ROTATE_RIGHT_VERTICALLY: str = 'Rotating Right Vertically'
    ROTATE_RIGHT_HORIZONTALLY: str = 'Rotating Right Horizontally'
    
    INVERT_VERTICALLY: str = 'Inverting Vertically'
    INVERT_HORIZONTALLY: str = 'Inverting Horizontally'
    
    SHIFT_RIGHT_COL_UP: str = 'Shifting Right Column Up'
    SHIFT_RIGHT_COL_DOWN: str = 'Shifting Right Column Down'
    SHIFT_LEFT_COL_UP: str = 'Shifting Left Column Up'
    SHIFT_LEFT_COL_DOWN: str = 'Shifting Left Column Down'
    SHIFT_TOP_ROW_LEFT: str = 'Shifting Top Row Left'
    SHIFT_TOP_ROW_RIGHT: str = 'Shifting Top Row Right'
    SHIFT_BOTTOM_ROW_LEFT: str = 'Shifting Bottom Row Left'
    SHIFT_BOTTOM_ROW_RIGHT: str = 'Shifting Bottom Row Right'
