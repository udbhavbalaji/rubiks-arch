from constants import Colours


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
        return f"Cube({self.current_front}, {self.current_front.left}, {self.current_front.right}, {self.current_front.top}, {self.current_front.opposite}, {self.current_front.bottom})"

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
        

    
    pass


class Face:
    
    def __init__(self, colour, left=None, right=None, top=None, bottom=None, front=None, back=None, opposite=None, is_copy=False) -> None:
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.front = front
        self.back = back
        self.opposite = opposite
        self._colour = colour
        pass

    def __repr__(self) -> str:
        return f"Face({self.colour})"
    
    @property
    def colour(self):
        return self._colour
    
    pass