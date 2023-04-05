from aiogram import types
from misc import dp, bot
import sqlite3
from .sqlit import info_members, delite_user,get_data_tag, sbros_all_tag,get_channel_info


import asyncio
from datetime import timedelta, datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.utils.exceptions import BotBlocked, ChatNotFound

ADMIN_ID_1 = 494588959  # Cаня (удалить после разработки)
ADMIN_ID_2 = 5502624024


ADMIN_ID = [ADMIN_ID_1, ADMIN_ID_2]



class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()
    step_q = State()
    step_regbutton = State()



@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_key = types.InlineKeyboardButton(text='Ключи ТикТок', callback_data='set_key')
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_e = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')
        bat_j = types.InlineKeyboardButton(text='База db', callback_data='baza')
        bat_j_1 = types.InlineKeyboardButton(text='Базу txt', callback_data='baza1')
        bat_setin = types.InlineKeyboardButton(text='Добавить канал', callback_data='settings')
        bat_ref = types.InlineKeyboardButton(text='Рефералка', callback_data='ref_ka')
        markup.add(bat_key)
        markup.add(bat_ref)
        markup.add(bat_j,bat_j_1)
        markup.add(bat_a, bat_e)
        markup.add(bat_setin)

        data = get_channel_info()
        for d in data:
            markup.add(types.InlineKeyboardButton(text=f"{d[0]} 👈🏻 удалить", callback_data=f'ch_{d[2]}'))

        await bot.send_message(message.chat.id, 'Выполнен вход в админ панель', reply_markup=markup)


