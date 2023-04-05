from aiogram import types
from misc import dp, bot
import requests

link = "https://bazon.cc/api/search?token=2da2f4cdca28d21a8ae887738f1f2f7f&"
title = "title={}&"
id_kk = "kp={}&"

#API кинопоиска:
API_KEY = "7a4e9d3d-8838-44fd-8f64-59ad0262be16" #Токен

def gen_movie_link(movie_link):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='🖥 Смотреть фильм', url = movie_link)
    bat_b = types.InlineKeyboardButton(text='⭐️ Добавить в избранное', callback_data=f'iz_{movie_link[46:]}')

    markup.add(bat_a)
    markup.add(bat_b)
    return markup


async def find_m(message):
    try:
        if 'https://www.kinopoisk.ru/' in message.text:
            #print()
            id_k = ((message.text).split('/'))[-2]
            #print(id_k)
            # answer = (requests.get(url=link + id_kk.format(id_k),headers= headers,proxies=random.choice(proxies))).json()  # Запрос по названию
            answer = (requests.get(timeout=2, url=link + id_kk.format(id_k))).json()  # Запрос по названию
            #print('Поиск по id', answer)
        else:
            # answer = (requests.get(url=link + title.format(message.text),headers= headers,proxies=random.choice(proxies))).json()  #Запрос по названию
            # print(link + title.format(message.text))
            answer = (requests.get(url=link + title.format(message.text))).json()  # Запрос по названию

        f = 0
        if len(answer['results']) != 0:
            for i in answer['results']:
                if f > 20:
                    break
                kp_id = i['kinopoisk_id']
                name_movie = i['info']['rus']
                year = i['info']['year']
                translation = i['translation']
                movie_link = i['link']
                previe = f'https://st.kp.yandex.net/images/film_big/{kp_id}.jpg'
                if (translation) != 'Дубляж (Український)' and (translation) != 'Багатоголосий (Український)' and (
                translation) != 'Дубляж (Український)' and (translation) != 'Українська':
                    print(translation)
                    f += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"<a href = '{previe}'>🎥</a> {name_movie} {year}",disable_web_page_preview=False, reply_markup=gen_movie_link(movie_link))
            await message.answer("""Продолжайте писать названия фильмов, мультфильмов или сериалов""")
        else:
            await message.answer("""Вы прислали что то невнятное!
Повторите попытку или отправьте мне ссылку на фильм с сайта https://www.kinopoisk.ru""")
    except:
        print('Ошибка поиска')
