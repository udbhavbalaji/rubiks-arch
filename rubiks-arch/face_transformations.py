from constants import Orientation, FacePositions
import numpy as np


class RotateUp:
    
    def front_face(current_front):
        face = current_front.copy()
        old_face = current_front.copy()
        
        face.front = old_face.bottom
        face.back = old_face.top
        
        face.top = None
        face.bottom = None

        face.side_of_cube = Orientation.TOP
        
        return face

    def opposite_face(current_front):
        face = current_front.opposite.copy()
        old_face = face.copy()

        face.back = old_face.top
        face.front = old_face.bottom

        face.left = old_face.right
        face.right = old_face.left

        face.top = None
        face.bottom = None

        face.side_of_cube = Orientation.BOTTOM
        
        return face

    def left_face(current_front):
        face = current_front.left.copy()
        old_face = face.copy()

        face.top = old_face.right
        face.bottom = old_face.left

        face.left = old_face.top
        face.right = old_face.bottom

        return face
    
    def right_face(current_front):
        face = current_front.right.copy()
        old_face = face.copy()

        face.top = old_face.left
        face.bottom = old_face.right

        face.left = old_face.bottom
        face.right = old_face.top

        return face
    
    def top_face(current_front):
        face = current_front.top.copy()
        old_face = face.copy()

        face.top = old_face.front
        face.bottom = old_face.back

        face.left = old_face.right
        face.right = old_face.left

        face.front = None
        face.back = None

        face.side_of_cube = Orientation.BACK
        
        return face
    
    def bottom_face(current_front):
        face = current_front.bottom.copy()
        old_face = face.copy()

        face.top = old_face.front
        face.bottom = old_face.back

        face.front = None
        face.back = None

        face.side_of_cube = Orientation.FRONT
        
        return face

    def front_grid(current_front):
        front_face = current_front.copy()
        front_face.update_grid_attrs()
        return front_face.grid

    def opposite_grid(current_front):
        back_face = current_front.opposite.copy()
        old_face = back_face.copy()
        
        back_face.grid[FacePositions.TOP_LEFT] = old_face.grid[FacePositions.BOTTOM_RIGHT]
        back_face.grid[FacePositions.TOP_RIGHT] = old_face.grid[FacePositions.BOTTOM_LEFT]
        back_face.grid[FacePositions.BOTTOM_LEFT] = old_face.grid[FacePositions.TOP_RIGHT]
        back_face.grid[FacePositions.BOTTOM_RIGHT] = old_face.grid[FacePositions.TOP_LEFT]

        back_face.grid[FacePositions.TOP_CENTER] = old_face.grid[FacePositions.BOTTOM_CENTER]
        back_face.grid[FacePositions.MID_LEFT] = old_face.grid[FacePositions.MID_RIGHT]
        back_face.grid[FacePositions.MID_RIGHT] = old_face.grid[FacePositions.MID_LEFT]
        back_face.grid[FacePositions.BOTTOM_CENTER] = old_face.grid[FacePositions.TOP_CENTER]
        
        # TODO: Re-evaluate how, when and why piece attrs need to be updated
        back_face.update_grid_attrs()
        
        return back_face.grid
    
    def left_grid(current_front):
        left_face = current_front.left.copy()
        old_face = left_face.copy()

        left_face.grid[FacePositions.TOP_LEFT] = old_face.grid[FacePositions.TOP_RIGHT]
        left_face.grid[FacePositions.TOP_RIGHT] = old_face.grid[FacePositions.BOTTOM_RIGHT]
        left_face.grid[FacePositions.BOTTOM_LEFT] = old_face.grid[FacePositions.TOP_LEFT]
        left_face.grid[FacePositions.BOTTOM_RIGHT] = old_face.grid[FacePositions.BOTTOM_LEFT]

        left_face.grid[FacePositions.TOP_CENTER] = old_face.grid[FacePositions.MID_RIGHT]
        left_face.grid[FacePositions.MID_LEFT] = old_face.grid[FacePositions.TOP_CENTER]
        left_face.grid[FacePositions.MID_RIGHT] = old_face.grid[FacePositions.BOTTOM_CENTER]
        left_face.grid[FacePositions.BOTTOM_CENTER] = old_face.grid[FacePositions.MID_LEFT]

        left_face.update_grid_attrs()

        return left_face.grid
    
    def right_grid(current_front):
        right_face = current_front.right.copy()
        old_face = right_face.copy()

        right_face.grid[FacePositions.TOP_LEFT] = old_face.grid[FacePositions.BOTTOM_LEFT]
        right_face.grid[FacePositions.TOP_RIGHT] = old_face.grid[FacePositions.TOP_LEFT]
        right_face.grid[FacePositions.BOTTOM_LEFT] = old_face.grid[FacePositions.BOTTOM_RIGHT]
        right_face.grid[FacePositions.BOTTOM_RIGHT] = old_face.grid[FacePositions.TOP_RIGHT]

        right_face.grid[FacePositions.TOP_CENTER] = old_face.grid[FacePositions.MID_LEFT]
        right_face.grid[FacePositions.MID_LEFT] = old_face.grid[FacePositions.BOTTOM_CENTER]
        right_face.grid[FacePositions.MID_RIGHT] = old_face.grid[FacePositions.TOP_CENTER]
        right_face.grid[FacePositions.BOTTOM_CENTER] = old_face.grid[FacePositions.MID_RIGHT]

        right_face.update_grid_attrs()

        return right_face.grid
    
    def top_grid(current_front):
        top_face = current_front.top.copy()
        old_face = top_face.copy()

        top_face.grid[FacePositions.TOP_LEFT] = old_face.grid[FacePositions.BOTTOM_RIGHT]
        top_face.grid[FacePositions.TOP_RIGHT] = old_face.grid[FacePositions.BOTTOM_LEFT]
        top_face.grid[FacePositions.BOTTOM_LEFT] = old_face.grid[FacePositions.TOP_RIGHT]
        top_face.grid[FacePositions.BOTTOM_RIGHT] = old_face.grid[FacePositions.TOP_LEFT]

        top_face.grid[FacePositions.TOP_CENTER] = old_face.grid[FacePositions.BOTTOM_CENTER]
        top_face.grid[FacePositions.MID_LEFT] = old_face.grid[FacePositions.MID_RIGHT]
        top_face.grid[FacePositions.MID_RIGHT] = old_face.grid[FacePositions.MID_LEFT]
        top_face.grid[FacePositions.BOTTOM_CENTER] = old_face.grid[FacePositions.TOP_CENTER]

        top_face.update_grid_attrs()
        
        return top_face.grid
    
    def bottom_grid(current_front):
        bottom_face = current_front.bottom.copy()
        bottom_face.update_grid_attrs()
        return bottom_face.grid
        

