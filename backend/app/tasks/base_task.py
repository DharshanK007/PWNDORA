from abc import ABC, abstractmethod
from typing import Any

class BaseTask(ABC):
    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        pass
