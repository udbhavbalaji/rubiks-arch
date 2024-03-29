from constants import Orientation


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