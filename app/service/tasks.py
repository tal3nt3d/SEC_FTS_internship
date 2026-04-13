from storage.tasks import tasks_db
from config.errors import TaskNotFoundError
async def get_tasks():
    tasks = tasks_db
    if not tasks:
        raise TaskNotFoundError()
    return tasks