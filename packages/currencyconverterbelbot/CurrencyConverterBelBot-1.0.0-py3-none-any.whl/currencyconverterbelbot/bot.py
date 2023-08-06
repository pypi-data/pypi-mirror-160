# variables url, TOKEN are stored in the config file
# -*- coding: UTF-8 -*-

import sys
import argparse
import requests
import logging
import typing
from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, executor, md, types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils.callback_data import CallbackData

from config import *

url = "https://myfin.by/currency/brest"


def createParser():
    parser = argparse.ArgumentParser(
        prog="bot",
        description="""The bot receives current exchange rates 
        from the site https://myfin.by/currency/brest, you only need to specify the bot token
        """,
        epilog="""(c) 2022. Telegram Bot (Long Poll)""",
    )
    parser.add_argument(
        "-t",
        "--token",
        required=True,
        help="""enter your bot token received from @BotFather to access the HTTP API or
        add config.py in folder with main program view token TOKEN = "TO:KEN",
        metavar="TO:KEN""",
    )

    return parser


def get_currency_from_bank(id: int):
    bank = soup.find("tr", id=f"bank-row-{id}")
    USD_buy = bank.find("td").next_sibling.text
    USD_sell = bank.find("td").next_sibling.next_sibling.text
    EUR_buy = bank.find("td").next_sibling.next_sibling.next_sibling.text
    EUR_sell = bank.find("td").next_sibling.next_sibling.next_sibling.next_sibling.text
    return USD_buy, USD_sell, EUR_buy, EUR_sell


logging.basicConfig(level=logging.INFO)


parser = createParser()
namespace = parser.parse_args(sys.argv[1:])
try:
    if namespace.token == "TOKEN":
        bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
        print(
            "TO:KEN taken from file config.py, specify the token as an argument, example -t TOKEN"
        )
    else:
        bot = Bot(token=namespace.token, parse_mode=types.ParseMode.HTML)
except:
    print(
        "define the TO:KEN as an argument or define TO:KEN in config.py, see the help"
    )
    sys.exit()

dp = Dispatcher(bot)

r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")

bank_list = list()
for i in range(2, 38, 2):
    name_bank = soup.find("tr", id=f"bank-row-{i}").find("a").text
    bank_list.append((f"{i}", f"{name_bank}"))
bank_dict = dict(bank_list)


BANKS = {
    str(key): {
        "title": f"{bank_dict[key]}",
        "body1": f"USD пок ",
        "body2": f"USD прод ",
        "body3": f"EUR пок ",
        "body4": f"EUR прод ",
    }
    for key in bank_dict
}


banks_cb = CallbackData("bank", "id", "action")


def get_keyboard() -> types.InlineKeyboardMarkup:
    """
    Generate keyboard with list of BANKS
    """
    markup = types.InlineKeyboardMarkup()
    for bank_id, bank in BANKS.items():
        markup.add(
            types.InlineKeyboardButton(
                bank["title"], callback_data=banks_cb.new(id=bank_id, action="view")
            ),
        )
    return markup


def format_bank(bank_id: str, bank: dict) -> (str, types.InlineKeyboardMarkup):
    USD_buy, USD_sell, EUR_buy, EUR_sell = get_currency_from_bank(bank_id)
    text = md.text(
        md.hbold(bank["title"]),
        md.quote_html(bank["body1"] + str(USD_buy)),
        md.quote_html(bank["body2"] + str(USD_sell)),
        md.quote_html(bank["body3"] + str(EUR_buy)),
        md.quote_html(bank["body4"] + str(EUR_sell)),
        "",  # just new empty line
        sep="\n",
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "<< Back", callback_data=banks_cb.new(id="-", action="list")
        )
    )
    return text, markup


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Выберите банк", reply_markup=get_keyboard())


@dp.callback_query_handler(banks_cb.filter(action="list"))
async def query_show_list(query: types.CallbackQuery):
    await query.message.edit_text("Выберите банк", reply_markup=get_keyboard())


@dp.callback_query_handler(banks_cb.filter(action="view"))
async def query_view(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    bank_id = callback_data["id"]

    bank = BANKS.get(bank_id, None)
    if not bank:
        return await query.answer("Неизвестный банк!")

    text, markup = format_bank(bank_id, bank)
    await query.message.edit_text(text, reply_markup=markup)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
