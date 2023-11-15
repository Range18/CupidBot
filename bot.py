from aiogram import types
from main import bot, dp
from aiogram import Router, F
from aiogram import filters
from filters import *
from typing import List
from MyMiddleware import MyMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from config import CHAT_ID, CHANEL_ID

router = Router(name=__name__)

dp.include_router(router)
dp.message.middleware(MyMiddleware())


class Application(StatesGroup):
    create_application_state = State()


create_application_btn = KeyboardButton(text="Сделать заявку")
Keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[create_application_btn]])


@dp.message(filters.Command(commands=['start']))
async def send_welcome(message: types.Message) -> None:
    await message.answer(
        f"Привет {message.from_user.full_name}!\nЕсли хочешь написть, когохочешь найти, просто нажми на кнопку ниже.",
        reply_markup=Keyboard)


@dp.message(TypeChatFilter(chat_type="private"), F.text == create_application_btn.text)
async def press_button(message: types.Message, state: FSMContext):
    await message.answer("Напиши, кого хочешь найти")
    await state.set_state(Application.create_application_state)


@dp.message(TypeChatFilter(chat_type="private"), Application.create_application_state)
async def create_application(message: types.Message, state: FSMContext, album: List[types.Message] = None) -> None:
    if message.media_group_id:
        media_group = []
        for msg in album:
            if msg.photo:
                file_id = msg.photo[-1].file_id
                caption = msg.caption
                media_group.append(types.InputMediaPhoto(media=file_id, caption=caption))
            elif msg.video:
                file_id = msg.video.file_id
                caption = msg.caption
                media_group.append(types.InputMediaVideo(media=file_id, caption=caption))
        msg = await bot.send_media_group(CHAT_ID, media_group)
        btn = InlineKeyboardButton(text="Разместить", callback_data=str(msg[0].message_id))
    else:
        msg = await message.copy_to(CHAT_ID)
        btn = InlineKeyboardButton(text="Разместить", callback_data=str(msg.message_id))
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    await bot.send_message(CHAT_ID,
                           f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>," + (
                               f" @{message.from_user.username}," if message.from_user.username else "") + f" (#ID{message.from_user.id})",
                           reply_markup=markup)
    await message.answer("Заявка принята, жди свою запись в канале @LoveSesc🥰")
    await state.clear()


@dp.callback_query()
async def post(callback_query: types.CallbackQuery) -> None:
    i = int(callback_query.data)
    media_group = []
    while True:
        msg = await bot.forward_message(CHAT_ID, CHAT_ID, i,
                                        disable_notification=True)
        if msg.photo:
            file_id = msg.photo[-1].file_id
            caption = msg.caption
            media_group.append(types.InputMediaPhoto(media=file_id, caption=caption))
        elif msg.video:
            file_id = msg.video.file_id
            caption = msg.caption
            media_group.append(types.InputMediaVideo(media=file_id, caption=caption))
        else:
            await msg.delete()
            break
        await msg.delete()
        i += 1
    if len(media_group) != 0:
        await bot.send_media_group(CHANEL_ID, CHAT_ID, media_group)
    else:
        await bot.copy_message(CHANEL_ID, CHAT_ID, i)
