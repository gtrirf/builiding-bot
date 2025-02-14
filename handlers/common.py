from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.inline import start_keyboard
from states.states import Form
import logging

# @dp.callback_query_handler(lambda c: c.data == "main_menu", state="*")
# async def main_menu(call: types.CallbackQuery, state: FSMContext):
#     """Ortga qaytish tugmasi bosilganda bosh menyuga o'tish."""
#     await call.message.edit_text("Ассалому алайкум!\nУшбу бот орқали сизга Тошкент "
#         "вилоятининг Паркент туманидаги турар жой мажмуалари "
#         "тўғрисида маълумот берилади.", reply_markup=start_keyboard())
#     await Form.MAIN.set()

@dp.callback_query_handler(lambda c: c.data == "main_menu", state="*")
async def back_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    """Bosh menyuga qaytganda rasmlar va tugmalar xabarlarini o‘chirib tashlash."""
    user_data = await state.get_data()
    message_ids = user_data.get("gallery_messages", [])
    data = await state.get_data()
    location_messages = data.get("location_messages", [])

    for msg_did in message_ids:
        try:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=msg_did)
        except Exception as e:
            logging.error(f"Xabarni o‘chirishda xatolik: {e}")

    await state.update_data(gallery_messages=[])  # Saqlangan xabarlarni tozalash

    # Bosh menyu xabarini yuborish
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="*Ушбу бот орқали сизга Тошкент "
        "вилоятининг Паркент туманидаги турар жой мажмуалари "
        "тўғрисида маълумот берилади.*",
        parse_mode="Markdown",
        reply_markup=start_keyboard())


# @dp.callback_query_handler(lambda c: c.data == 'back', state="*")
# async def go_back(call: types.CallbackQuery, state: FSMContext):
#     """Bitta oldingi state'ga qaytish."""
#     data = await state.get_data()
#     last_state = data.get("last_state")  # Oxirgi saqlangan state
#
#     if last_state:
#         await state.set_state(last_state)  # Oldingi state'ga qaytish
#         await call.answer("🔙 Orqaga qaytdingiz.")  # Foydalanuvchiga xabar yuborish
#     else:
#         await call.answer("⏪ Ortga qaytib bo‘lmaydi.")  # Agar oldingi state bo‘lmasa
#
#
# async def save_last_state(state: FSMContext):
#     """State o‘zgarganda oldingi state'ni saqlab borish."""
#     current_state = await state.get_state()
#     if current_state:
#         await state.update_data(last_state=current_state)
