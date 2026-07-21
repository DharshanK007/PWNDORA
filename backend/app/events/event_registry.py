class EventRegistry:
    def __init__(self):
        self._subscribers = {}
        
    def register(self, event_name: str, handler_func):
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler_func)

    def get_subscribers(self, event_name: str):
        return self._subscribers.get(event_name, [])

registry = EventRegistry()
