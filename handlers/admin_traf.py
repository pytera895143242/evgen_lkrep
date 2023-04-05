from .sqlit import info_members,cheak_traf,obnovatrafika1
from aiogram import types
from misc import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class reg_trafik(StatesGroup):
    traf1 = State()
    traf2 = State()
    traf3 = State()


# НАСТРОЙКА ТРАФИКА
@dp.callback_query_handler(text='settings')
async def baza12(call: types.callback_query):
    await bot.send_message(call.message.chat.id, text="""Введите данные о новом канале в формате:
ИМЯ КАНАЛА - ССЫЛКА - ID КАНАЛА""",parse_mode='html')
    await reg_trafik.traf1.set()
    await bot.answer_callback_query(call.id)

@dp.message_handler(state=reg_trafik.traf1, content_types='text')
async def traf_obnovlenie1(message: types.Message, state: FSMContext):
    data = (message.text.split(' - '))
    obnovatrafika1(data[0],data[1],data[2])
    await state.finish()
    await message.answer("Успешно")

