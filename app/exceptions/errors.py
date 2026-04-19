"""Application custom exceptions."""

from fastapi import HTTPException, status

class AppException(HTTPException):
    """Base application exception."""
    def __init__(self, status_code: int, detail: str = "Application error"):
        super().__init__(status_code=status_code, detail=detail)

class TaskNotFoundError(AppException):
    """Raised when task not found."""
    def __init__(self, detail: str = "Task not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UserNotFoundError(AppException):
    """Raised when user not found."""
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class CommentNotFoundError(AppException):
    """Raised when comment not found."""
    def __init__(self, detail: str = "Comment not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class TaskAlreadyCompletedError(AppException):
    """Raised when trying to complete already completed task."""
    def __init__(self, detail: str = "Task has been already completed"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        
class TaskAlreadyArchivedError(AppException):
    """Raised when trying to archive already archived task."""
    def __init__(self, detail: str = "Task has been already archived"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    