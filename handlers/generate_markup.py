from aiogram import types
from .sqlit import update_status,get_channel_info
from aiogram import types
from misc import dp,bot


def subscription_markup():
    markup = types.InlineKeyboardMarkup()
    data = get_channel_info()
    for d in data:
        markup.add(types.InlineKeyboardButton(text=d[0], url = d[1]))
    markup.add(types.InlineKeyboardButton(text='🥤Я ПОДПИСАЛСЯ🥤', callback_data=f'call_check'))
    return markup


async def check_subscription(user_id):
    data = get_channel_info()
    flag = 1

    for d in data:
        print(d[2])
        proverka = (await bot.get_chat_member(chat_id=d[2], user_id=user_id)).status
        if proverka == 'member' or proverka == 'administrator' or proverka == 'creator':
            pass
        else:
            flag = 0

    if flag == 1:  # Человек прошел все 3 проверки
        update_status(user_id)
        return True
    else:
        return False

def open_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1_1 = types.KeyboardButton('Поиск фильмов 🔎')
    button_1_2 = types.KeyboardButton('Фильм из ТикТок 🎬')
    button_2_1 = types.KeyboardButton('Новинки 🎊')
    button_2_2 = types.KeyboardButton('Избранное ❤️')
    button_3 = types.KeyboardButton('Информация ⚙️')
    button_4 = types.KeyboardButton('FAQ ?')

    markup.add(button_1_1,button_1_2)
    markup.add(button_2_1,button_2_2)
    markup.add(button_3)
    markup.add(button_4)

    return markup