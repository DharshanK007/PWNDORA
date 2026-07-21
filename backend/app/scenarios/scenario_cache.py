from typing import Any, Dict

class ScenarioCache:
    def __init__(self):
        self._cache: Dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self._cache.get(key)

    def set(self, key: str, value: Any):
        self._cache[key] = value

    def clear(self, scenario_id: str = None):
        if scenario_id:
            keys_to_remove = [k for k in self._cache.keys() if k.startswith(f"{scenario_id}:")]
            for k in keys_to_remove:
                del self._cache[k]
        else:
            self._cache.clear()
