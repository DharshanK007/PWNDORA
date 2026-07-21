from fastapi import BackgroundTasks
from typing import Callable, Any

class TaskManager:
    @staticmethod
    def enqueue(background_tasks: BackgroundTasks, func: Callable, *args: Any, **kwargs: Any):
        """
        Enqueues a task for background execution.
        Using FastAPI's BackgroundTasks as the underlying engine for now.
        Can be swapped with Celery/Redis later.
        """
        background_tasks.add_task(func, *args, **kwargs)
