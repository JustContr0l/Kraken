import logging
import telebot
from telebot import types

logger = logging.getLogger("Kraken.T.SM")


class TelegramSender:
    __TOKEN: str = None
    __CHAT_IDS: list = []
    __bot = None

    def set_token(self, token: str):
        self.__TOKEN = token
        self.__bot = telebot.TeleBot(token=self.__TOKEN)
        logger.info("Telegram Sender has been started.")

    def set_chat_id(self, chat_id: str):
        self.__CHAT_IDS.append(chat_id)
        logger.info(f"Add new chat_id: {chat_id}")

    def send_csgo_message(self, name: str, min_p: float, price: float, wear: str, stickers: list):
        item_url = f"https://steamcommunity.com/market/listings/730/" \
                   f"{name.replace(' ', '%20').replace('|', '%7C').replace('(', '%28').replace(')', '%29')}"
        button_bar = types.InlineKeyboardButton('ITEM URL', url=item_url)

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_bar)

        message = f"Bot find new item.\n\n" \
                  f"Name: {name}\n" \
                  f"Price: {price:.2f}$\n" \
                  f"Min.Price: {min_p:.2f}$\n\n" \
                  f"Wear: {wear}\n"

        if len(stickers) > 0:
            message += "\nStickers:\n"
            all_sticker_price = 0.0
            for sticker in stickers:
                message += f" Name: {sticker['name']} | Price: {sticker['price']}$\n"
                if sticker["price"]:
                    all_sticker_price += sticker["price"]
            message += f"\n All stickers price: {all_sticker_price:.2f}$\n"
            price_with_stickers = price + (all_sticker_price * 0.05)
            message += f" Price with stickers: {price_with_stickers:.2f}$\n"

        for chat_id in self.__CHAT_IDS:
            logger.info(f"Send info about new item. [{chat_id}]")
            self.__bot.send_message(chat_id, text=message, reply_markup=keyboard)
