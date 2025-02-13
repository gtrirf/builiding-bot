import asyncio
import json
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.inline import (
    lakeside_purchase_options, lakeside_main_keyboard,
    full_payment_options, discount_payment_options, credit_payment_options
)
from states.states import Form
from aiogram.types import InputFile


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.callback_query_handler(lambda c: c.data == "lakeside_residence", state="*")
async def lakeside_residence_main(call: types.CallbackQuery, state: FSMContext):
    """Lakeside Residence haqida ma'lumot beruvchi asosiy menyu."""
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="турар жой мажмуаси Тошкент вилояти, Паркент тумани «Истиқбол» МФЙ Алишер Навоий кўчаси "
        "48-уй ҳудудида жойлашган бўлиб, ушбу мажмуада 7 қаватли турар уй-жой бинолари мавжуд.",
        reply_markup=lakeside_main_keyboard(),
    )
    await Form.LAKESIDE_MAIN.set()


@dp.callback_query_handler(lambda c: c.data == "lakeside_residence_under_construction", state=Form.LAKESIDE_MAIN)
async def lakeside_residence_buy(call: types.CallbackQuery, state: FSMContext):
    """Sotib olish uchun menyu."""
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Сотиб олиш учун",
        reply_markup=lakeside_purchase_options()
    )
    await Form.LAKESIDE_READY.set()


@dp.callback_query_handler(lambda c: c.data == "full_payment_lakeside", state=Form.LAKESIDE_READY)
async def lakeside_residence_full_payment(call: types.CallbackQuery, state: FSMContext):
    """100% to'lov asosida sotib olish."""
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='100%лик тўлов асосида сотиб олиш',
        reply_markup=full_payment_options()
    )
    await Form.LAKESIDE_100PERSENT.set()


@dp.callback_query_handler(lambda c: c.data == "discount_payment_lakeside", state=Form.LAKESIDE_READY)
async def lakeside_residence_discount(call: types.CallbackQuery, state: FSMContext):
    """5% chegirma asosida sotib olish."""
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="5%лик чегирма асосида сотиб олиш",
        reply_markup=discount_payment_options()
    )
    await Form.LAKESIDE_5PERSENT.set()


@dp.callback_query_handler(lambda c: c.data == "credit_payment_lakeside", state=Form.LAKESIDE_READY)
async def lakeside_residence_credit(call: types.CallbackQuery, state: FSMContext):
    """Kredit asosida sotib olish."""
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Кредит асосида сотиб олиш',
        reply_markup=credit_payment_options()
    )
    await Form.LAKESIDE_CREDIT.set()


@dp.callback_query_handler(lambda c: c.data == "lakeside_residence_gallery", state=Form.LAKESIDE_MAIN)
async def send_lakeside_gallery(call: types.CallbackQuery, state: FSMContext):
    """Lakeside uchun foto galereya."""
    await call.answer()
    try:
        with open("image_path.json", "r", encoding="utf-8") as file:
            IMAGE_PATHS = json.load(file)

        media_group = []
        message_ids = []  # Yuborilgan xabar ID'larini saqlash
        for key, image_path in IMAGE_PATHS.items():
            if key.startswith("lakeside"):
                photo = types.InputFile(image_path)
                media_group.append(types.InputMediaPhoto(photo))

        if media_group:
            messages = await bot.send_media_group(chat_id=call.message.chat.id, media=media_group)
            message_ids.extend([msg.message_id for msg in messages])  # Rasmlar ID larini saqlash

        menu_msg = await bot.send_message(
            chat_id=call.message.chat.id,
            text="📸 *Lakeside Foto Galereya* 🏡",
            parse_mode="Markdown",
            reply_markup=lakeside_main_keyboard()
        )

        message_ids.append(menu_msg.message_id)
        await state.update_data(gallery_messages=message_ids)
    except Exception as e:
        logging.error(f"JSON faylni o'qishda xatolik: {e}")


@dp.callback_query_handler(lambda c: c.data == "lakeside_residence_location", state=Form.LAKESIDE_MAIN)
async def send_lakeside_location(call: types.CallbackQuery, state: FSMContext):
    """Lakeside joylashuvi."""
    await call.answer()

    location = {'latitude': 41.312336, 'longitude': 69.278707}  # Lakeside koordinatalari

    await bot.send_location(
        chat_id=call.message.chat.id,
        latitude=location['latitude'],
        longitude=location['longitude']
    )

    await bot.send_message(
        chat_id=call.message.chat.id,
        text="📍 *Lakeside Residence Joylashuvi*",
        parse_mode="Markdown",
        reply_markup=lakeside_main_keyboard()
    )


