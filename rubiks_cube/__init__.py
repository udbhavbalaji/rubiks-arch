"""
Package initialization file. This module creates a rubiks-cube object and all the menu options.
"""
from rubiks_cube.cube import RubiksCube
from rubiks_cube.constants import Operations

cube = RubiksCube()

menu_options= [
    'Rotate Cube',
    'Invert Cube',
    'Shift Cube',
    'Reset Cube Perspective',
    'Shuffle Cube',
    'Unshuffle Cube'
    ]

menu_options_funcs = [cube.rotate,cube.invert,cube.shift,cube.reset_perspective,cube.shuffle,cube.unshuffle]

rotate_options = [
    'Rotate Down',
    'Rotate Up',
    'Rotate Left Vertically',
    'Rotate Left Horizontally',
    'Rotate Right Vertically',
    'Rotate Right Horizontally'
    ]

rotate_options_params = [Operations.ROTATE_DOWN, Operations.ROTATE_UP, Operations.ROTATE_LEFT_VERTICALLY, Operations.ROTATE_LEFT_HORIZONTALLY, Operations.ROTATE_RIGHT_VERTICALLY, Operations.ROTATE_RIGHT_HORIZONTALLY]

invert_options = [
    'Invert Vertically',
    'Invert Horizontally'
    ]

invert_options_params = [Operations.INVERT_VERTICALLY, Operations.INVERT_HORIZONTALLY]

shift_options = [
    'Shift Right Column Up',
    'Shift Right Column Down',
    'Shift Left Column Up',
    'Shift Left Column Down',
    'Shift Top Row Left',
    'Shift Top Row Right',
    'Shift Bottom Row Left',
    'Shift Bottom Row Right'
    ]

shift_options_params = [Operations.SHIFT_RIGHT_COL_UP,Operations.SHIFT_RIGHT_COL_DOWN,Operations.SHIFT_LEFT_COL_UP,Operations.SHIFT_LEFT_COL_DOWN,Operations.SHIFT_TOP_ROW_LEFT,Operations.SHIFT_TOP_ROW_RIGHT,Operations.SHIFT_BOTTOM_ROW_LEFT,Operations.SHIFT_BOTTOM_ROW_RIGHT]

shuffle_options = [
    'Random Number of Operations',
    'Enter Number of Operations'
    ]