from service.tasks import TaskService

def get_task_service() -> TaskService:
    return TaskService()