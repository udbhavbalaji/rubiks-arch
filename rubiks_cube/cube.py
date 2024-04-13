from __future__ import annotations
from typing import Optional
from rubiks_cube.constants import Colours, Orientation, FacePositions, PieceTypes, Operations as ops
from rubiks_cube.errors import ImmutableAttributeError, OperationStackContentsError, InvalidOperationError
from rubiks_cube.predicates import is_default_perspective, is_white_face_top
from rubiks_cube.operations import Rotations as rotate, Inversions as invert, Shifts as shift

import random
import numpy as np

FACE_ORDER = ['FRONT', 'LEFT', 'RIGHT', 'TOP', 'OPPOSITE', 'BOTTOM']
POTENTIAL_FACE_ORDER = ['FRONT', 'OPPOSITE', 'LEFT', 'RIGHT', 'TOP', 'BOTTOM']
INVERSE_OP_MAPPING = {
    ops.ROTATE_DOWN: ops.ROTATE_UP,
    ops.ROTATE_UP: ops.ROTATE_DOWN,
    ops.ROTATE_LEFT_VERTICALLY: ops.ROTATE_RIGHT_VERTICALLY,
    ops.ROTATE_RIGHT_VERTICALLY: ops.ROTATE_LEFT_VERTICALLY,
    ops.ROTATE_LEFT_HORIZONTALLY: ops.ROTATE_RIGHT_HORIZONTALLY,
    ops.ROTATE_RIGHT_HORIZONTALLY: ops.ROTATE_LEFT_HORIZONTALLY,
    ops.INVERT_VERTICALLY: ops.INVERT_VERTICALLY,
    ops.INVERT_HORIZONTALLY: ops.INVERT_HORIZONTALLY,
    ops.SHIFT_RIGHT_COL_UP: ops.SHIFT_RIGHT_COL_DOWN,
    ops.SHIFT_LEFT_COL_UP: ops.SHIFT_LEFT_COL_DOWN,
    ops.SHIFT_RIGHT_COL_DOWN: ops.SHIFT_RIGHT_COL_UP,
    ops.SHIFT_LEFT_COL_DOWN: ops.SHIFT_LEFT_COL_UP,
    ops.SHIFT_TOP_ROW_LEFT: ops.SHIFT_TOP_ROW_RIGHT,
    ops.SHIFT_TOP_ROW_RIGHT: ops.SHIFT_TOP_ROW_LEFT,
    ops.SHIFT_BOTTOM_ROW_LEFT: ops.SHIFT_BOTTOM_ROW_RIGHT,
    ops.SHIFT_BOTTOM_ROW_RIGHT: ops.SHIFT_BOTTOM_ROW_LEFT
}


