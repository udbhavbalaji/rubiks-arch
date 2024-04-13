

def is_default_perspective(cube):
    return is_blue_face_front(cube.current_front, cube.blue_face) and is_white_face_top(cube.current_front, cube.white_face) and is_red_face_left(cube.current_front, cube.red_face)


def is_blue_face_front(current_front, blue_face):
    return current_front == blue_face

    
def is_white_face_top(current_front, white_face):
    return current_front.top == white_face


def is_red_face_left(current_front, red_face):
    return current_front.left == red_face