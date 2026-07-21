from .clue_types import ClueType

class ClueProvider:
    def get_clue(self, clue_id: str, clue_type: ClueType) -> dict:
        return {"id": clue_id, "type": clue_type, "content": "Sample Clue Content"}
