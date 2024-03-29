
class FaceTransferError(Exception):
    
    def __init__(self) -> None:
        msg = 'Face attributes couldn\'t be transferred as the passed in arguments aren\'t Face objects'
        super().__init__(msg)

        
class ImmutableAttributeError(Exception):
    
    def __init__(self) -> None:
        msg = 'Attribute value cannot be changed once set'
        super().__init__(msg)