class RotateLeftVertical:
    
    def front_face(current_front):
        face = current_front.copy()
        face.side_of_cube = Orientation.LEFT
        return face

    def opposite_face(current_front):
        face = current_front.opposite.copy()
        face.side_of_cube = Orientation.RIGHT
        return face

    def left_face(current_front):
        face = current_front.left.copy()
        face.side_of_cube = Orientation.BACK
        return face
    
    def right_face(current_front):
        face = current_front.right.copy()
        face.side_of_cube = Orientation.FRONT
        return face
    
    def top_face(current_front):
        face = current_front.top.copy()
        old_face = face.copy()
        
        face.left = old_face.front
        face.right = old_face.back
        
        face.front = old_face.right
        face.back = old_face.left
        
        return face
    
    def bottom_face(current_front):
        face = current_front.bottom.copy()
        old_face = face.copy()
        
        face.left = old_face.front
        face.right = old_face.back
        
        face.front = old_face.right
        face.back = old_face.left
        
        return face

    def front_grid(current_front):
        front_face = current_front.copy()
        front_face.update_grid_attrs()
        return front_face.grid
    
    def opposite_grid(current_front):
        opposite_face = current_front.opposite.copy()
        opposite_face.update_grid_attrs()
        return opposite_face.grid
    
    def left_grid(current_front):
        left_face = current_front.left.copy()
        left_face.update_grid_attrs()
        return left_face.grid
    
    def right_grid(current_front):
        right_face = current_front.right.copy()
        right_face.update_grid_attrs()
        return right_face.grid
    
    def top_grid(current_front):
        top_face = current_front.top.copy()
        old_face = top_face.copy()
        
        top_face.grid[FacePositions.TOP_LEFT] = old_face.grid[FacePositions.BOTTOM_LEFT]
        top_face.grid[FacePositions.TOP_RIGHT] = old_face.grid[FacePositions.TOP_LEFT]
        top_face.grid[FacePositions.BOTTOM_LEFT] = old_face.grid[FacePositions.BOTTOM_RIGHT]
        top_face.grid[FacePositions.BOTTOM_RIGHT] = old_face.grid[FacePositions.TOP_RIGHT]

        top_face.grid[FacePositions.TOP_CENTER] = old_face.grid[FacePositions.MID_LEFT]
        top_face.grid[FacePositions.MID_LEFT] = old_face.grid[FacePositions.BOTTOM_CENTER]
        top_face.grid[FacePositions.MID_RIGHT] = old_face.grid[FacePositions.TOP_CENTER]
        top_face.grid[FacePositions.BOTTOM_CENTER] = old_face.grid[FacePositions.MID_RIGHT]
        
        top_face.update_grid_attrs()
        
        return top_face.grid
    
    def bottom_grid(current_front):
        bottom_face = current_front.bottom.copy()
        old_face = bottom_face.copy()
        
        bottom_face.grid[FacePositions.TOP_LEFT] = old_face.grid[FacePositions.TOP_RIGHT]
        bottom_face.grid[FacePositions.TOP_RIGHT] = old_face.grid[FacePositions.BOTTOM_RIGHT]
        bottom_face.grid[FacePositions.BOTTOM_LEFT] = old_face.grid[FacePositions.TOP_LEFT]
        bottom_face.grid[FacePositions.BOTTOM_RIGHT] = old_face.grid[FacePositions.BOTTOM_LEFT]

        bottom_face.grid[FacePositions.TOP_CENTER] = old_face.grid[FacePositions.MID_RIGHT]
        bottom_face.grid[FacePositions.MID_LEFT] = old_face.grid[FacePositions.TOP_CENTER]
        bottom_face.grid[FacePositions.MID_RIGHT] = old_face.grid[FacePositions.BOTTOM_CENTER]
        bottom_face.grid[FacePositions.BOTTOM_CENTER] = old_face.grid[FacePositions.MID_LEFT]
        
        bottom_face.update_grid_attrs()
        
        return bottom_face.grid
        

