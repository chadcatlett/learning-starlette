import json
import os
import sys

import requests
from authlib.integrations.requests_client import OAuth2Auth

BASE_URL="https://us.api.blizzard.com/hearthstone"
CARDS_URL=f"{BASE_URL}/cards"
METADATA_URL=f"{BASE_URL}/metadata"
DEFAULT_PARAMS={
    'locale': 'en_US'
}

# def get_input(prompt: str, secure:bool=False):
#     """Prompt for user input, but loop until something is typed"""
#     if not prompt:
#         # error if passed None, empty string, anything that results in 'False'
#         raise ValueError(f"get_input expects a valid prompt, got: {prompt}")
#     while True:
#         if secure:
#             user_input = getpass(prompt)
#         else:
#             user_input = input(prompt)
#         if user_input:
#             return user_input
#         print("Didn't quite get that, let's try again.")

def get_metadata(session):
    try:
        response = session.get(METADATA_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to get metadata: {str(e)}")
        sys.exit(1)


def _get_cards(session: requests.Session, params: dict):
    page = 1
    cards = []
    page_params = {
        'pageSize': 500,
        'page': page
    }

    try:
        while True:
            page_params['page'] = page
            result = session.get(CARDS_URL, params=params|page_params)
            result.raise_for_status()
            temp_cards = result.json()
            if temp_cards.get('cards'):
                cards.extend(temp_cards['cards'])
            else:
                print(f"Failed to get cards for {params | page_params}")
                sys.exit(1)
            if temp_cards['pageCount'] == page:
                break
            page += 1
    except requests.RequestException as e:
        print(f"Failed to get cards: {str(e)}")
        sys.exit(1)
    return cards

def get_cards(session):
    all_cards = []

    # we fetch cards in two batches.
    # according to the Card search API docs manaCost specifies a specific manaCost value,
    # unless the manaCost is 10, in which case query changes to be considered greater than or equal to 10.

    # shared params
    params = {
        'class': 'druid,warlock',
        'rarity': 'legendary'
    }

    # first batch is manaCost of 7-9, inclusive of each end of the range
    first_batch_params = {
        'manaCost': '7,8,9'
    }

    # second batch is manaCost equal to or greate than 10.
    second_batch_params = {
        'manaCost': '10'
    }

    # fetch first batch
    cards = _get_cards(session, DEFAULT_PARAMS|params|first_batch_params)
    all_cards.extend(cards)
    cards = _get_cards(session, DEFAULT_PARAMS|params|second_batch_params)
    all_cards.extend(cards)
    return all_cards

def main():
    access_token = os.environ.get("BLIZZARD_ACCESS_TOKEN", None)
    if access_token is None:
        print("Set environment variable BLIZZARD_ACCESS_TOKEN to a valid access token value")
        sys.exit(1)

    auth = OAuth2Auth(dict(token_type="bearer", access_token=access_token))
    session = requests.session()
    session.auth = auth
    session.headers['Accept'] = "application/json"
    session.params = DEFAULT_PARAMS
    if not os.path.exists("metadata.json"):
        print("Fetching metadata")
        metadata = get_metadata(session)
        print("Storing metadata")
        json.dump(metadata, open("metadata.json", "w"), indent=1)
    else:
        print("Already have metadata.json, remove it to fetch latest metadata")
    if not os.path.exists('cards.json'):
        print("Fetching card data")
        cards = get_cards(session)
        print(f"Storing {len(cards)} cards")
        json.dump(cards, open("cards.json", "w"), indent=1)
    else:
        print("Already have cards.jso, remove it to fetch the latest data.")
if __name__ == "__main__":
    main()