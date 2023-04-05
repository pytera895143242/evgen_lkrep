from aiogram import types
from misc import dp, bot
from .sqlit import get_info_all_key,reg_tiktok,delite_all_key
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class reg_kkey(StatesGroup):
    traf1 = State()
    traf2 = State()
    traf3 = State()
    traf4 = State()


# НАСТРОЙКА КЛЮЧЕЙ
@dp.callback_query_handler(text='set_key')
async def setkey212(call: types.callback_query):
    markup_traf = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='Добавить ключ', callback_data='add_key')
    bat_b = types.InlineKeyboardButton(text='Удалить все ключи', callback_data='delite_key')
    markup_traf.add(bat_a)
    markup_traf.add(bat_b)

    text = ""
    ans = get_info_all_key()
    for a in ans:
        text +=  a[0] + " -- " + f"<a href = '{a[3]}'>" + a[2][0:16] + "..." + "\n\n" + "</a>"

    await bot.send_message(call.message.chat.id, text=f'Список активных ключей:\n\n\n'
                                                      f'{text}',reply_markup=markup_traf,disable_web_page_preview=True)

@dp.callback_query_handler(text='delite_key')
async def addkey212(call: types.callback_query):
    try:
        delite_all_key()
        await call.message.answer("Все ключи успешно удалены")
    except:
        await call.message.answer("Произошла ошибка при удалении ключей")



@dp.callback_query_handler(text='add_key')
async def addkey212(call: types.callback_query):
    await bot.send_message(call.message.chat.id, text=f'1/4 Отправьте ключ')
    await reg_kkey.traf1.set()

@dp.message_handler(state=reg_kkey.traf1, content_types='text')
async def key_obnovlenie1(message: types.Message, state: FSMContext):
    await state.update_data(key = message.text)
    await bot.send_message(message.chat.id, text=f'2/4 Отправьте ссылку на просмотр фильма')
    await reg_kkey.traf2.set()

@dp.message_handler(state=reg_kkey.traf2, content_types='text')
async def key_obnovlenie2(message: types.Message, state: FSMContext):
    await state.update_data(link = message.text)
    await bot.send_message(message.chat.id, text=f'3/4 Отправьте описание к фильму')
    await reg_kkey.traf3.set()

@dp.message_handler(state=reg_kkey.traf3, content_types='text')
async def key_obnovlenie3(message: types.Message, state: FSMContext):
    await state.update_data(caption = message.text)
    await bot.send_message(message.chat.id, text=f'4/4 Обложку к фильму')
    await reg_kkey.traf4.set()

@dp.message_handler(state=reg_kkey.traf4, content_types='photo')
async def key_obnovlenie4(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        key = data['key']
        link = data['link']
        caption = data['caption']
        file_id = message.photo[0].file_id
        reg_tiktok(key,file_id,caption,link)
        await message.answer("Ключ успешно зарегистрирован! ")
    except:
        await message.answer("Произошла ошибка...")

    await state.finish()