@dp.callback_query_handler(text='ref_ka')
async def ref_ka(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_key = types.InlineKeyboardButton(text='Сбросить все тэги', callback_data='sbros')
    markup.add(bat_key)

    data = get_data_tag()
    answ = ""
    for d in data:
        d3 = d[1] + d[2] #Всего пользователей на метке
        a = f"<b>{d[0]}</b> : <i>({d3} / {d[2]})</i> \n"
        answ+= a


    await bot.send_message(chat_id=call.message.chat.id, text = f"""Данные указаны в виде
<i>Реф. Метка : (всего юзеров / юзеров на ОП)\n</i>
{answ}""",reply_markup=markup)
    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(text='sbros')
async def sbros(call: types.callback_query):
    try:
        sbros_all_tag()
        await call.message.answer("Успешно")
    except:
        await call.message.answer("Произошла ошибка при сбрасывании тэгов")
    await bot.answer_callback_query(call.id)







@dp.callback_query_handler(text='baza')
async def baza(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        a = open('server.db', 'rb')
        await bot.send_document(chat_id=call.message.chat.id, document=a)
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(text='baza1')
async def baza1(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        db = sqlite3.connect('server.db')
        sql = db.cursor()
        a = sql.execute(f"SELECT * FROM user_time").fetchall()
        f = open('id.txt', 'w')
        for id in a:
            f.write(f'{id[0]}, ')
        f.close()
        a = open('id.txt', 'rb')
        await bot.send_document(chat_id=call.message.chat.id, document=a)
        f.close()
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(text='list_members')  # АДМИН КНОПКА ТРАФИКА
async def check(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        a = info_members()  # Вызов функции из файла sqlit
        await bot.send_message(call.message.chat.id, f'Количество пользователей: {a}')
    await bot.answer_callback_query(call.id)


########################  Рассылка  ################################
@dp.callback_query_handler(text='write_message')  # АДМИН КНОПКА Рассылка пользователям
async def check(call: types.callback_query, state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='Да', callback_data='rasl_yes')
    bat1 = types.InlineKeyboardButton(text='нет', callback_data='rasl_no')
    murkap.add(bat0, bat1)

    await bot.send_message(call.message.chat.id, 'Будем чистить базу от блокированных? (может занять больше время)', reply_markup = murkap)
    await bot.answer_callback_query(call.id)



@dp.callback_query_handler(text_startswith='rasl_')  # АДМИН КНОПКА Рассылка пользователям
async def check(call: types.callback_query, state: FSMContext):
    if call.data == 'rasl_yes':
        await state.update_data(rasl = 'yes')
    else:
        await state.update_data(rasl = 'no')

    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                           reply_markup=murkap)
    await st_reg.step_q.set()
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(text='otemena', state='*')
async def otmena_12(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Отменено')
    await state.finish()
    await bot.answer_callback_query(call.id)


@dp.message_handler(state=st_reg.step_q,
                    content_types=['text', 'photo', 'video', 'video_note', 'voice'])  # Предосмотр поста
async def redarkt_post(message: types.Message, state: FSMContext):
    await st_reg.st_name.set()
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
    bat2 = types.InlineKeyboardButton(text='Добавить кнопки', callback_data='add_but')
    murkap.add(bat1)
    murkap.add(bat2)
    murkap.add(bat0)

    await message.copy_to(chat_id=message.chat.id)
    q = message
    await state.update_data(q=q)

    await bot.send_message(chat_id=message.chat.id, text='Пост сейчас выглядит так 👆', reply_markup=murkap)


# НАСТРОЙКА КНОПОК
@dp.callback_query_handler(text='add_but', state=st_reg.st_name)  # Добавление кнопок
async def addbutton(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id, text='Отправляй мне кнопки по принципу Controller Bot')
    await st_reg.step_regbutton.set()
    await bot.answer_callback_query(call.id)


@dp.message_handler(state=st_reg.step_regbutton, content_types=['text'])  # Текст кнопок в неформате
async def redarkt_button(message: types.Message, state: FSMContext):
    arr3 = message.text.split('\n')
    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками

    massiv_text = []
    massiv_url = []

    for but in arr3:
        new_but = but.split('-')
        massiv_text.append(new_but[0][:-1])
        massiv_url.append(new_but[1][1:])
        bat9 = types.InlineKeyboardButton(text=new_but[0][:-1], url=new_but[1][1:])
        murkap.add(bat9)

    try:
        data = await state.get_data()
        mess = data['q']  # ID сообщения для рассылки

        await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=mess.message_id,
                               reply_markup=murkap)

        await state.update_data(text_but=massiv_text)  # Обновление Сета
        await state.update_data(url_but=massiv_url)  # Обновление Сета

        murkap2 = types.InlineKeyboardMarkup()  # Клавиатура - меню
        bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
        murkap2.add(bat1)
        murkap2.add(bat0)

        await bot.send_message(chat_id=message.chat.id, text='Теперь твой пост выглядит так☝', reply_markup=murkap2)


    except:
        await bot.send_message(chat_id=message.chat.id, text='Ошибка. Отменено')
        await state.finish()


# КОНЕЦ НАСТРОЙКИ КНОПОК


@dp.callback_query_handler(text='send_ras', state="*")  # Рассылка
async def fname_step(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    data = await state.get_data()
    mess = data['q']  # Сообщения для рассылки
    rasl = data['rasl']  # Сообщения для рассылки

    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками
    try:  # Пытаемся добавить кнопки. Если их нету оставляем клаву пустой
        text_massiv = data['text_but']
        url_massiv = data['url_but']
        for t in text_massiv:
            for u in url_massiv:
                bat = types.InlineKeyboardButton(text=t, url=u)
                murkap.add(bat)
                break

    except:
        pass

    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    users = sql.execute("SELECT id FROM user_time").fetchall()
    bad = 0
    good = 0
    delit = 0
    await bot.send_message(call.message.chat.id,
                           f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")

    if rasl == 'yes':
        for i in users:
            await asyncio.sleep(0.03)
            try:
                await mess.copy_to(i[0], reply_markup=murkap)
                good += 1
            except (BotBlocked, ChatNotFound):
                try:
                    delite_user(i[0])
                    delit += 1

                except:
                    pass
            except:
                bad += 1
    else:
        for i in users:
            await asyncio.sleep(0.03)
            try:
                await mess.copy_to(i[0], reply_markup=murkap)
                good += 1
            except:
                bad += 1

    await bot.send_message(
        call.message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Удалено пользователей:</b> <code>{delit}</code>\n"
        f"<b>Произошло ошибок:</b> <code>{bad}</code>",
        parse_mode="html"
    )
    await bot.answer_callback_query(call.id)
#########################################################
