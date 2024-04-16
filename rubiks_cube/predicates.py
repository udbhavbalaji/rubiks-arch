"""
This module contains predicate functions meant for handling logic in the rubiks cube architecure.

"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rubiks_cube.cube import RubiksCube, Face

def is_default_perspective(cube: RubiksCube) -> bool:
    """
    This function checks if the cube's orientation is the default perspective of the cube.
    Default perspective is as follows:
    
    1. Blue face in front
    2. White face on top
    3. Red face to the left
    
    Checking these will auto-fulfill the other face checks.

    Args:
        cube (RubiksCube): Rubiks Cube instance

    Returns:
        bool: returns if the cube instance is in default perspective

    """
    return is_blue_face_front(cube.current_front, cube.blue_face) and is_white_face_top(cube.current_front, cube.white_face) and is_red_face_left(cube.current_front, cube.red_face)


def is_blue_face_front(current_front: Face, blue_face: Face) -> bool:
    """
    This function compares the current front face with the blue face and checks to see if they're equal.
    Important to check if the cube's orientation is in the default perspective.

    Args:
        current_front (Face): cube's current front face instance
        blue_face (Face): cube's blue face

    Returns:
        bool: returns if the faces are equal (the same)

    """
    return current_front == blue_face

    
def is_white_face_top(current_front: Face, white_face: Face) -> bool:
    """
    This function compares the current top face with the white face and checks to see if they're equal.
    Important to check if the cube's orientation is in the default perspective.

    Args:
        current_front (Face): cube's current front face instance
        white_face (Face): cube's white face

    Returns:
        bool: returns if the faces are equal (the same)

    """
    return current_front.top == white_face


def is_red_face_left(current_front: Face, red_face: Face) -> bool:
    """
    This function compares the current left face with the red face and checks to see if they're equal.
    Important to check if the cube's orientation is in the default perspective.

    Args:
        current_front (Face): cube's current front face instance
        red_face (Face): cube's red face

    Returns:
        bool: returns if the faces are equal (the same)

    """
    return current_front.left == red_face
