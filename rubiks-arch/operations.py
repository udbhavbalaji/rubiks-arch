from constants import Operations as ops
from face_transformations import RotateUp as ru, RotateLeftVertical as rlv, RightColUp as rcu, LeftColUp as lcu, TopRowLeft as trl, BottomRowLeft as brl
import helper as help

class Rotations:
    
    # def up(current_front, internal_req=False):
    def up(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.ROTATE_UP)
            print('Rotating Up')
        # Getting transformed faces
        new_left_face = ru.left_face(cube.current_front)
        new_right_face = ru.right_face(cube.current_front)
        new_top_face = ru.top_face(cube.current_front)
        new_bottom_face = ru.bottom_face(cube.current_front)
        #########
        new_front_face = ru.front_face(cube.current_front)
        new_opposite_face = ru.opposite_face(cube.current_front)
        
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
    
    # def left_vertical(current_front, internal_req=False):
    def left_vertical(cube, internal_req=False):
        # TODO: change parameter to cube from face (front)
        if not internal_req:
            cube.op_stack.append(ops.ROTATE_LEFT_VERTICALLY)
            print('Rotating Left Vertically')
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
    
    def down(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.ROTATE_DOWN)
            print('Rotating Down')
        Rotations.up(cube, internal_req=True)
        Rotations.up(cube, internal_req=True)
        Rotations.up(cube, internal_req=True)
    
    def right_vertical(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.ROTATE_RIGHT_VERTICALLY)
            print('Rotating Right Vertically')
        Rotations.left_vertical(cube, internal_req=True)
        Rotations.left_vertical(cube, internal_req=True)
        Rotations.left_vertical(cube, internal_req=True)
    
    def left_horizontal(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.ROTATE_LEFT_HORIZONTALLY)
            print('Rotating Left Horizontally')
        Rotations.right_vertical(cube, internal_req=True)
        Rotations.down(cube, internal_req=True)
        Rotations.left_vertical(cube, internal_req=True)
    
    def right_horizontal(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.ROTATE_RIGHT_HORIZONTALLY)
            print('Rotating Right Horizontally')
        Rotations.left_vertical(cube, internal_req=True)
        Rotations.down(cube, internal_req=True)
        Rotations.right_vertical(cube, internal_req=True)

    
class Inversions:
    
    def horizontally(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.INVERT_HORIZONTALLY)
            print('Inverting Horizontally')
        Rotations.left_horizontal(cube, internal_req=True)
        Rotations.left_horizontal(cube, internal_req=True)
    
    def vertically(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.INVERT_VERTICALLY)
            print('Inverting Vertically')
        Rotations.left_vertical(cube, internal_req=True)
        Rotations.left_vertical(cube, internal_req=True)
    
    
class Shifts:
    
    def right_col_up(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.SHIFT_RIGHT_COL_UP)
            print('Shifting Right Column Up')
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
    
    def left_col_up(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.SHIFT_LEFT_COL_UP)
            print('Shifting Left Column Up')
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
    
    def top_row_left(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.TOP_ROW_LEFT)
            print('Shifting Top Row Left')
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
    
    def bottom_row_left(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.BOTTOM_ROW_LEFT)
            print('Shifting Bottom Row Left')
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
    
    def right_col_down(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.SHIFT_RIGHT_COL_DOWN)
            print('Shifting Right Column Down')
        Shifts.right_col_up(cube, internal_req=True)
        Shifts.right_col_up(cube, internal_req=True)
        Shifts.right_col_up(cube, internal_req=True)
    
    def left_col_down(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.SHIFT_LEFT_COL_DOWN)
            print('Shifting Left Column Down')
        Shifts.left_col_up(cube, internal_req=True)
        Shifts.left_col_up(cube, internal_req=True)
        Shifts.left_col_up(cube, internal_req=True)
    
    def top_row_right(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.TOP_ROW_RIGHT)
            print('Shifting Top Row Right')
        Shifts.top_row_left(cube, internal_req=True)
        Shifts.top_row_left(cube, internal_req=True)
        Shifts.top_row_left(cube, internal_req=True)
    
    def bottom_row_right(cube, internal_req=False):
        if not internal_req:
            cube.op_stack.append(ops.BOTTOM_ROW_RIGHT)
            print('Shifting Bottom Row Right')
        Shifts.bottom_row_left(cube, internal_req=True)
        Shifts.bottom_row_left(cube, internal_req=True)
        Shifts.bottom_row_left(cube, internal_req=True)
        