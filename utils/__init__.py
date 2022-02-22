from app.types import Card
def resolve_metadata(metadata, section, _id, default=None):
    """Return metdata value in a given section of metadata and given id"""
    for i in metadata[section]:
        if i['id'] == _id:
            return i['name']
    return default

import requests
from authlib.integrations.requests_client import OAuth2Auth

BASE_URL="https://us.api.blizzard.com/hearthstone"
CARDS_URL=f"{BASE_URL}/cards"
METADATA_URL=f"{BASE_URL}/metadata"
DEFAULT_PARAMS={
    'locale': 'en_US'
}

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

def get_raw_cards(session):
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

def get_cards(access_token):
    auth = OAuth2Auth(dict(token_type="bearer", access_token=access_token))
    session = requests.session()
    session.auth = auth
    session.headers['Accept'] = "application/json"
    session.params = DEFAULT_PARAMS

    metadata = get_metadata(session)
    raw_cards = get_raw_cards(session)

    cards = []

    for rcard in raw_cards:
        raw_classes = [rcard['classId'], ]
        if rcard['multiClassIds']:
            raw_classes = rcard['multiClassIds']

        new_card = Card(rcard['id'],
                        rcard['name'],
                        rcard['image'],
                        resolve_metadata(metadata, "types", rcard["cardTypeId"]),
                        resolve_metadata(metadata, "rarities", rcard["rarityId"]),
                        resolve_metadata(metadata, "sets", rcard["cardSetId"], "Core"),
                        ", ".join([resolve_metadata(metadata, "classes", i) for i in raw_classes]))
        cards.append(new_card)
    return cards