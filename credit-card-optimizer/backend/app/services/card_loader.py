from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "raw" / "credit_cards.json"


def load_cards() -> List[Dict[str, Any]]:
    """Load all credit card definitions from the JSON file."""
    with DATA_PATH.open("r", encoding="utf-8") as f:
        cards: List[Dict[str, Any]] = json.load(f)
    return cards


def get_card_by_id(card_id: str) -> Optional[Dict[str, Any]]:
    """Return a single card dict by its card_id, or None if not found."""
    cards = load_cards()
    for card in cards:
        if card.get("card_id") == card_id:
            return card
    return None


if __name__ == "__main__":
    # Simple manual test
    all_cards = load_cards()
    print(f"Loaded {len(all_cards)} cards.")
    sample_id = all_cards[0]["card_id"] if all_cards else None
    if sample_id:
        print(f"Sample card {sample_id}: {get_card_by_id(sample_id)}")

