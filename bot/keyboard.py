from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo


b_tff = KeyboardButton(text="Твой ФФ", web_app=WebAppInfo(url="https://app.profcomff.com/"))
kb = ReplyKeyboardMarkup(
    keyboard=[[b_tff]], resize_keyboard=True, one_time_keyboard=True
    )

ib_yes = InlineKeyboardButton(text="Yes", callback_data="Да")
ib_no = InlineKeyboardButton(text="No", callback_data="Нет")
ib_dop = InlineKeyboardButton(text="Дополнить", callback_data="Дополнить")
ikb_2 = InlineKeyboardMarkup(inline_keyboard=[[ib_yes, ib_no], [ib_dop]])


def keyboard_links(links_list):
  inline_keyboard=[]
  for item in links_list:
    for name, link in item.items():
      inline_keyboard.append([InlineKeyboardButton(text=name, url=link)])
  return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)