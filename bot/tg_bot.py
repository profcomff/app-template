import sys
import logging
import asyncio

import UserInfo
import keyboard

from config import token, dict_links
from aiogram import types, Dispatcher, Bot, F
from aiogram.filters import CommandStart
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from init_model import model_pipeline, data_base

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
bot = Bot(token=token)


class BotMemory(StatesGroup):
    user_info = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text=f"Привет, {message.from_user.full_name}! Я, OnbordingQA-Bot!",
        reply_markup=keyboard.kb
        )


@dp.message(F.text.lower() == "твой фф")
async def command_tff_handler(message: Message) -> None:
    await message.answer(
        text="Приложение Твой ФФ!",
        reply_markup=keyboard.kb
    )


@dp.message(F.text.lower() == "end")
async def command_tff_handler(message: Message) -> None:
    await message.answer(text="You kiled me!")
    await message.answer_sticker(
        sticker="CAACAgIAAxkBAAEL12tmDbNK4-uH1aVvkki-NKZKxZSceQACAhYAAsjfaElONyIfo2wJgzQE"
        )
    await dp.stop_polling()


@dp.message(F.content_type == types.ContentType.TEXT)
async def message_handler(message: Message, state: FSMContext) -> None:
    question = message.text
    user = UserInfo(question, 0)
    answer_bot = user.correction_answer(data_base, model_pipeline)

    await state.set_state(BotMemory.user_info)
    await state.update_data(user_info=user)

    await message.answer(text=f"{answer_bot}")
    await message.answer(text='Вас устроил овет?', reply_markup=keyboard.ikb_2)


@dp.callback_query(BotMemory.user_info, F.data == "Да")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext) -> None:
  data = await state.get_data()
  await callback.bot.delete_message(
      chat_id=callback.from_user.id, message_id=callback.message.message_id
      )
  
  contexts = data['user_info'].contexts
  links_list = [dict_links[contexts[i].page_content] for i in range(3)]
  await callback.message.answer(
      text="Также может быть полезно:", reply_markup=keyboard.keyboard_links(links_list)
      )


@dp.callback_query(BotMemory.user_info, F.data == "Нет")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext) -> None:
  data = await state.get_data()
  user = data['user_info']
  user.number_context += 1

  if user.number_context < 3:

    await callback.bot.delete_message(
        chat_id=callback.from_user.id, message_id=callback.message.message_id
        )
    await callback.bot.delete_message(
        chat_id=callback.from_user.id, message_id=callback.message.message_id-1
        )
    
    user.search_answer()
    answer_bot = user.correction_answer()

    await callback.message.answer(text=answer_bot)
    await callback.message.answer(text='Лучше?', reply_markup=keyboard.ikb_2)

    await state.update_data(user_info=user)

  else:

    await callback.bot.delete_message(
        chat_id=callback.from_user.id, message_id=callback.message.message_id
        )
    await callback.bot.delete_message(
        chat_id=callback.from_user.id, message_id=callback.message.message_id-1
        )
    
    await callback.message.answer(text='Ничего не нашлось...')
    await callback.message.answer_sticker(
        sticker="CAACAgIAAxkBAAEL6DdmGpb0WZzGRoY9afNs1uP00M3OtwACGxUAAr9-aElhR1Vxwa8PXTQE"
        )
    

@dp.callback_query(BotMemory.user_info, F.data == "Дополнить")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext) -> None:
  data = await state.get_data()
  user = data['user_info']

  await callback.bot.delete_message(
      chat_id=callback.from_user.id, message_id=callback.message.message_id
      )
  await callback.bot.delete_message(
      chat_id=callback.from_user.id, message_id=callback.message.message_id-1
      )
  
  contexts = user.contexts
  addition = contexts[user.number_context].page_content.replace(';', '\n')
  await callback.message.answer(text=addition)

  links_list = [dict_links[contexts[i].page_content] for i in range(3)]
  await callback.message.answer(
      text="Также может быть полезно:", reply_markup=keyboard.keyboard_links(links_list)
      )


async def main() -> None:
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
