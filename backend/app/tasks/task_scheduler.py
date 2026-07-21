import asyncio
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
