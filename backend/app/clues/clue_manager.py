from .clue_provider import ClueProvider
from .clue_validator import ClueValidator

class ClueManager:
    def __init__(self):
        self.provider = ClueProvider()
        self.validator = ClueValidator()

    def request_clue(self, clue_id: str, user_progress: int):
        if self.validator.is_clue_unlocked(clue_id, user_progress):
            return self.provider.get_clue(clue_id, None)
        return None

clue_manager = ClueManager()
