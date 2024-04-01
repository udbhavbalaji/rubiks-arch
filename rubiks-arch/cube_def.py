from constants import Colours, Orientation, FacePositions, PieceTypes
from errors import ImmutableAttributeError
# from face_transformations import RotateUp as ru, RotateLeftVertical as rlv, RightColUp as rcu, LeftColUp as lcu, TopRowLeft as trl, BottomRowLeft as brl
from predicates import is_default_perspective, is_white_face_top
# import helper as help
from operations import Rotations as rotate, Inversions as invert, Shifts as shift

import numpy as np

FACE_ORDER = ['FRONT', 'LEFT', 'RIGHT', 'TOP', 'OPPOSITE', 'BOTTOM']


class RubiksCube:
    
    def __init__(self, blue_face=None, red_face=None, orange_face=None, white_face=None, green_face=None, yellow_face=None, is_copy=False) -> None:
        self.blue_face = blue_face
        self.red_face = red_face
        self.orange_face = orange_face
        self.white_face = white_face
        self.green_face = green_face
        self.yellow_face = yellow_face

        if not is_copy:
            self.define_cube()
        else:
            self.current_front = self.blue_face

    def __repr__(self):
        front = self.current_front
        
        front_grid = repr(front).split('\n')
        left_grid = repr(front.left).split('\n')
        right_grid = repr(front.right).split('\n')
        top_grid = repr(front.top).split('\n')
        opposite_grid = repr(front.opposite).split('\n')
        bottom_grid = repr(front.bottom).split('\n')

        output = f"     _______\n"
        output += (
            f"     !{left_grid[0]}|\n     !{left_grid[1]}|\n     !{left_grid[2]}|\n"
        )
        output += "------------------------\n"
        output += f"{front_grid[0]}|{bottom_grid[0]}|{opposite_grid[0]}|{top_grid[0]}|\n"
        output += f"{front_grid[1]}|{bottom_grid[1]}|{opposite_grid[1]}|{top_grid[1]}|\n"
        output += f"{front_grid[2]}|{bottom_grid[2]}|{opposite_grid[2]}|{top_grid[2]}|\n"
        output += "------------------------\n"
        output += (
            f"     !{right_grid[0]}|\n     !{right_grid[1]}|\n     !{right_grid[2]}|\n"
        )
        output += f"     -------"

        return output

    @property
    def faces(self):
        return [
            self.current_front,
            self.current_front.left,
            self.current_front.right,
            self.current_front.top,
            self.current_front.opposite,
            self.current_front.bottom
        ]

    def define_cube(self):
        # Creating the cube Face Objects
        self.blue_face = Face(Colours.BLUE)
        self.red_face = Face(Colours.RED)
        self.orange_face = Face(Colours.ORANGE)
        self.white_face = Face(Colours.WHITE)
        self.green_face = Face(Colours.GREEN)
        self.yellow_face = Face(Colours.YELLOW)

        # Setting the current front as blue
        self.current_front = self.blue_face

        # Joining the side faces
        self.blue_face.left = self.red_face
        self.blue_face.right = self.orange_face
        
        self.orange_face.left = self.blue_face
        self.orange_face.right = self.green_face
        
        self.green_face.left = self.orange_face
        self.green_face.right = self.red_face
        
        self.red_face.left = self.green_face
        self.red_face.right = self.blue_face

        # Joining the top face
        self.blue_face.top = self.white_face
        self.red_face.top = self.white_face
        self.green_face.top = self.white_face
        self.orange_face.top = self.white_face
        
        self.white_face.front = self.blue_face
        self.white_face.left = self.red_face
        self.white_face.right = self.orange_face
        self.white_face.back = self.green_face
        
        # Joining the bottom face
        self.blue_face.bottom = self.yellow_face
        self.red_face.bottom = self.yellow_face
        self.green_face.bottom = self.yellow_face
        self.orange_face.bottom = self.yellow_face
        
        self.yellow_face.front = self.blue_face
        self.yellow_face.left = self.red_face
        self.yellow_face.right = self.orange_face
        self.yellow_face.back = self.green_face
        
        # Connecting opposite faces
        self.blue_face.opposite = self.green_face
        self.green_face.opposite = self.blue_face

        self.red_face.opposite = self.orange_face
        self.orange_face.opposite = self.red_face
        
        self.white_face.opposite = self.yellow_face
        self.yellow_face.opposite = self.white_face

        # Setting face sides
        self.blue_face.side_of_cube = Orientation.FRONT
        self.red_face.side_of_cube = Orientation.LEFT
        self.orange_face.side_of_cube = Orientation.RIGHT
        self.white_face.side_of_cube = Orientation.TOP
        self.green_face.side_of_cube = Orientation.BACK
        self.yellow_face.side_of_cube = Orientation.BOTTOM

    def assign_complements(self):
        for face in self.faces:
            face.init_face_complements()

    def print_face_ids(self):
        for pos, face in zip(FACE_ORDER, self.faces):
            print(f'{pos}: {face._id}')
        
    # def rotate_up(self):
    #     # Getting transformed faces
    #     new_front_face = ru.front_face(self.current_front)
    #     new_opposite_face = ru.opposite_face(self.current_front)
    #     new_left_face = ru.left_face(self.current_front)
    #     new_right_face = ru.right_face(self.current_front)
    #     new_top_face = ru.top_face(self.current_front)
    #     new_bottom_face = ru.bottom_face(self.current_front)
        
    #     # Getting transformed grids
    #     new_front_grid = ru.front_grid(self.current_front)
    #     new_opposite_grid = ru.opposite_grid(self.current_front)
    #     new_left_grid = ru.left_grid(self.current_front)
    #     new_right_grid = ru.right_grid(self.current_front)
    #     new_top_grid = ru.top_grid(self.current_front)
    #     new_bottom_grid = ru.bottom_grid(self.current_front)

    #     # Setting updated grids
    #     new_front_face.grid = new_front_grid
    #     new_opposite_face.grid = new_opposite_grid
    #     new_left_face.grid = new_left_grid
    #     new_right_face.grid = new_right_grid
    #     new_top_face.grid = new_top_grid
    #     new_bottom_face.grid = new_bottom_grid
        
    #     # Resetting current front based on the rotation
    #     self.current_front = self.current_front.bottom

    #     # Transferring values from new face to the original face
    #     help.transfer_faces(self.current_front, new_bottom_face)
    #     help.transfer_faces(self.current_front.left, new_left_face)
    #     help.transfer_faces(self.current_front.right, new_right_face)
    #     help.transfer_faces(self.current_front.opposite, new_top_face)
    #     help.transfer_faces(self.current_front.top, new_front_face)
    #     help.transfer_faces(self.current_front.bottom, new_opposite_face)

    # def rotate_down(self):
    #     self.rotate_up()
    #     self.rotate_up()
    #     self.rotate_up()

    # def rotate_left_vertically(self):
    #     # Getting transformed faces
    #     new_front_face = rlv.front_face(self.current_front)
    #     new_opposite_face = rlv.opposite_face(self.current_front)
    #     new_left_face = rlv.left_face(self.current_front)
    #     new_right_face = rlv.right_face(self.current_front)
    #     new_top_face = rlv.top_face(self.current_front)
    #     new_bottom_face = rlv.bottom_face(self.current_front)

    #     # Getting transformed grids
    #     new_front_grid = rlv.front_grid(self.current_front)
    #     new_opposite_grid = rlv.opposite_grid(self.current_front)
    #     new_left_grid = rlv.left_grid(self.current_front)
    #     new_right_grid = rlv.right_grid(self.current_front)
    #     new_top_grid = rlv.top_grid(self.current_front)
    #     new_bottom_grid = rlv.bottom_grid(self.current_front)

    #     # Setting updated grids
    #     new_front_face.grid = new_front_grid
    #     new_opposite_face.grid = new_opposite_grid
    #     new_left_face.grid = new_left_grid
    #     new_right_face.grid = new_right_grid
    #     new_top_face.grid = new_top_grid
    #     new_bottom_face.grid = new_bottom_grid
        
    #     # Resetting current front based on the rotation
    #     self.current_front = self.current_front.right

    #     # Transferring values from new face to the original face
    #     help.transfer_faces(self.current_front, new_right_face)
    #     help.transfer_faces(self.current_front.left, new_front_face)
    #     help.transfer_faces(self.current_front.right, new_opposite_face)
    #     help.transfer_faces(self.current_front.opposite, new_left_face)
    #     help.transfer_faces(self.current_front.top, new_top_face)
    #     help.transfer_faces(self.current_front.bottom, new_bottom_face)
    
    # def rotate_right_vertically(self):
    #     self.rotate_left_vertically()
    #     self.rotate_left_vertically()
    #     self.rotate_left_vertically()

    # def rotate_left_horizontally(self):
    #     self.rotate_right_vertically()
    #     self.rotate_down()
    #     self.rotate_left_vertically()
    
    # def rotate_right_horizontally(self):
    #     self.rotate_left_vertically()
    #     self.rotate_down()
    #     self.rotate_right_vertically()

    # def invert_vertically(self):
    #     self.rotate_left_vertically()
    #     self.rotate_left_vertically()
    
    # def invert_horizontally(self):
    #     self.rotate_left_horizontally()
    #     self.rotate_left_horizontally()

    def reset_perspective(self):
        while True:
            if is_default_perspective(self):
                break
            else:
                blue_face_side = self.blue_face.side_of_cube
                if blue_face_side == Orientation.TOP:
                    # self.rotate_down()
                    rotate.down(self.current_front)
                elif blue_face_side == Orientation.BOTTOM:
                    # self.rotate_up()
                    rotate.up(self.current_front)
                elif blue_face_side == Orientation.BACK:
                    if is_white_face_top(self.current_front, self.white_face):
                        # self.invert_vertically()
                        invert.vertically(self.current_front)
                    else:
                        # self.invert_horizontally()
                        invert.horizontally(self.current_front)
                elif blue_face_side == Orientation.LEFT:
                    # self.rotate_right_vertically()
                    rotate.right_vertical(self.current_front)
                elif blue_face_side == Orientation.RIGHT:
                    # self.rotate_left_vertically()
                    rotate.left_vertical(self.current_front)
                else:
                    # self.rotate_left_horizontally()
                    rotate.left_horizontal(self.current_front)

    # def shift_right_col_up(self):
    #     # Getting updated grids for each face
    #     new_front_grid = rcu.front_grid(self.current_front)
    #     new_opposite_grid = rcu.opposite_grid(self.current_front)
    #     new_left_grid = rcu.left_grid(self.current_front)
    #     new_right_grid = rcu.right_grid(self.current_front)
    #     new_top_grid = rcu.top_grid(self.current_front)
    #     new_bottom_grid = rcu.bottom_grid(self.current_front)
        
    #     # Setting updated grids
    #     self.current_front.grid = new_front_grid
    #     self.current_front.opposite.grid = new_opposite_grid
    #     self.current_front.left.grid = new_left_grid
    #     self.current_front.right.grid = new_right_grid
    #     self.current_front.top.grid = new_top_grid
    #     self.current_front.bottom.grid = new_bottom_grid

    # def shift_right_col_down(self):
    #     self.shift_right_col_up()
    #     self.shift_right_col_up()
    #     self.shift_right_col_up()

    # def shift_left_col_up(self):
    #     # Getting updated grids for each face
    #     new_front_grid = lcu.front_grid(self.current_front)
    #     new_opposite_grid = lcu.opposite_grid(self.current_front)
    #     new_left_grid = lcu.left_grid(self.current_front)
    #     new_right_grid = lcu.right_grid(self.current_front)
    #     new_top_grid = lcu.top_grid(self.current_front)
    #     new_bottom_grid = lcu.bottom_grid(self.current_front)
        
    #     # Setting updated grids
    #     self.current_front.grid = new_front_grid
    #     self.current_front.opposite.grid = new_opposite_grid
    #     self.current_front.left.grid = new_left_grid
    #     self.current_front.right.grid = new_right_grid
    #     self.current_front.top.grid = new_top_grid
    #     self.current_front.bottom.grid = new_bottom_grid

    # def shift_left_col_down(self):
    #     self.shift_left_col_up()
    #     self.shift_left_col_up()
    #     self.shift_left_col_up()

    # def shift_top_row_left(self):
    #     # Getting updated grids for each face
    #     new_front_grid = trl.front_grid(self.current_front)
    #     new_opposite_grid = trl.opposite_grid(self.current_front)
    #     new_left_grid = trl.left_grid(self.current_front)
    #     new_right_grid = trl.right_grid(self.current_front)
    #     new_top_grid = trl.top_grid(self.current_front)
    #     new_bottom_grid = trl.bottom_grid(self.current_front)
        
    #     # Setting updated grids
    #     self.current_front.grid = new_front_grid
    #     self.current_front.opposite.grid = new_opposite_grid
    #     self.current_front.left.grid = new_left_grid
    #     self.current_front.right.grid = new_right_grid
    #     self.current_front.top.grid = new_top_grid
    #     self.current_front.bottom.grid = new_bottom_grid

    # def shift_top_row_right(self):
    #     self.shift_top_row_left()
    #     self.shift_top_row_left()
    #     self.shift_top_row_left()

    # def shift_bottom_row_left(self):
    #     # Getting updated grids for each face
    #     new_front_grid = brl.front_grid(self.current_front)
    #     new_opposite_grid = brl.opposite_grid(self.current_front)
    #     new_left_grid = brl.left_grid(self.current_front)
    #     new_right_grid = brl.right_grid(self.current_front)
    #     new_top_grid = brl.top_grid(self.current_front)
    #     new_bottom_grid = brl.bottom_grid(self.current_front)
        
    #     # Setting updated grids
    #     self.current_front.grid = new_front_grid
    #     self.current_front.opposite.grid = new_opposite_grid
    #     self.current_front.left.grid = new_left_grid
    #     self.current_front.right.grid = new_right_grid
    #     self.current_front.top.grid = new_top_grid
    #     self.current_front.bottom.grid = new_bottom_grid

    # def shift_bottom_row_right(self):
    #     self.shift_bottom_row_left()
    #     self.shift_bottom_row_left()
    #     self.shift_bottom_row_left()


