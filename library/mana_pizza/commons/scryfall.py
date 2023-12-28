import json
import os
from collections import defaultdict
from math import inf
from time import sleep

import requests
import urllib.parse


class ScryfallEndpoints:
    SEARCH_CARD    = "cards/search"
    LIST_SYMBOLOGY = "symbology"


class ScryfallClient:

    __SCRYFALL_API_HOST = "https://api.scryfall.com"

    def __request_scryfall_api(self, endpoint, body=None, params=None):
        sleep(.1)
        res = requests.get(f"{self.__SCRYFALL_API_HOST}/{endpoint}", json=body or {}, params=params or {})
        if res.status_code > 299:
            print(f"Something happened when requesting scryfall API: {res.content}")
            print(f"Endpoint: {endpoint}. Status code: {res.status_code}")
            return None
        return res.json()

    def __encode_q_param(self, value):
        return urllib.parse.quote(value, safe='"!, /\: \'')

    def fetch_symbology(self):
        return self.__request_scryfall_api(ScryfallEndpoints.LIST_SYMBOLOGY)["data"]

    def fetch_card_by_name(self, card_name, edition=None):
        print(f"Fetching card {card_name} from scryfall...")
        query = f"!\"{card_name}\""
        if edition:
            query += f" set:{edition}"
        res = self.__request_scryfall_api(ScryfallEndpoints.SEARCH_CARD, params={"q": self.__encode_q_param(query)})
        if not res:
            return None
        if res["total_cards"] > 1:
            print("Duplicated cards found!")
            return None
        return res["data"][0]
    

class CardsDB:

    __DB_FILE = "db.json"

    def __init__(self):
        with open(self.__DB_FILE) as db_content:
            self.db = json.load(db_content)

    def get_card_by_name(self, card_name):
        return self.db[card_name]


scryfall_client = ScryfallClient()
cards_db = CardsDB()