class RightColUp:
    
    def front_grid(current_front):
        front_face = current_front.copy()
        old_face = front_face.copy()
        
        bottom_face = current_front.bottom.copy()
        
        bottom_right_col = bottom_face.grid[:, FacePositions.RIGHT_COL].copy()
        front_face.grid[:, FacePositions.RIGHT_COL] = bottom_right_col
        
        front_face.update_grid_attrs()
        
        return front_face.grid
    
    def opposite_grid(current_front):
        opposite_face = current_front.opposite.copy()
        old_face = opposite_face.copy()
        
        top_face = current_front.top.copy()
        
        top_right_col = top_face.grid[:, FacePositions.RIGHT_COL].copy()
        opposite_face.grid[:, FacePositions.LEFT_COL] = np.flip(top_right_col)
        
        opposite_face.update_grid_attrs()
        
        return opposite_face.grid
    
    def left_grid(current_front):
        return current_front.left.grid
    
    def right_grid(current_front):
        return RotateUp.right_grid(current_front)
        
    def top_grid(current_front):
        top_face = current_front.top.copy()
        
        front_face = current_front.copy()
        
        front_right_col = front_face.grid[:, FacePositions.RIGHT_COL].copy()
        top_face.grid[:, FacePositions.RIGHT_COL] = front_right_col
        
        top_face.update_grid_attrs()
        
        return top_face.grid
    
    def bottom_grid(current_front):
        bottom_face = current_front.bottom.copy()
        
        opposite_face = current_front.opposite.copy()
        
        opposite_left_col = opposite_face.grid[:, FacePositions.LEFT_COL].copy()
        bottom_face.grid[:, FacePositions.RIGHT_COL] = np.flip(opposite_left_col)
        
        bottom_face.update_grid_attrs()
        
        return bottom_face.grid
    
    
