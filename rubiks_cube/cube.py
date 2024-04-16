"""
This module contains the definition of RubiksCube, Face, Piece, EdgePiece & CornerPiece classes. Each class contains properties and methods
that allow all possible operations that can be done to a rubiks cube in real life.

"""
from __future__ import annotations
from typing import Optional
from rubiks_cube.constants import Colours, Orientation, FacePositions, PieceTypes, Operations as ops
from rubiks_cube.errors import ImmutableAttributeError, OperationStackContentsError, InvalidOperationError, InvalidOrientationError, CubeIntegrityError
from rubiks_cube.predicates import is_default_perspective, is_white_face_top
from rubiks_cube.operations import Rotations as rotate, Inversions as invert, Shifts as shift

import random
import numpy as np

FACE_ORDER = ['FRONT', 'LEFT', 'RIGHT', 'TOP', 'OPPOSITE', 'BOTTOM']
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
    
    """
    This is a class representing the Rubiks Cube. A cube has 6 faces (type=Face). It is initialized with the blue face
    in front, red face on the left, orange face on the right, green face on the back, white face on top and yellow face on the bottom (referred to as 'default perspective').
    
    ATTRIBUTES:
        current_front: Pointer to the Face instance that is currently set as front face of the cube
        blue_face: Pointer to the Blue Face instance that is part of the cube
        red_face: Pointer to the Red Face instance that is part of the cube
        orange_face: Pointer to the Orange Face instance that is part of the cube
        green_face: Pointer to the Green Face instance that is part of the cube
        white_face: Pointer to the White Face instance that is part of the cube
        yellow_face: Pointer to the Yellow Face instance that is part of the cube
        op_stack: List that contains the stack of operations that have been performed on the cube
        
    PROPERTIES:
        faces: List of faces that are part of the cube
        
    METHODS:
        define_cube: Defines the cube structure
        assign_complements: Assigns complement values for all pieces in the cube
        print_face_ids: Helper method that displays enumerated faces of the cube in the order defined in FACE_ORDER (defined above)
        rotate: Performs the specified rotation operation 
        invert: Performs the specified inversion operation
        shift: Performs the specified shift operation
        reset_perspective: Resets the cube's perspective back to default perspective
        shuffle: Shuffles cube by performing random operations on the cube
        unshuffle: Unshuffles cube by performing the inverse of operations in operation stack

    """
    
    def __init__(self, blue_face: Optional[Face] = None, red_face: Optional[Face] = None, orange_face: Optional[Face] = None, white_face: Optional[Face] = None, green_face: Optional[Face] = None, yellow_face: Optional[Face] = None, is_copy: bool = False) -> None:
        """
        Constructor method for the Rubiks Cube class.

        Args:
            blue_face (Face, optional): Face instance for the blue face of the cube. Defaults to None.
            red_face (Face, optional): Face instance for the red face of the cube. Defaults to None.
            orange_face (Face, optional): Face instance for the orange face of the cube. Defaults to None.
            white_face (Face, optional): Face instance for the white face of the cube. Defaults to None.
            green_face (Face, optional): Face instance for the green face of the cube. Defaults to None.
            yellow_face (Face, optional): Face instance for the yellow face of the cube. Defaults to None.
            is_copy (bool, optional): Flag representing if the cube is a copy. Defaults to False.

        """
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
        """
        This method is used to create a string representation of the cube instance.
        
                            _________
        Every face's grid = |1, 2, 3|
                            |4, 5, 6|
                            |7, 8, 9|
                            ---------

        The output representation is as follows:
        
            Left Face
              _______   Bottom Face
              |3 2 1|   /
              |6 5 4|  /
              |9 8 7| /
        _____________L___________
        |1 4 7|1 4 7|9 6 3|1 4 7|
Front   |2 5 8|2 5 8|8 5 2|2 5 8| Top
Face    |3 6 9|3 6 9|7 4 1|3 6 9| Face
        -------------------------
              |7 8 9|   \
              |4 5 6|    \
              |1 2 3|    Back Face
              -------
            Right Face


        Raises:
            CubeIntegrityError: Error representing that the cube's integrity was broken by a prior operation

        Returns:
            str: string representation of a rubiks cube instance

        """
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
            raise CubeIntegrityError("Cube's current front face hasn't been transformed correctly. One or more essential attributes are of NoneType")

        return output

    @property
    def faces(self) -> list[Face]:
        """
        This property returns a list of all the cube's faces in order of FACE_ORDER (defined above).

        Returns:
            list: List of the cube's faces

        """
        return [
            self.current_front,
            self.current_front.left,
            self.current_front.right,
            self.current_front.top,
            self.current_front.opposite,
            self.current_front.bottom
        ]

    def define_cube(self) -> None:
        """
        This method initializes the Rubiks Cube. The faces (type=Face) are created, edges are joined & opposite faces, positional attributes
        are assigned. Every piece's complement value(s) are assigned for each piece (type=Piece | EdgePiece | CornerPiece).

        Side Faces Initialization:
                                (Top)
                        (Left Col)   (Right Col)
                                ^    ^
                                |    |
                                _______
                                |1 2 3|-> (Top Row)
                (Left)          |4 5 6|                  (Right)
                                |7 8 9|-> (Bottom Row)
                                -------
                                (Bottom)

        Top Face Initialization:
                                (Back)
                        (Left Col)   (Right Col)
                                ^    ^
                                |    |
                                _______
                                |1 2 3|-> (Top Row)
                (Left)          |4 5 6|                  (Right)
                                |7 8 9|-> (Bottom Row)
                                -------
                                (Front)
                                
        Bottom Face Initialization:
                                (Front)
                        (Left Col)   (Right Col)
                                ^    ^
                                |    |
                                _______
                                |1 2 3|-> (Top Row)
                (Left)          |4 5 6|                  (Right)
                                |7 8 9|-> (Bottom Row)
                                -------
                                (Back)

        """
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
        """
        This method assigns complements for each piece (type=EdgePiece | CornerPiece) in the cube. The cube's faces are looped through.
        The Face class has a method that initializes the complement values for each piece in the face instance.

        """
        for face in self.faces:
            face.init_face_complements()

    def print_face_ids(self) -> None:
        """
        This helper method displays the enumerated face instances part of the cube in the order of FACE_ORDER (defined above).

        """
        for pos, face in zip(FACE_ORDER, self.faces):
            print(f'{pos}: {face._id}')

    def rotate(self, op: ops, unshuffling: bool = False) -> None:
        """
        This method performs the specified rotation operation.

        Args:
            op (Operations): Enumerated operation constant indicating which operation is requested.
            unshuffling (bool, optional): Flag parameter indicating to the method if the operation 
                                        being requested is part of the unshuffling operation. Defaults to False.

        Raises:
            InvalidOperationError: Raised if the operation requested is not a a valid rotation operation.

        """ 
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
        """
        This method performs the specified inversion operation.

        Args:
            op (Operations): Enumerated operation constant indicating which operation is requested.
            unshuffling (bool, optional): Flag parameter indicating to the method if the operation
                                        being requested is part of the unshuffling operation. Defaults to False.

        Raises:
            InvalidOperationError: Raised if the operation requested is not a valid inversion operation.

        """ 
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
        """
        This method performs the specified shift operation.

        Args:
            op (Operations): Enumerated operation constant indicating which operation is requested.
            unshuffling (bool, optional): Flag parameter indicating to the method if the operation 
                                        being requested is part of the unshuffling operation. Defaults to False.

        Raises:
            InvalidOperationError: Raised if the operation requested is not a valid shift operation.

        """
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
        """
        This method resets the cube's orientation to the default perspective. The end-state of the cube after the 
        method is done running will have the blue face in front, red face on the left and white face on the top. This is 
        also the same perspective that the cube was initialized. NOTE: No shift operations are performed at all during 
        this process. Therefore, the positions of the pieces aren't changed.

        """
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
        """
        This method shuffles the cube by performing randomly chosen operations. Number of operations
        is either randomly chosen (between 100 & 200) or can be supplied by the user.

        Args:
            num_ops (int, optional): Number of operations to be chosen while shuffling the cube. Defaults to None.

        Raises:
            OperationStackContentsError: Raised if the cube's operation stack's contents aren't compatible with the operation.

        """
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
        """
        This method unshuffles the cube by performing the inverse operations of the operations stored in the cube's
        operation stack. The result of this operation is a fully new (& solved!) rubiks cube.

        Raises:
            OperationStackContentsError: Raised if the operation stack is empty.
            InvalidOperationError: Raised when the cube's operation stack contains an invalid operation.

        """
        if len(self.op_stack) == 0:
            raise OperationStackContentsError('Cannot unshuffle a solved cube. Try to perform some operations before trying to unshuffle.')
        
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
    
    """
    This is a class representing a face of a rubiks cube (type=RubiksCube) as part of the rubiks cube 
    architecture. Each face has a 3 X 3 grid, representing the 9 pieces (type=Piece | EdgePiece | CornerPiece) 
    present on a rubiks cube's face. The face instance's colour attribute is always set to be the colour of 
    the face's center piece.
    
    ATTRIBUTES:
        left: Pointer to the face instance to the left of the face
        right: Pointer to the face instance to the right of the face
        top: Pointer to the face instance to the top of the face, if the current face is a side face
        bottom: Pointer to the face instance to the bottom of the face, if the current face is a side face
        front: Pointer to the face instance to the front of the face, if the current face is a top/bottom face
        back: Pointer to the face instance to the back of the face, if the current face is a top/bottom face
        grid: 2-dimensional array storing the pieces for each face
    
    PROPERTIES:
        colour: Enum colour literal indicating the primary colour of the face
        opposite: Pointer to the face instance that is opposite to the current face
        is_copy: Boolean flag indicating if the current face is a copy
    
    METHODS:
        copy: Creates a duplicate instance of the current face
        initialize_grid: Creates and initializes the piece objects for the current face
        update_grid_attrs: Method that updates the attributes of each piece instance of the current face after each operation is performed on the rubiks cube
        init_face_complements: Method that initializes the complement values for each piece (type=EdgePiece | CornerPiece) in the current face
        print_attrs: Helper method that displays all essential attribute values for the current face
    
    """
    
    def __init__(self, colour: Colours, left: Optional[Face] = None, right: Optional[Face] = None, top: Optional[Face] = None, bottom: Optional[Face] = None, front: Optional[Face] = None, back: Optional[Face] = None, opposite: Optional[Face] = None, grid: Optional[np.ndarray] = None, side_of_cube: Optional[Orientation] = None, is_copy: bool = False) -> None:
        """
        Constructor method for the Face class.

        Args:
            colour (Colours): Colour literal for the current face
            left (Face, optional): Pointer to the face instance to the left of the current face. Defaults to None.
            right (Face, optional): Pointer to the face instance to the right of the current face. Defaults to None.
            top (Face, optional): Pointer to the face instance to the top of the current face if it's a side face. Defaults to None.
            bottom (Face, optional): Pointer to the face instance to the bottom of the current face if it's a side face. Defaults to None.
            front (Face, optional): Pointer to the face instance to the front of the current face if it's a top/bottom face. Defaults to None.
            back (Face, optional): Pointer to the face instance to the back of the current face if it's a top/bottom face. Defaults to None.
            opposite (Face, optional): Pointer to the face instance that is opposite to the current face. Defaults to None.
            grid (np.ndarray, optional): 3 X 3 grid representing the current face's pieces. Defaults to None.
            side_of_cube (Orientation, optional): Orientation literal indicating which side  of the cube the current face is at the current state. Defaults to None.
            is_copy (bool, optional): Boolean flag indicating if the current face is a copy. Defaults to False.

        """
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
        """
        This method is used to create a string representation of the face instance. The representation of each face
        is arranged as per the cube's representation and changes based on the cube's state. For each face's individual
        representation, refer to RubiksCube.__repr__() documentation and see the corresponding orientation's arrangement.

        Raises:
            InvalidOrientationError: Raised if the current face has an invalid Orientation with respect to the cube or 
                                    the face doesn't belong to a rubiks cube instance.

        Returns:
            str: String representation of the current face's grid with respect to its position in its rubiks cube.

        """
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
            raise InvalidOrientationError

        output = f"{first_row}\n{second_row}\n{third_row}"

        return output

    @property
    def colour(self) -> Colours:
        """
        This property returns the face's primary colour.

        Returns:
            Colours: Colour literal representing a colour within the rubiks cube architecture.

        """
        return self._colour

    @property
    def opposite(self) -> Face:
        """
        This property returns the current face's opposite face.

        Returns:
            Face: Pointer to the opposite face instance.

        """
        return self._opposite

    @opposite.setter
    def opposite(self, face: Face) -> None:
        """
        This is the setter method for the opposite property.

        Args:
            face (Face): Face instance to be set as opposite face.

        Raises:
            ImmutableAttributeError: Raised when attempt is made to re-assign property once assigned.

        """
        if not self._opposite:
            self._opposite = face
        else:
            raise ImmutableAttributeError()
    
    @property
    def is_copy(self) -> bool:
        """
        This property returns if the current face is a copy.

        Returns:
            bool: Boolean flag indicating if the current face is a copy

        """
        return self._is_copy

    def copy(self) -> Face:
        """
        This method creates and returns a new face instance with the same attribute values.

        Returns:
            Face: Newly created face instance with duplicated attributes.

        """
        return Face(self.colour, self.left, self.right, self.top, self.bottom, self.front, self.back, self.opposite, self.grid.copy(), self.side_of_cube, is_copy=True)

    def initialize_grid(self) -> np.ndarray:
        """
        This method creates 9 pieces (type=Piece | EdgePiece | CornerPiece) and assigns them to corresponding position in the current face's grid.

        Returns:
            np.ndarray: 3 X 3 matrix containing the pieces of the current face

        """
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

    def update_grid_attrs(self) -> None:
        """
        This is a method that updates the state attributes of the current face's pieces. Since the various operations can change these
        values, it is important to track the current state of these attributes. Called for each face after each operation.

        """
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
        """
        This method initializes the complement(s) values for the current face's pieces. Once these are set, they cannot 
        be changed. Current face must belong to a cube i.e. face.side_of_cube must be type=Orientation. 

        """
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
    
    def print_attrs(self) -> None:
        """
        This is a helper method that displays all the attributes of the current face. Mainly 
        used to debug to ensure that transformations are taking place accurately.

        """
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

    
class Piece:
    
    """
    This is a class that represents each piece on each face instance of a rubiks cube instance. 
    
    ATTRIBUTES:
        face: Pointer to the face instance that the piece is currently on.
        face_position: FacePosition constant indicating the piece's position in the face instance.
    
    PROPERTIES:
        colour: Colour enum showing the piece's colour.
        piece_type: PieceType literal storing the type of piece it is (values=CENTER | EDGE | CORNER)
    
    """
    
    def __init__(self, face: Face, face_position: FacePositions, piece_type: PieceTypes) -> None:
        """
        Constructor method for the Piece class.

        Args:
            face (Face): Pointer to the face instance that the piece is currently in.
            face_position (FacePositions): FacePosition constant (tuple[int,int]) indicating the current piece's position in its face.
            piece_type (PieceTypes): PieceType literal indicating the type of piece

        """
        self.face = face
        self._colour: Colours = self.face.colour
        self.face_position = face_position
        self._piece_type = piece_type

    def __repr__(self) -> str:
        """
        This method creates a string representation of a piece instance. Each piece is represented as the first character in 
        the piece's colour. This is because the most important representational aspect of the piece is its colour.

        Returns:
            str: First character of the piece's colour

        """
        return self.colour.value[0]

    @property
    def colour(self) -> Colours:
        """
        This property returns the piece's colour.

        Returns:
            Colours: Colours literal showing the current piece instance's colour.

        """
        return self._colour
    
    @property
    def piece_type(self) -> PieceTypes:
        """
        This property returns the current piece instance's piece type.

        Returns:
            PieceTypes: PieceType literal showing the current piece instance's piece type.

        """
        return self._piece_type

        
