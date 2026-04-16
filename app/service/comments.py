from storage.comments import comments_db
from exceptions.errors import CommentNotFoundError

async def get_comments():
    comments = comments_db
    if not comments:
        raise CommentNotFoundError()
    return comments