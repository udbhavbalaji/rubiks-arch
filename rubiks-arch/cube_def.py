from constants import Colours, Orientation
from errors import ImmutableAttributeError
from face_transformations import RotateUp as ru, RotateLeftVertical as rlv
from predicates import is_default_perspective, is_white_face_top

import helper as help


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

    def __repr__(self) -> str:
        return f"Cube(Front: {self.current_front}, Left: {self.current_front.left}, Right: {self.current_front.right}, Top: {self.current_front.top}, Opposite: {self.current_front.opposite}, Bottom: {self.current_front.bottom})"

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
        
        self.green_face.left = self.red_face
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
        
    def rotate_up(self):
        # Getting transformed faces
        new_front_face = ru.front_face(self.current_front)
        new_opposite_face = ru.opposite_face(self.current_front)
        new_left_face = ru.left_face(self.current_front)
        new_right_face = ru.right_face(self.current_front)
        new_top_face = ru.top_face(self.current_front)
        new_bottom_face = ru.bottom_face(self.current_front)

        # Resetting current front based on the rotation
        self.current_front = self.current_front.bottom

        # Transferring values from new face to the original face
        help.transfer_faces(self.current_front, new_bottom_face)
        help.transfer_faces(self.current_front.left, new_left_face)
        help.transfer_faces(self.current_front.right, new_right_face)
        help.transfer_faces(self.current_front.opposite, new_top_face)
        help.transfer_faces(self.current_front.top, new_front_face)
        help.transfer_faces(self.current_front.bottom, new_opposite_face)

    def rotate_down(self):
        self.rotate_up()
        self.rotate_up()
        self.rotate_up()

    def rotate_left_vertically(self):
        # Getting transformed faces
        new_front_face = rlv.front_face(self.current_front)
        new_opposite_face = rlv.opposite_face(self.current_front)
        new_left_face = rlv.left_face(self.current_front)
        new_right_face = rlv.right_face(self.current_front)
        new_top_face = rlv.top_face(self.current_front)
        new_bottom_face = rlv.bottom_face(self.current_front)
        
        # Resetting current front based on the rotation
        self.current_front = self.current_front.right

        # Transferring values from new face to the original face
        help.transfer_faces(self.current_front, new_right_face)
        help.transfer_faces(self.current_front.left, new_front_face)
        help.transfer_faces(self.current_front.right, new_opposite_face)
        help.transfer_faces(self.current_front.opposite, new_left_face)
        help.transfer_faces(self.current_front.top, new_top_face)
        help.transfer_faces(self.current_front.bottom, new_bottom_face)
    
    def rotate_right_vertically(self):
        self.rotate_left_vertically()
        self.rotate_left_vertically()
        self.rotate_left_vertically()

    def rotate_left_horizontally(self):
        self.rotate_right_vertically()
        self.rotate_down()
        self.rotate_left_vertically()
    
    def rotate_right_horizontally(self):
        self.rotate_left_vertically()
        self.rotate_down()
        self.rotate_right_vertically()

    def invert_vertically(self):
        self.rotate_left_vertically()
        self.rotate_left_vertically()
    
    def invert_horizontally(self):
        self.rotate_left_horizontally()
        self.rotate_left_horizontally()

    def reset_perspective(self):
        while True:
            if is_default_perspective(self):
                break
            else:
                blue_face_side = self.blue_face.side_of_cube
                if blue_face_side == Orientation.TOP:
                    self.rotate_down()
                elif blue_face_side == Orientation.BOTTOM:
                    self.rotate_up()
                elif blue_face_side == Orientation.BACK:
                    if is_white_face_top(self.current_front, self.white_face):
                        self.invert_vertically()
                    else:
                        self.invert_horizontally()
                elif blue_face_side == Orientation.LEFT:
                    self.rotate_right_vertically()
                elif blue_face_side == Orientation.RIGHT:
                    self.rotate_left_vertically()
                else:
                    self.rotate_left_horizontally()
    
    pass


class Face:
    
    def __init__(self, colour, left=None, right=None, top=None, bottom=None, front=None, back=None, opposite=None, side_of_cube=None, is_copy=False) -> None:
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
        pass

    def __repr__(self) -> str:
        return f"Face({self.colour})"
    
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
        return Face(self.colour, self.left, self.right, self.top, self.bottom, self.front, self.back, self.opposite, is_copy=True)
    
    pass