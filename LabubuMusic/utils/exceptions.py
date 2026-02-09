class AssistantErr(Exception):
    """
    Raised when the Assistant client encounters a playback error.
    """
    def __init__(self, message: str):
        super().__init__(message)