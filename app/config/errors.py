"""Application custom exceptions."""

class AppException(Exception):
    """Base application exception."""
    def __init__(self, message="Application error"):
        self.message = message
        super().__init__(self.message)

class TaskNotFoundError(AppException):
    """Raised when task not found."""
    def __init__(self, message="Task not found"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundError(AppException):
    """Raised when user not found."""
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)

class CommentNotFoundError(AppException):
    """Raised when comment not found."""
    def __init__(self, message="Comment not found"):
        self.message = message
        super().__init__(self.message)
