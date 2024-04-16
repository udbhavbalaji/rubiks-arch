"""
This module contains the definitions of errors thrown in the rubiks cube architecture.
        
"""
from typing import Optional

class FaceTransferError(Exception):

    """
    Error class defined to throw excpetions when there is an error when trying to 
    transfer face attribute values from 1 face to another.
    
    """
    
    def __init__(self) -> None:
        """
        Constructor method for FaceTransferError class.

        """
        msg = 'Face attributes couldn\'t be transferred as the passed in arguments aren\'t Face objects'
        super().__init__(msg)

        
class ImmutableAttributeError(Exception):
    
    """
    Error class defined to throw excpetions when an attempt is made to try and re-assign
    immutable attributes within the rubiks cube architecture.
    
    """

    def __init__(self) -> None:
        """
        Constructor method for the ImmutableAttributeError class.
        
        """
        msg = 'Attribute value cannot be changed once set'
        super().__init__(msg)

        
class OperationStackContentsError(Exception):
    
    """
    Error class defined to throw excpetions when the rubiks cube instance's operation stack doesn't allow 
    certain operations on the cube.
    
    """

    def __init__(self, msg: Optional[str] = None) -> None:
        """
        Constructor method for the OperationStackContentsError class.

        Args:
            msg (str, optional): Optional error message. Defaults to None.

        """
        if not msg:
            msg = 'Cannot shuffle cube if there are no operations in the operation stack'
        super().__init__(msg)

        
class InvalidOperationError(Exception):
    
    """
    Error class defined to throw excpetions when an invalid operation is requested on the rubiks cube instance.
    
    """

    def __init__(self, msg: Optional[str] = None) -> None:
        """
        Constructor method for the InvalidOperationError class.

        Args:
            msg (str, optional): Optional error message. Defaults to None.

        """
        if not msg:
            msg = 'Invalid operation requested on cube'
        super().__init__(msg)


class InvalidOrientationError(Exception):
    
    """
    Error class defined to throw excpetions when a face instance has an invalid orientation value or the 
    face instance isn't part of any rubiks cube instance.
    
    """

    def __init__(self, msg: Optional[str] = None) -> None:
        """
        Constructor method for the InvalidOrientationError class.

        Args:
            msg (str, optional): Optional error message. Defaults to None.
        """
        if not msg:
            msg = "Face's orientation is not valid"
        super().__init__(msg)

        
class CubeIntegrityError(Exception):
    
    """
    Error class defined to throw excpetions when prior operations on the cube have broken the rubiks cube 
    instance's integrity.
    
    """

    def __init__(self, msg: Optional[str] = None) -> None:
        """
        Constructor method for the CubeIntegrityError class.

        Args:
            msg (str, optional): Optional error message. Defaults to None.
        """
        if not msg:
            msg = 'Cube Integrity has been broken!'
        super().__init__(msg)