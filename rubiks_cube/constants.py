"""
This module defines the constants and enums used in the rubiks_cube package.

"""
from enum import Enum, auto


class Colours(Enum):
    """
    This class defines colour constants used within the rubiks cube architecture.

    Parent Class:
        Enum (class): Defines this class as an Enum
        
    """
    BLUE: str = 'Blue'
    RED: str = 'Red'
    ORANGE: str = 'Orange'
    WHITE: str = 'White'
    GREEN: str = 'Green'
    YELLOW: str = 'Yellow'

    
class Orientation(Enum):
    """
    This class defines cube orientation constants used within the rubiks cube architecture.

    Parent Class:
        Enum (class): Defines this class as an Enum
        
    """
    FRONT = auto()
    BACK = auto()
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()


class FacePositions:
    """
    This class defines the positional constants for pieces within a face's grid. Allows easier indexing of a face's grid.
        
    """
    TOP_LEFT = (0, 0)
    TOP_CENTER = (0, 1)
    TOP_RIGHT = (0, 2)
    MID_LEFT = (1, 0)
    CENTER = (1, 1)
    MID_RIGHT = (1, 2)
    BOTTOM_LEFT = (2, 0)
    BOTTOM_CENTER = (2, 1)
    BOTTOM_RIGHT = (2, 2)

    TOP_ROW: int = 0
    BOTTOM_ROW: int = 2
    
    LEFT_COL: int = 0
    RIGHT_COL: int = 2

    
class PieceTypes(Enum):
    """
    This class defines the piece type constants used within the rubiks cube architecture.

    Parent Class:
        Enum (class): Defines this class as an Enum
        
    """
    CENTER = auto()
    EDGE = auto()
    CORNER = auto()

    
class Operations(Enum):
    """
    This class defines the operation constants used to map to corresponding methods within the rubiks cube architecture.

    Parent Class:
        Enum (class): Defines this class as an Enum
        
    """
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
