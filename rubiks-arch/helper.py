from errors import FaceTransferError

def transfer_faces(orig, new):
    try:
        orig.left = new.left
        orig.right = new.right
        orig.top = new.top
        orig.bottom = new.bottom
        orig.front = new.front
        orig.back = new.back
        orig.side_of_cube = new.side_of_cube
    except AttributeError:
        raise FaceTransferError()
