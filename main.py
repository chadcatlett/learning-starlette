import os
import random
import sys
import uvicorn
import utils
import app.app

if __name__ == "__main__":
    access_token = os.environ.get("BLIZZARD_ACCESS_TOKEN", None)
    if access_token is None:
        print("Set environment variable BLIZZARD_ACCESS_TOKEN to a valid access token value")
        sys.exit(1)
    cards = utils.get_cards(access_token)
    random.shuffle(cards)
    app.app.CARDS = cards[0:10]
    app.app.CARDS.sort(key=lambda x:x.Id)
    uvicorn.run("app:app.app", host="127.0.0.1", port=8000, log_level="info")