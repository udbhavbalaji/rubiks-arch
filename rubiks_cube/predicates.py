from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rubiks_cube.cube import RubiksCube, Face

def is_default_perspective(cube: RubiksCube) -> bool:
    return is_blue_face_front(cube.current_front, cube.blue_face) and is_white_face_top(cube.current_front, cube.white_face) and is_red_face_left(cube.current_front, cube.red_face)


def is_blue_face_front(current_front: Face, blue_face: Face) -> bool:
    return current_front == blue_face

    
def is_white_face_top(current_front: Face, white_face: Face) -> bool:
    return current_front.top == white_face


def is_red_face_left(current_front: Face, red_face: Face) -> bool:
    return current_front.left == red_face