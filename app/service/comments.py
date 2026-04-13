from storage.comments import comments_db
from config.errors import CommentNotFoundError

async def get_comments():
    comments = comments_db
    if not comments:
        raise CommentNotFoundError()
    return comments