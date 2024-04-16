"""
This module contains helper functions that are used within the rubiks cube architecture.

"""
from __future__ import annotations
from typing import TYPE_CHECKING
from rubiks_cube.errors import FaceTransferError

if TYPE_CHECKING:
    from rubiks_cube.cube import Face

def transfer_faces(orig: Face, new: Face) -> None:
    """
    This function transfers the attribute values from one face to another. The primary objective is to preserve the 
    original face object but get the updated attribute values to keep track of the rubiks cube instance's current state.

    Args:
        orig (Face): Original face instance, where the values will be updated.
        new (Face): New face instance, from where the values will be transferred to the original face.

    Raises:
        FaceTransferError: Raised when either param isn't of type Face.
    """
    try:
        orig.left = new.left
        orig.right = new.right
        orig.top = new.top
        orig.bottom = new.bottom
        orig.front = new.front
        orig.back = new.back
        orig.side_of_cube = new.side_of_cube
        orig.grid = new.grid
    except AttributeError:
        raise FaceTransferError()