class LeftColUp:
    
    def front_grid(current_front):
        front_face = current_front.copy()
        
        bottom_face = current_front.bottom.copy()
        
        bottom_left_col = bottom_face.grid[:, FacePositions.LEFT_COL].copy()
        front_face.grid[:, FacePositions.LEFT_COL] = bottom_left_col
        
        front_face.update_grid_attrs()
        
        return front_face.grid
    
    def opposite_grid(current_front):
        opposite_face = current_front.opposite.copy()
        
        top_face = current_front.top.copy()
        
        top_left_col = top_face.grid[:, FacePositions.LEFT_COL].copy()
        opposite_face.grid[:, FacePositions.RIGHT_COL] = np.flip(top_left_col)
        
        opposite_face.update_grid_attrs()
        
        return opposite_face.grid
    
    def left_grid(current_front):
        return RotateUp.left_grid(current_front)
    
    def right_grid(current_front):
        return current_front.right.grid
    
    def top_grid(current_front):
        top_face = current_front.top.copy()
        
        front_face = current_front.copy()
        
        front_left_col = front_face.grid[:, FacePositions.LEFT_COL].copy()
        top_face.grid[:, FacePositions.LEFT_COL] = front_left_col
        
        top_face.update_grid_attrs()
        
        return top_face.grid
    
    def bottom_grid(current_front):
        bottom_face = current_front.bottom.copy()
        
        opposite_face = current_front.opposite.copy()
        
        opposite_right_col = opposite_face.grid[:, FacePositions.RIGHT_COL].copy()
        bottom_face.grid[:, FacePositions.LEFT_COL] = np.flip(opposite_right_col)
        
        bottom_face.update_grid_attrs()
        
        return bottom_face.grid


class TopRowLeft:
    
    def front_grid(current_front):
        front_face = current_front.copy()
        
        right_face = current_front.right.copy()
        
        right_top_row = right_face.grid[FacePositions.TOP_ROW].copy()
        front_face.grid[FacePositions.TOP_ROW] = right_top_row
        
        front_face.update_grid_attrs()
        
        return front_face.grid
    
    def opposite_grid(current_front):
        opposite_face = current_front.opposite.copy()
        
        left_face = current_front.left.copy()

        left_top_row = left_face.grid[FacePositions.TOP_ROW].copy()
        opposite_face.grid[FacePositions.TOP_ROW] = left_top_row
        
        opposite_face.update_grid_attrs()
        
        return opposite_face.grid
    
    def left_grid(current_front):
        left_face = current_front.left.copy()
        
        front_face = current_front.copy()
        
        front_top_row = front_face.grid[FacePositions.TOP_ROW].copy()
        left_face.grid[FacePositions.TOP_ROW] = front_top_row
        
        left_face.update_grid_attrs()
        
        return left_face.grid
    
    def right_grid(current_front):
        right_face = current_front.right.copy()
        
        opposite_face = current_front.opposite.copy()
        
        opposite_top_row = opposite_face.grid[FacePositions.TOP_ROW].copy()
        right_face.grid[FacePositions.TOP_ROW] = opposite_top_row
        
        right_face.update_grid_attrs()
        
        return right_face.grid
    
    def top_grid(current_front):
        return RotateLeftVertical.top_grid(current_front)
    
    def bottom_grid(current_front):
        return current_front.bottom.grid

        
class BottomRowLeft:
    
    def front_grid(current_front):
        front_face = current_front.copy()
        
        right_face = current_front.right.copy()
        
        right_bottom_row = right_face.grid[FacePositions.BOTTOM_ROW].copy()
        front_face.grid[FacePositions.BOTTOM_ROW] = right_bottom_row
        
        front_face.update_grid_attrs()
        
        return front_face.grid
    
    def opposite_grid(current_front):
        opposite_face = current_front.opposite.copy()
        
        left_face = current_front.left.copy()
        
        left_bottom_row = left_face.grid[FacePositions.BOTTOM_ROW].copy()
        opposite_face.grid[FacePositions.BOTTOM_ROW] = left_bottom_row
        
        opposite_face.update_grid_attrs()
        
        return opposite_face.grid
    
    def left_grid(current_front):
        left_face = current_front.left.copy()
        
        front_face = current_front.copy()
        
        front_bottom_row = front_face.grid[FacePositions.BOTTOM_ROW].copy()
        left_face.grid[FacePositions.BOTTOM_ROW] = front_bottom_row
        
        left_face.update_grid_attrs()
        
        return left_face.grid
    
    def right_grid(current_front):
        right_face = current_front.right.copy()
        
        opposite_face = current_front.opposite.copy()
        
        opposite_bottom_row = opposite_face.grid[FacePositions.BOTTOM_ROW].copy()
        right_face.grid[FacePositions.BOTTOM_ROW] = opposite_bottom_row
        
        right_face.update_grid_attrs()
        
        return right_face.grid
    
    def top_grid(current_front):
        return current_front.top.grid
    
    def bottom_grid(current_front):
        return RotateLeftVertical.bottom_grid(current_front)
        