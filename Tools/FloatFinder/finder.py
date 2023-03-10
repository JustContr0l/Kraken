import time
import random
import logging
import requests
from ..TgBot import TelegramSender
from ..JsonDumps import SteamItemsJSON
from ..SiteParsers import SteamLotsParser

logger = logging.getLogger("Kraken.T.FF")


class FloatFinder(SteamLotsParser, SteamItemsJSON, TelegramSender):
    _min_price: float = None
    _max_price: float = None

    _allowed_names: list = []
    _blocked_names: list = []
    __items: list = []

    __used_urls: dict = {}

    _min_float: float = None
    _max_float: float = None
    _min_sticker_x: float = None

    def set_items_settings(self, allowed_names: list, blocked_names: list,
                           min_price: float = 0.0, max_price: float = 1.0,
                           min_float: float = 0.009999999, max_float: float = 0.96, min_sticker_x: float = 3.0,
                           parse_fn: bool = True, parse_bs: bool = True):
        self._min_float, self._max_float, self._min_sticker_x = min_float, max_float, min_sticker_x
        self.__items = self.get_items_for_ff(allowed_names, blocked_names, min_price, max_price,
                                             730, parse_fn, parse_bs)

    def _check_item(self, wear, price, min_price, stickers):
        if min_price * 2 < price:
            return False

        wear = float(wear)
        if wear >= self._max_float:
            return True
        if wear <= self._min_float:
            return True
        # print("Bad Item Wear:", wear)

        all_stickers_price = 0.0
        for sticker in stickers:
            sticker_price = sticker["price"]
            if sticker_price is not False:
                all_stickers_price += sticker_price
        if all_stickers_price > price * self._min_sticker_x:
            return True
        # print("All stickers price:", all_stickers_price, "Item Price:", price)
        return False

    @staticmethod
    def _get_item_wear(over_url: str):
        code_1 = over_url.split('/730/')[-1].split('/+csgo')[0]
        code_2 = over_url.split('+csgo_econ_action_preview%')[-1]
        url = f"http://127.0.0.1:3000/getinfo?code1={code_1}&code2={code_2}"
        resp = requests.get(url).json()
        if not resp["paintwear"]:
            return False
        return resp["paintwear"]

    def start(self):
        while True:
            for item in self.__items:
                logger.debug(f"Check item: {item['name']}")
                lots = self.get_lots(item_name=item["name"])
                request_time = time.time()
                if not lots:
                    logger.warning("Somethings wrong. No lots. Sleep min: 2m, max: 3m.")
                    time.sleep(random.randint(120, 180))
                    continue
                for index, lot in enumerate(lots):
                    if index != 0:
                        time.sleep(0.51)

                    over_url = lot["over_url"]
                    if over_url in self.__used_urls:
                        # wear = self.__used_urls[over_url]["paintwear"]
                        continue
                    else:
                        wear = str(self._get_item_wear(over_url=over_url))
                        self.__used_urls.update({over_url: {"paintwear": wear}})

                    if not wear:
                        logger.warning("No wear from check server. Mb lot is not weapon. Skip.")
                        continue

                    price = lot["price"]
                    min_price = lot["min_price"]

                    stickers = []
                    if len(lot["stickers"]) > 0:
                        for sticker in lot["stickers"]:
                            stickers.append({
                                "name": sticker,
                                "price": self.get_item_price(sticker)
                            })

                    check_result = self._check_item(wear, price, min_price, stickers)
                    if not check_result:
                        continue

                    logger.info("Find good item!")
                    self.send_csgo_message(lot["name"], min_price, lot["price"], wear, stickers)

                if time.time() - request_time < self._min_delay:
                    time.sleep(random.uniform(self._min_delay, self._max_delay))
            logger.info("No items. Sleep before next check.")
            # time.sleep(random.randint(120, 180))
