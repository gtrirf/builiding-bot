from aiogram import types
from keyboards.inline.inline import start_keyboard
from aiogram.dispatcher.filters import Command
from loader import dp

@dp.message_handler(Command('start'), state="*")
async def start(message: types.Message):
    await message.answer(
        "Ассалому алайкум!\nУшбу бот орқали сизга Тошкент "
        "вилоятининг Паркент туманидаги турар жой мажмуалари "
        "тўғрисида маълумот берилади.",
        reply_markup=start_keyboard()
    )
