
from face_transformations import RotateUp as ru, RotateLeftVertical as rlv, RightColUp as rcu, LeftColUp as lcu, TopRowLeft as trl, BottomRowLeft as brl
import helper as help

class Rotations:
    
    def up(current_front):
        # Getting transformed faces
        new_front_face = ru.front_face(current_front)
        new_opposite_face = ru.opposite_face(current_front)
        new_left_face = ru.left_face(current_front)
        new_right_face = ru.right_face(current_front)
        new_top_face = ru.top_face(current_front)
        new_bottom_face = ru.bottom_face(current_front)
        
        # Getting transformed grids
        new_front_grid = ru.front_grid(current_front)
        new_opposite_grid = ru.opposite_grid(current_front)
        new_left_grid = ru.left_grid(current_front)
        new_right_grid = ru.right_grid(current_front)
        new_top_grid = ru.top_grid(current_front)
        new_bottom_grid = ru.bottom_grid(current_front)

        # Setting updated grids
        new_front_face.grid = new_front_grid
        new_opposite_face.grid = new_opposite_grid
        new_left_face.grid = new_left_grid
        new_right_face.grid = new_right_grid
        new_top_face.grid = new_top_grid
        new_bottom_face.grid = new_bottom_grid
        
        # Resetting current front based on the rotation
        current_front = current_front.bottom

        # Transferring values from new face to the original face
        help.transfer_faces(current_front, new_bottom_face)
        help.transfer_faces(current_front.left, new_left_face)
        help.transfer_faces(current_front.right, new_right_face)
        help.transfer_faces(current_front.opposite, new_top_face)
        help.transfer_faces(current_front.top, new_front_face)
        help.transfer_faces(current_front.bottom, new_opposite_face)
    
    def left_vertical(current_front):
        # Getting transformed faces
        new_front_face = rlv.front_face(current_front)
        new_opposite_face = rlv.opposite_face(current_front)
        new_left_face = rlv.left_face(current_front)
        new_right_face = rlv.right_face(current_front)
        new_top_face = rlv.top_face(current_front)
        new_bottom_face = rlv.bottom_face(current_front)

        # Getting transformed grids
        new_front_grid = rlv.front_grid(current_front)
        new_opposite_grid = rlv.opposite_grid(current_front)
        new_left_grid = rlv.left_grid(current_front)
        new_right_grid = rlv.right_grid(current_front)
        new_top_grid = rlv.top_grid(current_front)
        new_bottom_grid = rlv.bottom_grid(current_front)

        # Setting updated grids
        new_front_face.grid = new_front_grid
        new_opposite_face.grid = new_opposite_grid
        new_left_face.grid = new_left_grid
        new_right_face.grid = new_right_grid
        new_top_face.grid = new_top_grid
        new_bottom_face.grid = new_bottom_grid
        
        # Resetting current front based on the rotation
        current_front = current_front.right

        # Transferring values from new face to the original face
        help.transfer_faces(current_front, new_right_face)
        help.transfer_faces(current_front.left, new_front_face)
        help.transfer_faces(current_front.right, new_opposite_face)
        help.transfer_faces(current_front.opposite, new_left_face)
        help.transfer_faces(current_front.top, new_top_face)
        help.transfer_faces(current_front.bottom, new_bottom_face)
    
    def down(current_front):
        Rotations.up(current_front)
        Rotations.up(current_front)
        Rotations.up(current_front)
    
    def right_vertical(current_front):
        Rotations.left_vertical(current_front)
        Rotations.left_vertical(current_front)
        Rotations.left_vertical(current_front)
    
    def left_horizontal(current_front):
        Rotations.right_vertical(current_front)
        Rotations.down(current_front)
        Rotations.left_vertical(current_front)
    
    def right_horizontal(current_front):
        Rotations.left_vertical(current_front)
        Rotations.down(current_front)
        Rotations.right_vertical(current_front)

    
