from __future__ import annotations
from typing import TYPE_CHECKING
from rubiks_cube.errors import FaceTransferError

if TYPE_CHECKING:
    from rubiks_cube.cube import Face

def transfer_faces(orig: Face, new: Face) -> None:
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
