from aiogram import types
from misc import dp, bot
import asyncio
from .sqlit import delit_trafik
from .generate_markup import check_subscription,subscription_markup,open_markup
file_id = "AgACAgIAAxkBAAMNZBm6HQ0cnJAlQe0nbtPkPslsVUkAAp_HMRtggdBIUk3z6YYFxcoBAAMCAANzAAMvBA"

@dp.callback_query_handler(lambda call: True, state = '*')
async def answer_push_inline_button(call):
    if call.data == 'call_check':
        if await check_subscription(call.from_user.id) == True:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await call.message.answer("""<b>Привет, киноман!</b>

Какой фильм или сериал ты хочешь посмотреть? Напиши мне название!""", reply_markup=open_markup())
        else:
            await bot.send_photo(call.message.chat.id, photo=file_id,caption="""<b>⭐️ Для полноценного использования КИНОБОТА, подпишитесь на наших спонсоров:</b>""",reply_markup=subscription_markup())

    await bot.answer_callback_query(call.id)


    if call.data[0:3] == 'ch_':
        try:
            delit_trafik(call.data[3:])
            await call.message.answer("Канал успешно удален")
        except:
            await call.message.answer("Произошла ошибка")