class Inversions:
    
    def horizontally(current_front):
        Rotations.left_horizontal(current_front)
        Rotations.left_horizontal(current_front)
    
    def vertically(current_front):
        Rotations.left_vertical(current_front)
        Rotations.left_vertical(current_front)
    
    
class Shifts:
    
    def right_col_up(current_front):
        # Getting updated grids for each face
        new_front_grid = rcu.front_grid(current_front)
        new_opposite_grid = rcu.opposite_grid(current_front)
        new_left_grid = rcu.left_grid(current_front)
        new_right_grid = rcu.right_grid(current_front)
        new_top_grid = rcu.top_grid(current_front)
        new_bottom_grid = rcu.bottom_grid(current_front)
        
        # Setting updated grids
        current_front.grid = new_front_grid
        current_front.opposite.grid = new_opposite_grid
        current_front.left.grid = new_left_grid
        current_front.right.grid = new_right_grid
        current_front.top.grid = new_top_grid
        current_front.bottom.grid = new_bottom_grid
    
    def left_col_up(current_front):
        # Getting updated grids for each face
        new_front_grid = lcu.front_grid(current_front)
        new_opposite_grid = lcu.opposite_grid(current_front)
        new_left_grid = lcu.left_grid(current_front)
        new_right_grid = lcu.right_grid(current_front)
        new_top_grid = lcu.top_grid(current_front)
        new_bottom_grid = lcu.bottom_grid(current_front)
        
        # Setting updated grids
        current_front.grid = new_front_grid
        current_front.opposite.grid = new_opposite_grid
        current_front.left.grid = new_left_grid
        current_front.right.grid = new_right_grid
        current_front.top.grid = new_top_grid
        current_front.bottom.grid = new_bottom_grid
    
    def top_row_left(current_front):
        # Getting updated grids for each face
        new_front_grid = trl.front_grid(current_front)
        new_opposite_grid = trl.opposite_grid(current_front)
        new_left_grid = trl.left_grid(current_front)
        new_right_grid = trl.right_grid(current_front)
        new_top_grid = trl.top_grid(current_front)
        new_bottom_grid = trl.bottom_grid(current_front)
        
        # Setting updated grids
        current_front.grid = new_front_grid
        current_front.opposite.grid = new_opposite_grid
        current_front.left.grid = new_left_grid
        current_front.right.grid = new_right_grid
        current_front.top.grid = new_top_grid
        current_front.bottom.grid = new_bottom_grid
    
    def bottom_row_left(current_front):
        # Getting updated grids for each face
        new_front_grid = brl.front_grid(current_front)
        new_opposite_grid = brl.opposite_grid(current_front)
        new_left_grid = brl.left_grid(current_front)
        new_right_grid = brl.right_grid(current_front)
        new_top_grid = brl.top_grid(current_front)
        new_bottom_grid = brl.bottom_grid(current_front)
        
        # Setting updated grids
        current_front.grid = new_front_grid
        current_front.opposite.grid = new_opposite_grid
        current_front.left.grid = new_left_grid
        current_front.right.grid = new_right_grid
        current_front.top.grid = new_top_grid
        current_front.bottom.grid = new_bottom_grid
    
    def right_col_down(current_front):
        Shifts.right_col_up(current_front)
        Shifts.right_col_up(current_front)
        Shifts.right_col_up(current_front)
    
    def left_col_down(current_front):
        Shifts.left_col_up(current_front)
        Shifts.left_col_up(current_front)
        Shifts.left_col_up(current_front)
    
    def top_row_right(current_front):
        Shifts.top_row_left(current_front)
        Shifts.top_row_left(current_front)
        Shifts.top_row_left(current_front)
    
    def bottom_row_right(current_front):
        Shifts.bottom_row_left(current_front)
        Shifts.bottom_row_left(current_front)
        Shifts.bottom_row_left(current_front)
        