class RubiksCube:
    
    def __init__(self, blue_face: Optional[Face] = None, red_face: Optional[Face] = None, orange_face: Optional[Face] = None, white_face: Optional[Face] = None, green_face: Optional[Face] = None, yellow_face: Optional[Face] = None, is_copy: bool = False) -> None:
        self.blue_face = blue_face
        self.red_face = red_face
        self.orange_face = orange_face
        self.white_face = white_face
        self.green_face = green_face
        self.yellow_face = yellow_face

        self.op_stack: list[ops] = []

        if not is_copy:
            self.define_cube()
        else:
            self.current_front = self.blue_face

    def __repr__(self) -> str:
        front = self.current_front
        
        front_grid = repr(front).split('\n')
        left_grid = repr(front.left).split('\n')
        right_grid = repr(front.right).split('\n')
        top_grid = repr(front.top).split('\n')
        opposite_grid = repr(front.opposite).split('\n')
        bottom_grid = repr(front.bottom).split('\n')

        try:
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
        except IndexError:
            print(front)
            print(front.left)
            print(front.right)
            print(front.top)
            print(front.opposite)
            print(front.bottom)

        return output

    @property
    def faces(self) -> list[Face]:
        return [
            self.current_front,
            self.current_front.left,
            self.current_front.right,
            self.current_front.top,
            self.current_front.opposite,
            self.current_front.bottom
        ]

    def define_cube(self) -> None:
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

        # Assigning complement pieces
        self.assign_complements()

    def assign_complements(self) -> None:
        for face in self.faces:
            face.init_face_complements()

    def print_face_ids(self) -> None:
        for pos, face in zip(FACE_ORDER, self.faces):
            print(f'{pos}: {face._id}')

    def rotate(self, op: ops, unshuffling: bool = False) -> None:
        if op not in rotate.rotations:
            raise InvalidOperationError

        if not unshuffling:
            if len(self.op_stack) > 0:
                if self.op_stack[-1] == INVERSE_OP_MAPPING[op]:
                    self.op_stack.pop()
                else:
                    self.op_stack.append(op)
            else:
                self.op_stack.append(op)
            print(op.value)
        
        rotate.rotations[op](self)

    def invert(self, op: ops, unshuffling: bool = False) -> None:
        if op not in invert.inversions:
            raise InvalidOperationError
        
        if not unshuffling:
            if len(self.op_stack) > 0:
                if self.op_stack[-1] == INVERSE_OP_MAPPING[op]:
                    self.op_stack.pop()
                else:
                    self.op_stack.append(op)
            else:
                self.op_stack.append(op)
            print(op.value)
            
        invert.inversions[op](self)

    def shift(self, op: ops, unshuffling: bool = False) -> None:
        if op not in shift.shifts:
            raise InvalidOperationError
        
        if not unshuffling:
            if len(self.op_stack) > 0:
                if self.op_stack[-1] == INVERSE_OP_MAPPING[op]:
                    self.op_stack.pop()
                else:
                    self.op_stack.append(op)
            else:
                self.op_stack.append(op)
            print(op.value)
            
        shift.shifts[op](self)

    def reset_perspective(self) -> None:
        while True:
            if is_default_perspective(self):
                break
            else:
                blue_face_side = self.blue_face.side_of_cube
                if blue_face_side == Orientation.TOP:
                    self.rotate(ops.ROTATE_DOWN)
                elif blue_face_side == Orientation.BOTTOM:
                    self.rotate(ops.ROTATE_UP)
                elif blue_face_side == Orientation.BACK:
                    if is_white_face_top(self.current_front, self.white_face):
                        self.invert(ops.INVERT_VERTICALLY)
                    else:
                        self.invert(ops.INVERT_HORIZONTALLY)
                elif blue_face_side == Orientation.LEFT:
                    self.rotate(ops.ROTATE_RIGHT_VERTICALLY)
                elif blue_face_side == Orientation.RIGHT:
                    self.rotate(ops.ROTATE_LEFT_VERTICALLY)
                else:
                    self.rotate(ops.ROTATE_LEFT_HORIZONTALLY)
                    
    def shuffle(self, num_ops: Optional[int] = None) -> None:
        if len(self.op_stack) != 0:
            raise OperationStackContentsError

        if num_ops:
            num_operations = num_ops
        else:
            num_operations = np.random.randint(100, 200)

        for _ in range(num_operations):
            p = np.random.random()
            if p > 0.95:
                op = random.choice(list(invert.inversions.keys()))
                self.invert(op)
            elif 0.7 < p <= 0.95:
                op = random.choice(list(rotate.rotations.keys()))
                self.rotate(op)
            else:
                op = random.choice(list(shift.shifts.keys()))
                self.shift(op)

    def unshuffle(self) -> None:
        if len(self.op_stack) == 0:
            raise InvalidOperationError
        
        for _ in range(len(self.op_stack)):
            inverse_op = INVERSE_OP_MAPPING[self.op_stack.pop()]
            if inverse_op in rotate.rotations:
                self.rotate(inverse_op, unshuffling=True)
            elif inverse_op in invert.inversions:
                self.invert(inverse_op, unshuffling=True)
            elif inverse_op in shift.shifts:
                self.shift(inverse_op, unshuffling=True)
            else:
                raise InvalidOperationError('Invalid operation requested while unshuffling!')


class Face:
    
    def __init__(self, colour: Colours, left: Optional[Face] = None, right: Optional[Face] = None, top: Optional[Face] = None, bottom: Optional[Face] = None, front: Optional[Face] = None, back: Optional[Face] = None, opposite: Optional[Face] = None, grid: Optional[np.ndarray] = None, side_of_cube: Optional[Orientation] = None, is_copy: bool = False) -> None:
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
    def colour(self) -> Colours:
        return self._colour

    @property
    def opposite(self) -> Face:
        return self._opposite

    @opposite.setter
    def opposite(self, face: Face) -> None:
        if not self._opposite:
            self._opposite = face
        else:
            raise ImmutableAttributeError()
    
    @property
    def is_copy(self) -> bool:
        return self._is_copy

    def copy(self) -> Face:
        return Face(self.colour, self.left, self.right, self.top, self.bottom, self.front, self.back, self.opposite, self.grid.copy(), self.side_of_cube, is_copy=True)

    def initialize_grid(self) -> np.ndarray:
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

    def print_attrs(self) -> None:
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

    def update_grid_attrs(self) -> None:
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
    
    def init_face_complements(self) -> None:
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
    
    def __init__(self, face: Face, face_position: FacePositions, piece_type: PieceTypes) -> None:
        self.face = face
        self._colour = self.face.colour
        self.face_position = face_position
        self._piece_type = piece_type

    def __repr__(self) -> str:
        return self.colour.value[0]

    @property
    def colour(self) -> Colours:
        return self._colour
    
    @property
    def piece_type(self) -> PieceTypes:
        return self._piece_type

        
class EdgePiece(Piece):
    
    def __init__(self, face: Face, face_position: FacePositions, piece_type: PieceTypes, complement: Optional[EdgePiece] = None) -> None:
        super().__init__(face, face_position, piece_type)
        self._complement = complement

    @property
    def complement(self) -> EdgePiece:
        return self._complement

    @complement.setter
    def complement(self, complement: EdgePiece) -> None:
        if self._complement is None:
            self._complement = complement
        else:
            raise ImmutableAttributeError()

            
class CornerPiece(Piece):
    
    def __init__(self, face: Face, face_position: FacePositions, piece_type: PieceTypes, complements: Optional[set[CornerPiece]]=None) -> None:
        super().__init__(face, face_position, piece_type)
        self._complements = complements

    @property
    def complements(self) -> set[CornerPiece]:
        return self._complements
    
    @complements.setter
    def complements(self, complements: set[CornerPiece]) -> None:
        if self._complements is None:
            self._complements = complements
        else:
            raise ImmutableAttributeError()
    