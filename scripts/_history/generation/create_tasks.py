import os

base_dir = "backend/app/tasks"
os.makedirs(base_dir, exist_ok=True)

# base_task.py
with open(os.path.join(base_dir, "base_task.py"), "w") as f:
    f.write('''from abc import ABC, abstractmethod
from typing import Any

class BaseTask(ABC):
    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        pass
''')

# task_manager.py
with open(os.path.join(base_dir, "task_manager.py"), "w") as f:
    f.write('''from fastapi import BackgroundTasks
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
''')

# task_scheduler.py
with open(os.path.join(base_dir, "task_scheduler.py"), "w") as f:
    f.write('''import asyncio
import logging

logger = logging.getLogger(__name__)

class TaskScheduler:
    _tasks = []

    @classmethod
    def schedule(cls, func, interval_seconds: int):
        """
        Simple in-memory task scheduler.
        """
        async def loop():
            while True:
                await asyncio.sleep(interval_seconds)
                try:
                    # In a real app, you'd probably enqueue this to TaskManager/Celery
                    # or run it using a specific session.
                    func()
                except Exception as e:
                    logger.error(f"Error in scheduled task {func.__name__}: {e}")
                    
        cls._tasks.append(asyncio.create_task(loop()))
''')

# __init__.py
with open(os.path.join(base_dir, "__init__.py"), "w") as f:
    f.write('''# Init tasks module
''')

print("Created Background Task Framework files.")
