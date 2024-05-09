"""
This module contains the definitions of operations that can be performed on the rubiks cube. These operations have been
partitioned into rotations, inversions & shifts.

"""
from __future__ import annotations
from rubiks_cube.constants import Operations as ops
from typing import TYPE_CHECKING
from rubiks_cube.transformations import (
    RotateUp as ru, 
    RotateLeftVertical as rlv, 
    RightColUp as rcu, 
    LeftColUp as lcu, 
    TopRowLeft as trl, 
    BottomRowLeft as brl
    )
import rubiks_cube.helper as help

if TYPE_CHECKING:
    from rubiks_cube.models import RubiksCube

class Rotations:

    """
    This class contains rotation operation methods for a rubiks cube instance within the rubiks cube architecture.

    """
    
    @staticmethod
    def up(cube: RubiksCube) -> None:
        """
        This static method performs the operation of rotating the rubiks cube up.
        The operation is as follows: 

        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        # Getting transformed faces
        new_front_face = ru.front_face(cube.current_front)
        new_opposite_face = ru.opposite_face(cube.current_front)
        new_left_face = ru.left_face(cube.current_front)
        new_right_face = ru.right_face(cube.current_front)
        new_top_face = ru.top_face(cube.current_front)
        new_bottom_face = ru.bottom_face(cube.current_front)
        
        # Getting transformed grids
        new_front_grid = ru.front_grid(cube.current_front)
        new_opposite_grid = ru.opposite_grid(cube.current_front)
        new_left_grid = ru.left_grid(cube.current_front)
        new_right_grid = ru.right_grid(cube.current_front)
        new_top_grid = ru.top_grid(cube.current_front)
        new_bottom_grid = ru.bottom_grid(cube.current_front)

        # Setting updated grids
        new_front_face.grid = new_front_grid
        new_opposite_face.grid = new_opposite_grid
        new_left_face.grid = new_left_grid
        new_right_face.grid = new_right_grid
        new_top_face.grid = new_top_grid
        new_bottom_face.grid = new_bottom_grid
        
        # Resetting current front based on the rotation
        cube.current_front = cube.current_front.bottom

        # Transferring values from new face to the original face
        help.transfer_faces(cube.current_front, new_bottom_face)
        help.transfer_faces(cube.current_front.left, new_left_face)
        help.transfer_faces(cube.current_front.right, new_right_face)
        help.transfer_faces(cube.current_front.opposite, new_top_face)
        help.transfer_faces(cube.current_front.top, new_front_face)
        help.transfer_faces(cube.current_front.bottom, new_opposite_face)
    
    @staticmethod
    def left_vertical(cube: RubiksCube) -> None:
        """
        This static method performs the operation of rotating the rubiks cube left vertically.
        The operation is as follows: 

        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        # Getting transformed faces
        new_front_face = rlv.front_face(cube.current_front)
        new_opposite_face = rlv.opposite_face(cube.current_front)
        new_left_face = rlv.left_face(cube.current_front)
        new_right_face = rlv.right_face(cube.current_front)
        new_top_face = rlv.top_face(cube.current_front)
        new_bottom_face = rlv.bottom_face(cube.current_front)

        # Getting transformed grids
        new_front_grid = rlv.front_grid(cube.current_front)
        new_opposite_grid = rlv.opposite_grid(cube.current_front)
        new_left_grid = rlv.left_grid(cube.current_front)
        new_right_grid = rlv.right_grid(cube.current_front)
        new_top_grid = rlv.top_grid(cube.current_front)
        new_bottom_grid = rlv.bottom_grid(cube.current_front)

        # Setting updated grids
        new_front_face.grid = new_front_grid
        new_opposite_face.grid = new_opposite_grid
        new_left_face.grid = new_left_grid
        new_right_face.grid = new_right_grid
        new_top_face.grid = new_top_grid
        new_bottom_face.grid = new_bottom_grid
        
        # Resetting current front based on the rotation
        cube.current_front = cube.current_front.right

        # Transferring values from new face to the original face
        help.transfer_faces(cube.current_front, new_right_face)
        help.transfer_faces(cube.current_front.left, new_front_face)
        help.transfer_faces(cube.current_front.right, new_opposite_face)
        help.transfer_faces(cube.current_front.opposite, new_left_face)
        help.transfer_faces(cube.current_front.top, new_top_face)
        help.transfer_faces(cube.current_front.bottom, new_bottom_face)
    
    @staticmethod
    def down(cube: RubiksCube) -> None:
        """
        This static method performs the operation of rotating the rubiks cube down.
        Equivalent of rotating up 3 times.

        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        Rotations.up(cube)
        Rotations.up(cube)
        Rotations.up(cube)
    
    @staticmethod
    def right_vertical(cube: RubiksCube) -> None:
        """
        This static method performs the operation of rotating the rubiks cube right vertically.
        Equivalent to rotating left vertically 3 times.
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        Rotations.left_vertical(cube)
        Rotations.left_vertical(cube)
        Rotations.left_vertical(cube)
    
    @staticmethod
    def left_horizontal(cube: RubiksCube) -> None:
        """
        This static method performs the operation of rotating the rubiks cube left horizontally.
        
        Equivalent to the following operations:
        
        1. Right vertical
        2. Down
        3. Left vertical
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        Rotations.right_vertical(cube)
        Rotations.down(cube)
        Rotations.left_vertical(cube)
    
    @staticmethod
    def right_horizontal(cube: RubiksCube) -> None:
        """
        This static method performs the operation of rotating the rubiks cube right horizontally.
        
        Equivalent to the following operations:
        
        1. Left vertical
        2. Down
        3. Right vertical
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        Rotations.left_vertical(cube)
        Rotations.down(cube)
        Rotations.right_vertical(cube)

    rotations = {
        ops.ROTATE_UP: up,
        ops.ROTATE_DOWN: down,
        ops.ROTATE_LEFT_VERTICALLY: left_vertical,
        ops.ROTATE_LEFT_HORIZONTALLY: left_horizontal,
        ops.ROTATE_RIGHT_VERTICALLY: right_vertical,
        ops.ROTATE_RIGHT_HORIZONTALLY: right_horizontal
    }

    
