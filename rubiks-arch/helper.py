from errors import FaceTransferError

def transfer_faces(orig, new):
    try:
        orig.left = new.left
        orig.right = new.right
        orig.top = new.top
        orig.bottom = new.bottom
        orig.front = new.front
        orig.back = new.back
    except AttributeError:
        raise FaceTransferError()