class EdgePiece(Piece):

    """
    This is a class that represents an edge piece in the rubiks architecture. Inherits from the Piece class.
    
    ATTRIBUTES:
        face: Pointer to the face instance that the piece is currently on.
        face_position: FacePosition constant indicating the piece's position in the face instance.
    
    PROPERTIES:
        colour: Colour enum showing the piece's colour.
        piece_type: PieceType literal storing the type of piece it is (values=CENTER | EDGE | CORNER)
        complement: Pointer to the edge piece instance that is directly adjacent to the current piece.
    
    """
    
    def __init__(self, face: Face, face_position: FacePositions, piece_type: PieceTypes, complement: Optional[EdgePiece] = None) -> None:
        """
        Constructor method for the EdgePiece class.

        Args:
            face (Face): Pointer to the face instance that the piece is currently in.
            face_position (FacePositions): FacePosition constant (tuple[int,int]) indicating the current piece's position in its face.
            piece_type (PieceTypes): PieceType literal indicating the type of piece
            complement (EdgePiece, optional): Pointer to the edge piece instance that is directly adjacent to the current piece instance.
            
        """
        super().__init__(face, face_position, piece_type)
        self._complement = complement

    @property
    def complement(self) -> EdgePiece:
        """
        This property returns the current piece instance's complement piece.

        Returns:
            EdgePiece: Pointer to the current piece instance's complement

        """
        return self._complement

    @complement.setter
    def complement(self, complement: EdgePiece) -> None:
        """
        This is a setter method for the complement property.

        Args:
            complement (EdgePiece): Complement of the current piece instance

        Raises:
            ImmutableAttributeError: Raised when value is trying to be re-assigned after initial assignment.

        """
        if self._complement is None:
            self._complement = complement
        else:
            raise ImmutableAttributeError()

            
