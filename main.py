import json
import uvicorn
import app.app

from app.types import Card
from utils import resolve_metadata

if __name__ == "__main__":
    metadata = json.load(open("metadata.json"))
    raw_cards = json.load(open("cards.json"))
    print("Building cards")
    cards = []
    for rcard in raw_cards:
        new_card = Card(rcard['name'],
                        rcard['image'],
                        resolve_metadata(metadata, "types", rcard["cardTypeId"]),
                        resolve_metadata(metadata, "rarities", rcard["rarityId"]),
                        resolve_metadata(metadata, "sets", rcard["cardSetId"]),
                        resolve_metadata(metadata, "classes", rcard["classId"])
                        )
        cards.append(new_card)
    app.app.CARDS = cards
    uvicorn.run("app:app.app", host="127.0.0.1", port=8000, log_level="info")