class Face:
    
    def __init__(self, colour, left=None, right=None, top=None, bottom=None, front=None, back=None, opposite=None, grid=None, side_of_cube=None, is_copy=False) -> None:
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.front = front
        self.back = back
        self.side_of_cube = side_of_cube
        self._opposite = opposite
        self._colour = colour
        self._is_copy = is_copy
        self._id = colour.value

        if not is_copy:
            self.grid = self.initialize_grid()
        else:
            self.grid = grid

    def __repr__(self) -> str:
        first_row = ""
        second_row = ""
        third_row = ""
        
        if self.side_of_cube == Orientation.LEFT:
            first_row = f"{self.grid[FacePositions.TOP_RIGHT]} {self.grid[FacePositions.TOP_CENTER]} {self.grid[FacePositions.TOP_LEFT]}"
            second_row = f"{self.grid[FacePositions.MID_RIGHT]} {self.grid[FacePositions.CENTER]} {self.grid[FacePositions.MID_LEFT]}"
            third_row = f"{self.grid[FacePositions.BOTTOM_RIGHT]} {self.grid[FacePositions.BOTTOM_CENTER]} {self.grid[FacePositions.BOTTOM_LEFT]}"

        elif self.side_of_cube in [Orientation.FRONT, Orientation.BOTTOM, Orientation.TOP]:
            first_row = f"{self.grid[FacePositions.TOP_LEFT]} {self.grid[FacePositions.MID_LEFT]} {self.grid[FacePositions.BOTTOM_LEFT]}"
            second_row = f"{self.grid[FacePositions.TOP_CENTER]} {self.grid[FacePositions.CENTER]} {self.grid[FacePositions.BOTTOM_CENTER]}"
            third_row = f"{self.grid[FacePositions.TOP_RIGHT]} {self.grid[FacePositions.MID_RIGHT]} {self.grid[FacePositions.BOTTOM_RIGHT]}"

        elif self.side_of_cube == Orientation.BACK:
            first_row = f"{self.grid[FacePositions.BOTTOM_RIGHT]} {self.grid[FacePositions.MID_RIGHT]} {self.grid[FacePositions.TOP_RIGHT]}"
            second_row = f"{self.grid[FacePositions.BOTTOM_CENTER]} {self.grid[FacePositions.CENTER]} {self.grid[FacePositions.TOP_CENTER]}"
            third_row = f"{self.grid[FacePositions.BOTTOM_LEFT]} {self.grid[FacePositions.MID_LEFT]} {self.grid[FacePositions.TOP_LEFT]}"

        elif self.side_of_cube == Orientation.RIGHT:
            first_row = f"{self.grid[FacePositions.BOTTOM_LEFT]} {self.grid[FacePositions.BOTTOM_CENTER]} {self.grid[FacePositions.BOTTOM_RIGHT]}"
            second_row = f"{self.grid[FacePositions.MID_LEFT]} {self.grid[FacePositions.CENTER]} {self.grid[FacePositions.MID_RIGHT]}"
            third_row = f"{self.grid[FacePositions.TOP_LEFT]} {self.grid[FacePositions.TOP_CENTER]} {self.grid[FacePositions.TOP_RIGHT]}" 
        else:
            print("This is why there is no output at all")

        output = f"{first_row}\n{second_row}\n{third_row}"

        return output

    @property
    def colour(self):
        return self._colour

    @property
    def opposite(self):
        return self._opposite

    @opposite.setter
    def opposite(self, face):
        if not self._opposite:
            self._opposite = face
        else:
            raise ImmutableAttributeError()
    
    @property
    def is_copy(self):
        return self._is_copy

    def copy(self):
        return Face(self.colour, self.left, self.right, self.top, self.bottom, self.front, self.back, self.opposite, self.grid.copy(), self.side_of_cube, is_copy=True)

    def initialize_grid(self):
        # Initializing center piece
        center_piece = Piece(self, FacePositions.CENTER, PieceTypes.CENTER)

        # Initializing edge pieces
        top_center_piece = EdgePiece(self, FacePositions.TOP_CENTER, PieceTypes.EDGE)
        mid_left_piece = EdgePiece(self, FacePositions.MID_LEFT, PieceTypes.EDGE)
        mid_right_piece = EdgePiece(self, FacePositions.MID_RIGHT, PieceTypes.EDGE)
        bottom_center_piece = EdgePiece(self, FacePositions.BOTTOM_CENTER, PieceTypes.EDGE)

        # Initializing corner pieces
        top_left_piece = CornerPiece(self, FacePositions.TOP_LEFT, PieceTypes.CORNER)
        top_right_piece = CornerPiece(self, FacePositions.TOP_RIGHT, PieceTypes.CORNER)
        bottom_left_piece = CornerPiece(self, FacePositions.BOTTOM_LEFT, PieceTypes.CORNER)
        bottom_right_piece = CornerPiece(self, FacePositions.BOTTOM_RIGHT, PieceTypes.CORNER)

        # Creating the pieces on the face using numpy arrays
        grid = [
            [top_left_piece, top_center_piece, top_right_piece],
            [mid_left_piece, center_piece, mid_right_piece],
            [bottom_left_piece, bottom_center_piece, bottom_right_piece]
        ]
    
        return np.array(grid)

    def print_attrs(self):
        print(f'Colour: {self.colour}')
        print(f'Left: Face({self.left._id})')
        print(f'Right: Face({self.right._id})')
        try:
            print(f'Top: Face({self.top._id})')
        except AttributeError:
            print('Top: N/A')

        try:
            print(f'Bottom: Face({self.bottom._id})')
        except AttributeError:
            print('Bottom: N/A')

        try:
            print(f'Front: Face({self.front._id})')
        except AttributeError:
            print('Front: N/A')
            
        try:
            print(f'Back: Face({self.back._id})')
        except AttributeError:
            print('Back: N/A')
            
        print(f'Opposite: Face({self.opposite._id})')
        print(f'Side of Cube: {self.side_of_cube}')

    def update_grid_attrs(self):
        self.grid[FacePositions.TOP_LEFT].face_position = FacePositions.TOP_LEFT
        self.grid[FacePositions.TOP_CENTER].face_position = FacePositions.TOP_CENTER
        self.grid[FacePositions.TOP_RIGHT].face_position = FacePositions.TOP_RIGHT
        self.grid[FacePositions.MID_LEFT].face_position = FacePositions.MID_LEFT
        self.grid[FacePositions.CENTER].face_position = FacePositions.CENTER
        self.grid[FacePositions.MID_RIGHT].face_position = FacePositions.MID_RIGHT
        self.grid[FacePositions.BOTTOM_LEFT].face_position = FacePositions.BOTTOM_LEFT
        self.grid[FacePositions.BOTTOM_CENTER].face_position = FacePositions.BOTTOM_CENTER
        self.grid[FacePositions.BOTTOM_RIGHT].face_position = FacePositions.BOTTOM_RIGHT

        self.grid[FacePositions.TOP_LEFT].face = self
        self.grid[FacePositions.TOP_CENTER].face = self
        self.grid[FacePositions.TOP_RIGHT].face = self
        self.grid[FacePositions.MID_LEFT].face = self
        self.grid[FacePositions.CENTER].face = self
        self.grid[FacePositions.MID_RIGHT].face = self
        self.grid[FacePositions.BOTTOM_LEFT].face = self
        self.grid[FacePositions.BOTTOM_CENTER].face = self
        self.grid[FacePositions.BOTTOM_RIGHT].face = self
    
    def init_face_complements(self):
        if self.side_of_cube == Orientation.FRONT:
            self.grid[FacePositions.TOP_CENTER].complement = self.top.grid[FacePositions.BOTTOM_CENTER]
            self.grid[FacePositions.MID_LEFT].complement = self.left.grid[FacePositions.MID_RIGHT]
            self.grid[FacePositions.MID_RIGHT].complement = self.right.grid[FacePositions.MID_LEFT]
            self.grid[FacePositions.BOTTOM_CENTER].complement = self.bottom.grid[FacePositions.TOP_CENTER]
            
            self.grid[FacePositions.TOP_LEFT].complements = {self.top.grid[FacePositions.BOTTOM_LEFT], self.left.grid[FacePositions.TOP_RIGHT]}
            self.grid[FacePositions.TOP_RIGHT].complements = {self.top.grid[FacePositions.BOTTOM_RIGHT], self.right.grid[FacePositions.TOP_LEFT]}
            self.grid[FacePositions.BOTTOM_LEFT].complements = {self.bottom.grid[FacePositions.TOP_LEFT], self.left.grid[FacePositions.BOTTOM_RIGHT]}
            self.grid[FacePositions.BOTTOM_RIGHT].complements = {self.bottom.grid[FacePositions.TOP_RIGHT], self.right.grid[FacePositions.BOTTOM_LEFT]}
        elif self.side_of_cube == Orientation.BACK:
            self.grid[FacePositions.TOP_CENTER].complement = self.top.grid[FacePositions.TOP_CENTER]
            self.grid[FacePositions.MID_LEFT].complement = self.left.grid[FacePositions.MID_RIGHT]
            self.grid[FacePositions.MID_RIGHT].complement = self.right.grid[FacePositions.MID_LEFT]
            self.grid[FacePositions.BOTTOM_CENTER].complement = self.bottom.grid[FacePositions.BOTTOM_CENTER]
            
            self.grid[FacePositions.TOP_LEFT].complements = {self.top.grid[FacePositions.TOP_RIGHT], self.right.grid[FacePositions.TOP_RIGHT]}
            self.grid[FacePositions.TOP_RIGHT].complements = {self.top.grid[FacePositions.TOP_LEFT], self.left.grid[FacePositions.TOP_LEFT]}
            self.grid[FacePositions.BOTTOM_LEFT].complements = {self.bottom.grid[FacePositions.BOTTOM_RIGHT], self.right.grid[FacePositions.BOTTOM_RIGHT]}
            self.grid[FacePositions.BOTTOM_RIGHT].complements = {self.bottom.grid[FacePositions.BOTTOM_LEFT], self.left.grid[FacePositions.BOTTOM_LEFT]}
        elif self.side_of_cube == Orientation.LEFT:
            self.grid[FacePositions.TOP_CENTER].complement = self.top.grid[FacePositions.MID_LEFT]
            self.grid[FacePositions.MID_LEFT].complement = self.left.grid[FacePositions.MID_RIGHT]
            self.grid[FacePositions.MID_RIGHT].complement = self.right.grid[FacePositions.MID_LEFT]
            self.grid[FacePositions.BOTTOM_CENTER].complement = self.bottom.grid[FacePositions.MID_LEFT]
            
            self.grid[FacePositions.TOP_LEFT].complements = {self.top.grid[FacePositions.TOP_LEFT], self.left.grid[FacePositions.TOP_RIGHT]}
            self.grid[FacePositions.TOP_RIGHT].complements = {self.top.grid[FacePositions.BOTTOM_LEFT], self.right.grid[FacePositions.TOP_LEFT]}
            self.grid[FacePositions.BOTTOM_LEFT].complements = {self.bottom.grid[FacePositions.BOTTOM_LEFT], self.left.grid[FacePositions.BOTTOM_RIGHT]}
            self.grid[FacePositions.BOTTOM_RIGHT].complements = {self.bottom.grid[FacePositions.TOP_LEFT], self.right.grid[FacePositions.BOTTOM_LEFT]}
        elif self.side_of_cube == Orientation.RIGHT:
            self.grid[FacePositions.TOP_CENTER].complement = self.top.grid[FacePositions.MID_RIGHT]
            self.grid[FacePositions.MID_LEFT].complement = self.left.grid[FacePositions.MID_RIGHT]
            self.grid[FacePositions.MID_RIGHT].complement = self.right.grid[FacePositions.MID_LEFT]
            self.grid[FacePositions.BOTTOM_CENTER].complement = self.bottom.grid[FacePositions.MID_RIGHT]
            
            self.grid[FacePositions.TOP_LEFT].complements = {self.top.grid[FacePositions.BOTTOM_RIGHT], self.left.grid[FacePositions.TOP_RIGHT]}
            self.grid[FacePositions.TOP_RIGHT].complements = {self.top.grid[FacePositions.TOP_RIGHT], self.right.grid[FacePositions.TOP_LEFT]}
            self.grid[FacePositions.BOTTOM_LEFT].complements = {self.bottom.grid[FacePositions.TOP_RIGHT], self.left.grid[FacePositions.BOTTOM_RIGHT]}
            self.grid[FacePositions.BOTTOM_RIGHT].complements = {self.bottom.grid[FacePositions.BOTTOM_RIGHT], self.right.grid[FacePositions.BOTTOM_LEFT]}
        elif self.side_of_cube == Orientation.TOP:
            self.grid[FacePositions.TOP_CENTER].complement = self.back.grid[FacePositions.TOP_CENTER]
            self.grid[FacePositions.MID_LEFT].complement = self.left.grid[FacePositions.TOP_CENTER]
            self.grid[FacePositions.MID_RIGHT].complement = self.right.grid[FacePositions.TOP_CENTER]
            self.grid[FacePositions.BOTTOM_CENTER].complement = self.front.grid[FacePositions.TOP_CENTER]
            
            self.grid[FacePositions.TOP_LEFT].complements = {self.back.grid[FacePositions.TOP_RIGHT], self.left.grid[FacePositions.TOP_LEFT]}
            self.grid[FacePositions.TOP_RIGHT].complements = {self.back.grid[FacePositions.TOP_LEFT], self.right.grid[FacePositions.TOP_RIGHT]}
            self.grid[FacePositions.BOTTOM_LEFT].complements = {self.front.grid[FacePositions.TOP_LEFT], self.left.grid[FacePositions.TOP_RIGHT]}
            self.grid[FacePositions.BOTTOM_RIGHT].complements = {self.front.grid[FacePositions.TOP_RIGHT], self.right.grid[FacePositions.TOP_LEFT]}
        elif self.side_of_cube == Orientation.BOTTOM:
            self.grid[FacePositions.TOP_CENTER].complement = self.front.grid[FacePositions.BOTTOM_CENTER]
            self.grid[FacePositions.MID_LEFT].complement = self.left.grid[FacePositions.BOTTOM_CENTER]
            self.grid[FacePositions.MID_RIGHT].complement = self.right.grid[FacePositions.BOTTOM_CENTER]
            self.grid[FacePositions.BOTTOM_CENTER].complement = self.back.grid[FacePositions.BOTTOM_CENTER]
            
            self.grid[FacePositions.TOP_LEFT].complements = {self.front.grid[FacePositions.BOTTOM_LEFT], self.left.grid[FacePositions.BOTTOM_RIGHT]}
            self.grid[FacePositions.TOP_RIGHT].complements = {self.front.grid[FacePositions.BOTTOM_RIGHT], self.right.grid[FacePositions.BOTTOM_LEFT]}
            self.grid[FacePositions.BOTTOM_LEFT].complements = {self.back.grid[FacePositions.BOTTOM_RIGHT], self.left.grid[FacePositions.BOTTOM_LEFT]}
            self.grid[FacePositions.BOTTOM_RIGHT].complements = {self.back.grid[FacePositions.BOTTOM_LEFT], self.right.grid[FacePositions.BOTTOM_RIGHT]}
    

class Piece:
    
    def __init__(self, face, face_position, piece_type) -> None:
        self.face = face
        self._colour = self.face.colour
        self.face_position = face_position
        self._piece_type = piece_type

    def __repr__(self) -> str:
        return self.colour.value[0]

    @property
    def colour(self):
        return self._colour
    
    @property
    def piece_type(self):
        return self._piece_type

        
class EdgePiece(Piece):
    
    def __init__(self, face, face_position, piece_type, complement=None) -> None:
        super().__init__(face, face_position, piece_type)
        self._complement = complement

    @property
    def complement(self):
        return self._complement

    @complement.setter
    def complement(self, complement):
        if self._complement is None:
            self._complement = complement
        else:
            raise ImmutableAttributeError()

            
class CornerPiece(Piece):
    
    def __init__(self, face, face_position, piece_type, complements=None) -> None:
        super().__init__(face, face_position, piece_type)
        self._complements = complements

    @property
    def complements(self):
        return self._complements
    
    @complements.setter
    def complements(self, complements):
        if self._complements is None:
            self._complements = complements
        else:
            raise ImmutableAttributeError()
    