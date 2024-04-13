from typing import Optional

class FaceTransferError(Exception):
    
    def __init__(self) -> None:
        msg = 'Face attributes couldn\'t be transferred as the passed in arguments aren\'t Face objects'
        super().__init__(msg)

        
class ImmutableAttributeError(Exception):
    
    def __init__(self) -> None:
        msg = 'Attribute value cannot be changed once set'
        super().__init__(msg)

        
class OperationStackContentsError(Exception):
    
    def __init__(self, msg: Optional[str] = None) -> None:
        if not msg:
            msg = 'Cannot shuffle cube if there are no operations in the operation stack'
        super().__init__(msg)

        
class InvalidOperationError(Exception):
    
    def __init__(self, msg: Optional[str] = None) -> None:
        if not msg:
            msg = 'Invalid operation requested on cube'
        super().__init__(msg)


class InvalidOrientationError(Exception):
    
    def __init__(self, msg: Optional[str] = None) -> None:
        if not msg:
            msg = "Face's orientation is not valid"
        super().__init__(msg)