# 100% to'lov asosida xonalar uchun handlerlar
@dp.callback_query_handler(lambda c: c.data.startswith("full_payment_"), state=Form.LAKESIDE_100PERSENT)
async def lakeside_full_payment_rooms(call: types.CallbackQuery, state: FSMContext):

    try:
        await bot.send_message(
            chat_id=call.message.chat.id,
            caption=f"🏠 *100%лик тўлов асосида сотиб олиш*",
            parse_mode="Markdown",
            reply_markup=full_payment_options(),
        )
    except Exception as e:
        logging.error(f"Rasm yuborishda xatolik: {e}")



data = {
    "credit_56_98": "images/Кредит/56.98/56,98 kredit.jpg",
    "credit_57_49": "images/Кредит/57.49/57,49 kredit.jpg",
    "credit_62_00": "images/Кредит/62.00/62,00 kredit.jpg",
    "credit_80_26": "images/Кредит/80.26/80,26 kredit.jpg",
    "credit_83_57": "images/Кредит/83.57/83,57 kredit.jpg",
    "credit_87_94": "images/Кредит/87.94/87,94 kredit.jpg",
    "full_payment_56_98": "images/100лик/56.98/56,98 100lik.jpg",
    "full_payment_57_49": "images/100лик/57.49/57,49 100lik.jpg",
    "full_payment_62_00": "images/100лик/62.00/62,00 100lik.jpg",
    "full_payment_80_26": "images/100лик/80.26/80,26 100lik.jpg",
    "full_payment_83_57": "images/100лик/83.57/83,57 100lik.jpg",
    "full_payment_87_94": "images/100лик/87.94/87,94 100lik.jpg",
    "discount_56_98": "images/5лик/56.98/56,98 5lik.jpg",
    "discount_57_49": "images/5лик/57.49/57,49 5lik.jpg",
    "discount_62_00": "images/5лик/62.00/62,00 5lik.jpg",
    "discount_80_26": "images/5лик/80.26/80,26 5lik.jpg",
    "discount_83_57": "images/5лик/83.57/83,57 5lik.jpg",
    "discount_87_94": "images/5лик/87.94/87,94 5lik.jpg",
}

IMAGE_NOT_FOUND_MSG = "❌ Tanlangan rasm mavjud emas: {}"
IMAGE_SEND_ERROR_MSG = "❌ Rasm yuborishda xatolik yuz berdi."
NO_IMAGE_FOUND_MSG = "❌ Ushbu tanlov uchun rasm topilmadi."

@dp.callback_query_handler(lambda c: c.data in data, state=Form.LAKESIDE_PHOTO)
async def send_image(callback_query: types.CallbackQuery, state: FSMContext):
    import os
    import logging

    current_state = await state.get_state()
    logger.info(f"Foydalanuvchi hozirgi state: {current_state}")

    image_path = data.get(callback_query.data)

    if not image_path:
        logger.error(f"Ushbu callback_data bo'yicha rasm topilmadi: {callback_query.data}")
        await callback_query.message.answer(NO_IMAGE_FOUND_MSG)
        await callback_query.answer()
        return


    if not os.path.exists(image_path):
        logger.error(f"Rasm topilmadi: {image_path}")
        await callback_query.message.answer(IMAGE_NOT_FOUND_MSG.format(callback_query.data))
        await callback_query.answer()
        return

    try:
        photo = InputFile(image_path)
        await bot.send_photo(chat_id=callback_query.message.chat.id, photo=photo, caption="Bu siz tanlagan variant.")
    except Exception as e:
        logger.error(f"Rasm yuborishda xatolik: {str(e)}")
        await callback_query.message.answer(IMAGE_SEND_ERROR_MSG)
    finally:
        await callback_query.answer()


# def send_photo(update: Update, context: CallbackContext) -> None:
#     keyboard = [[InlineKeyboardButton(key, callback_data=key)] for key in data.keys()]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text('Rasmlarni tanlang:', reply_markup=reply_markup)
#
# def button_callback(update: Update, context: CallbackContext) -> None:
#     query = update.callback_query
#     query.answer()
#     image_path = data.get(query.data)
#     if image_path:
#         query.message.reply_photo(photo=open(image_path, 'rb'))
#     else:
#         query.message.reply_text("Rasm topilmadi.")
