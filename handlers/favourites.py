from aiogram import types
from misc import dp, bot
import requests
from .sqlit import reg_fav,delite_all_fav
link_d = 'https://207734375553.svetacdn.in/FfABlTZmDpBH/'

@dp.callback_query_handler(text_startswith='del_fav')  # Нажал кнопку Добавить избранное
async def del_favorite(call: types.callback_query):
    try:
        await call.message.answer("Избранные успешно очищены ")
        delite_all_fav()
    except:
        await call.message.answer("Удаление не выполнено. Повторите попытку")
    await bot.answer_callback_query(call.id)



@dp.callback_query_handler(text_startswith='iz_')  # Нажал кнопку Добавить избранное
async def start_favorite(call: types.callback_query):
    try:
        user_id = call.message.chat.id
        link = (link_d + call.data[3:])
        reg_fav(user_id,link,call.message.caption[:20])
        await call.message.answer('Фильм добавлен в избранное')
        await bot.answer_callback_query(call.id)
    except:
        try:
            user_id = call.message.chat.id
            link = (link_d + call.data[3:])
            reg_fav(user_id, link, call.message.text[:20])
            await call.message.answer('Фильм добавлен в избранное')
            await bot.answer_callback_query(call.id)
        except:
            await call.message.answer('Произошла ошибка')




