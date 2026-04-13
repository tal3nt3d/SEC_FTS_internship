from storage.users import users_db
from config.errors import UserNotFoundError

async def get_users():
    users = users_db
    if not users:
        raise UserNotFoundError()
    return users