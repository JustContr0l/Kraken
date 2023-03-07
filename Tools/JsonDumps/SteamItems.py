import json
import logging

logger = logging.getLogger("Kraken.T.SI")


class SteamItemsJSON:
    def __init__(self):
        with open("Tools/JsonDumps/market_items.json", "r", encoding='utf-8') as file:
            self.data = json.load(file)
            logger.info("Get items from JSON Dump.")

    def get_item_price(self, item_name: str):
        for item in self.data:
            if item["name"] == item_name:
                return item["price"]
        return False

    def get_items_for_ff(self, allowed_names: list, blocked_names: list,
                         min_p: float, max_p: float, game_id: int):
        items = []
        for item in self.data:
            if item["game_id"] != game_id:
                continue

            if not min_p < item["price"] < max_p:
                continue

            if len(blocked_names) > 0:
                bad_item = False
                for blocked_name in blocked_names:
                    if blocked_name in item["name"]:
                        bad_item = True
                        break
                if bad_item:
                    continue

            if len(allowed_names) > 0:
                for allowed_name in allowed_names:
                    if allowed_name in item["name"]:
                        items.append(item)
                        break
            else:
                items.append(item)

        logger.debug(f"Return {len(items)} from dump for FF.")
        return items
