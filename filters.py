from aiogram.filters import Filter
from aiogram import types
from typing import Any


class TypeChatFilter(Filter):
    def __init__(self, chat_type: str) -> None:
        self.chat_type = chat_type

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type == self.chat_type


class IsReplyMessage(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return bool(message.reply_to_message)