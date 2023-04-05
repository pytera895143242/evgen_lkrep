import sqlite3
import json

def reg_user(id,ref):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(""" CREATE TABLE IF NOT EXISTS user_time (
        id BIGINT,
        ref,
        status
        ) """)

    sql.execute(f"SELECT id FROM user_time WHERE id ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?,?)", (id, ref, '0'))
        db.commit()

    sql.execute(""" CREATE TABLE IF NOT EXISTS name_tag (
            id BIGINT,
            name
            ) """)

    sql.execute(f"SELECT name FROM name_tag WHERE name = 'default'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO name_tag VALUES (?,?)", (1,'default'))
        db.commit()

    sql.execute(f"SELECT name FROM name_tag WHERE name = '{ref}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO name_tag VALUES (?,?)", (1, str(ref)))
        db.commit()



    sql.execute(""" CREATE TABLE IF NOT EXISTS trafik (
                    name,
                    link,
                    user_id
                    ) """)

    db.commit()


    sql.execute(""" CREATE TABLE IF NOT EXISTS tiktok_key (
                    key,
                    file_id,
                    captions,
                    link_film)""")
    db.commit()


    sql.execute(""" CREATE TABLE IF NOT EXISTS favorites (
                        user_id,
                        film_id,
                        name)""")
    db.commit()

def info_members():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f'SELECT COUNT(*) FROM user_time').fetchone()[0]
    return a


def get_data_tag():
    print('rr')
    data = []
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    tags = sql.execute(f'SELECT name FROM name_tag').fetchall()

    for t in tags:
        a0 = sql.execute(f"SELECT COUNT(*) FROM user_time WHERE ref = '{t[0]}' and status = '0'").fetchone()[0]
        a1 = sql.execute(f"SELECT COUNT(*) FROM user_time WHERE ref = '{t[0]}' and status = '1'").fetchone()[0]
        if not ((a0 == 0) and (a1 == 0)):
            data.append([t[0], a0, a1])
    return data

def sbros_all_tag():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE user_time SET status = 'del'")
    db.commit()


def update_status(user_id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE user_time SET status = '1'  WHERE id ='{user_id}'")
    db.commit()


def cheak_traf():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    c1 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel1'").fetchone()[0]
    c2 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel2'").fetchone()[0]
    c3 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel3'").fetchone()[0]
    c4 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel4'").fetchone()[0]
    c5 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel5'").fetchone()[0]
    list = [c1,c2,c3,c4,c5]
    return list

def get_channel_info():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    c1 = sql.execute(f"SELECT * FROM trafik").fetchall()
    return c1


def obnovatrafika1(name,link,chat_id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    chat_id = str(-int(chat_id))
    sql.execute(f"SELECT name FROM trafik WHERE user_id = '{chat_id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", (name,link,chat_id))
        db.commit()

def delit_trafik(chat_id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    sql.execute(f"DELETE FROM trafik WHERE user_id = '{chat_id}'")
    db.commit()


def delite_user(id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f'DELETE FROM user_time WHERE id = "{id}"')
    db.commit()

def reg_tiktok(key = '1' , file_id = 'AgACAgIAAxkBAANZY9vDLeHV3O-NBus0BtIZ3ug6wsEAAk_EMRtsdOFKhetPRh1yK2IBAAMCAANzAAMuBA', captions = '<b>Кот в сапогах 2: Последнее желание [2022 | +16]\n\nРейтинг: 8.563</b>\n\nКот в сапогах потратил восемь из девяти отпущенных ему жизней и теперь отправляется в новое приключение, чтобы отыскать мифическое Последнее желание и восстановить свои жизни.', link_film = 'https://207734375553.svetacdn.in/FfABlTZmDpBH/movie/63676'): # Регистрация выплатны
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT key FROM tiktok_key WHERE key = '{key}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO tiktok_key VALUES (?,?,?,?)", (str(key),str(file_id),str(captions),str(link_film)))
        db.commit()

def reg_fav(user_id, film_id,name): # Регистрация выплатны
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT user_id FROM favorites WHERE user_id = '{user_id}' AND film_id = '{film_id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO favorites VALUES (?,?,?)", (str(user_id),str(film_id),name))
        db.commit()

def get_info_fav(user_id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT * FROM favorites WHERE user_id = '{user_id}'").fetchall()
    return a


def delite_all_key():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f'DELETE FROM tiktok_key')
    db.commit()

def delite_all_fav():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f'DELETE FROM favorites')
    db.commit()




def get_info_key(key):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT * FROM tiktok_key WHERE key = '{key}'").fetchall()
    return a

def get_info_all_key():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT * FROM tiktok_key").fetchall()
    return a