class Inversions:
    
    """
    This class contains inversion operation methods for a rubiks cube instance within the rubiks cube architecture.

    """
    
    @staticmethod
    def horizontally(cube: RubiksCube) -> None:
        """
        This static method performs the operation of inverting the rubiks cube horizontally.
        
        Equivalent to rotating left horizontally 2 times.
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        Rotations.left_horizontal(cube)
        Rotations.left_horizontal(cube)
    
    @staticmethod
    def vertically(cube: RubiksCube) -> None:
        """
        This static method performs the operation of inverting the rubiks cube vertically.
        
        Equivalent to rotating left vertically 2 times.
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        Rotations.left_vertical(cube)
        Rotations.left_vertical(cube)

    inversions = {
        ops.INVERT_HORIZONTALLY: horizontally,
        ops.INVERT_VERTICALLY: vertically
    }
    
    
class Shifts:
    
    """
    This class contains shift operation methods for a rubiks cube instance within the rubiks cube architecture.

    """
    
    @staticmethod
    def right_col_up(cube: RubiksCube) -> None:
        """
        This static method performs the operation of shifting the rubiks cube's right column up.
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        # Getting updated grids for each face
        new_front_grid = rcu.front_grid(cube.current_front)
        new_opposite_grid = rcu.opposite_grid(cube.current_front)
        new_left_grid = rcu.left_grid(cube.current_front)
        new_right_grid = rcu.right_grid(cube.current_front)
        new_top_grid = rcu.top_grid(cube.current_front)
        new_bottom_grid = rcu.bottom_grid(cube.current_front)
        
        # Setting updated grids
        cube.current_front.grid = new_front_grid
        cube.current_front.opposite.grid = new_opposite_grid
        cube.current_front.left.grid = new_left_grid
        cube.current_front.right.grid = new_right_grid
        cube.current_front.top.grid = new_top_grid
        cube.current_front.bottom.grid = new_bottom_grid
    
    @staticmethod
    def left_col_up(cube: RubiksCube) -> None:
        """
        This static method performs the operation of shifting the rubiks cube's left column up.
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        # Getting updated grids for each face
        new_front_grid = lcu.front_grid(cube.current_front)
        new_opposite_grid = lcu.opposite_grid(cube.current_front)
        new_left_grid = lcu.left_grid(cube.current_front)
        new_right_grid = lcu.right_grid(cube.current_front)
        new_top_grid = lcu.top_grid(cube.current_front)
        new_bottom_grid = lcu.bottom_grid(cube.current_front)
        
        # Setting updated grids
        cube.current_front.grid = new_front_grid
        cube.current_front.opposite.grid = new_opposite_grid
        cube.current_front.left.grid = new_left_grid
        cube.current_front.right.grid = new_right_grid
        cube.current_front.top.grid = new_top_grid
        cube.current_front.bottom.grid = new_bottom_grid
    
    @staticmethod
    def top_row_left(cube: RubiksCube) -> None:
        """
        This static method performs the operation of shifting the rubiks cube's top row left.
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        # Getting updated grids for each face
        new_front_grid = trl.front_grid(cube.current_front)
        new_opposite_grid = trl.opposite_grid(cube.current_front)
        new_left_grid = trl.left_grid(cube.current_front)
        new_right_grid = trl.right_grid(cube.current_front)
        new_top_grid = trl.top_grid(cube.current_front)
        new_bottom_grid = trl.bottom_grid(cube.current_front)
        
        # Setting updated grids
        cube.current_front.grid = new_front_grid
        cube.current_front.opposite.grid = new_opposite_grid
        cube.current_front.left.grid = new_left_grid
        cube.current_front.right.grid = new_right_grid
        cube.current_front.top.grid = new_top_grid
        cube.current_front.bottom.grid = new_bottom_grid
    
    @staticmethod
    def bottom_row_left(cube: RubiksCube) -> None:
        """
        This static method performs the operation of shifting the rubiks cube's bottom row left.
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        # Getting updated grids for each face
        new_front_grid = brl.front_grid(cube.current_front)
        new_opposite_grid = brl.opposite_grid(cube.current_front)
        new_left_grid = brl.left_grid(cube.current_front)
        new_right_grid = brl.right_grid(cube.current_front)
        new_top_grid = brl.top_grid(cube.current_front)
        new_bottom_grid = brl.bottom_grid(cube.current_front)
        
        # Setting updated grids
        cube.current_front.grid = new_front_grid
        cube.current_front.opposite.grid = new_opposite_grid
        cube.current_front.left.grid = new_left_grid
        cube.current_front.right.grid = new_right_grid
        cube.current_front.top.grid = new_top_grid
        cube.current_front.bottom.grid = new_bottom_grid
    
    @staticmethod
    def right_col_down(cube: RubiksCube) -> None:
        """
        This static method performs the operation of shifting the rubiks cube's right column down.
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        Shifts.right_col_up(cube)
        Shifts.right_col_up(cube)
        Shifts.right_col_up(cube)
    
    @staticmethod
    def left_col_down(cube: RubiksCube) -> None:
        """
        This static method performs the operation of shifting the rubiks cube's left column down.
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        Shifts.left_col_up(cube)
        Shifts.left_col_up(cube)
        Shifts.left_col_up(cube)
    
    @staticmethod
    def top_row_right(cube: RubiksCube) -> None:
        """
        This static method performs the operation of shifting the rubiks cube's top row right.
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        Shifts.top_row_left(cube)
        Shifts.top_row_left(cube)
        Shifts.top_row_left(cube)
    
    @staticmethod
    def bottom_row_right(cube: RubiksCube) -> None:
        """
        This static method performs the operation of shifting the rubiks cube's bottom row right.
        
        Args:
            cube (RubiksCube): The rubiks cube instance on which the operation should be performed.

        """
        Shifts.bottom_row_left(cube)
        Shifts.bottom_row_left(cube)
        Shifts.bottom_row_left(cube)
        
    shifts = {
        ops.SHIFT_LEFT_COL_UP: left_col_up,
        ops.SHIFT_LEFT_COL_DOWN: left_col_down,
        ops.SHIFT_RIGHT_COL_UP: right_col_up,
        ops.SHIFT_RIGHT_COL_DOWN: right_col_down,
        ops.SHIFT_TOP_ROW_LEFT: top_row_left,
        ops.SHIFT_TOP_ROW_RIGHT: top_row_right,
        ops.SHIFT_BOTTOM_ROW_LEFT: bottom_row_left,
        ops.SHIFT_BOTTOM_ROW_RIGHT: bottom_row_right
    }