class CornerPiece(Piece):
    
    """
    This is a class that represents an corner piece in the rubiks architecture. Inherits from the Piece class.
    
    ATTRIBUTES:
        face: Pointer to the face instance that the piece is currently on.
        face_position: FacePosition constant indicating the piece's position in the face instance.
    
    PROPERTIES:
        colour: Colour enum showing the piece's colour.
        piece_type: PieceType literal storing the type of piece it is (values=CENTER | EDGE | CORNER)
        complements: Pointer to the corner pieces instance that are directly adjacent to the current piece.
    
    """
    
    def __init__(self, face: Face, face_position: FacePositions, piece_type: PieceTypes, complements: Optional[set[CornerPiece]]=None) -> None:
        """
        Constructor method for the CornerPiece class.

        Args:
            face (Face): Pointer to the face instance that the piece is currently in.
            face_position (FacePositions): FacePosition constant (tuple[int,int]) indicating the current piece's position in its face.
            piece_type (PieceTypes): PieceType literal indicating the type of piece
            complements (set[CornerPiece], optional): Set that contains the pointers to the corner piece instances 
                                                    that are directly adjacent to the current piece instance.
            
        """
        super().__init__(face, face_position, piece_type)
        self._complements = complements

    @property
    def complements(self) -> set[CornerPiece]:
        """
        This property returns the set of complement pieces to the current piece instance. 

        Returns:
            set[CornerPiece]: Set containing the complement pieces of the current piece instance.

        """
        return self._complements
    
    @complements.setter
    def complements(self, complements: set[CornerPiece]) -> None:
        """
        This is a setter method for the complements property.

        Args:
            complements (set[CornerPiece]): Set of corner piece instances

        Raises:
            ImmutableAttributeError: Raised when value is trying to be re-assigned after initial assignment.
            
        """
        if self._complements is None:
            self._complements = complements
        else:
            raise ImmutableAttributeError()
    