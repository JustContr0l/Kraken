import json
import logging
import requests
from .misc import iterators, delay

logger = logging.getLogger("Kraken.T.SP.SL")


class SteamLotsParser:
    _proxies: list = None
    _game_id: int = None

    _iterator = None
    _min_delay: float = None
    _max_delay: float = None

    def set_settings(self, proxies: list, game_id: int):
        self._proxies = proxies
        self._game_id = game_id

        self._iterator = iterators.proxy_ua_iterator(proxies, one_proxy_count=5)
        self._min_delay, self._max_delay = delay.get_min_max_float_delay(proxies)

    @staticmethod
    def _get_stickers_from_html(html):
        if len(html) < 10:
            return []

        html_sticker_line = html.split("<br>Sticker: ")[-1].split("</center></div>")[0]
        stickers = html_sticker_line.split(",")
        stickers = [f"Sticker | {sticker.strip()}" for sticker in stickers]

        return stickers

    def _send_request(self, name: str):
        # Send request
        url = f"https://steamcommunity.com/market/listings/{self._game_id}/{name}/render/?query=&start=0&" \
              f"count=30&country=US&language=english&currency=1&norender=1"
        proxy, user_agent = next(self._iterator)
        logger.debug(f"Send new request to Steam Api. [{name}][{proxy.split('@')[-1]}]")
        resp = requests.get(url, headers={'User-Agent': user_agent}, proxies={'https': proxy})

        # Check response
        if resp.status_code != 200:
            logger.warning(f"Proxy banned or something wrong. [{resp.status_code}]")
            return False
        logger.debug("Get new response from Steam.")

        # Get info from response
        resp_data = json.loads(resp.text)

        # Iterate all lots
        lots = []
        min_lot_price = 0
        for list_info in resp_data["listinginfo"]:
            # Get listing info from JSON
            list_item = resp_data["listinginfo"][list_info]

            # Get lot price and check min_price
            try:
                price = (int(list_item["converted_price"]) + int(list_item["converted_fee"])) * 0.01
            except KeyError:
                logger.debug("Item already purchased. Skip.")
                continue
            if min_lot_price == 0 or min_lot_price > price:
                min_lot_price = price

            # Get asset info from JSON
            asset_id = list_item["asset"]["id"]
            asset = resp_data["assets"]["730"]["2"][asset_id]

            # Save lot info
            market_name = asset["market_hash_name"]
            lot = {
                "name": market_name,
                "price": price,
                "min_price": min_lot_price,
                "game_id": self._game_id,
            }

            # If game CSGO, parse stickers and update lot info
            if self._game_id == 730:
                over_url = asset["market_actions"][0]["link"].replace("%assetid%", asset_id)
                stickers = asset["descriptions"][-1]["value"]
                lot.update({
                    "over_url": over_url,
                    "stickers": self._get_stickers_from_html(html=stickers),
                })

            # Save lot info
            lots.append(lot)

        logger.info(f"Get lots response. [{name}]")
        return lots

    def get_lots(self, item_name: str):
        resp = self._send_request(name=item_name)
        if resp is False:
            return False
        return resp
