from aiogram import Dispatcher, Bot, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import keyboard
import states
import states as st
import config
import db

storage = MemoryStorage()
bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=storage)


async def on_startup(arg):
    """"""
    await db.connect_db()


@dp.message_handler(commands=['start'], state='*')
async def start_chat(message, state: FSMContext):
    """User start chat"""

    if await db.ifUserIsWorker(message):

        await state.set_state(await st.UserStates.worker_start_state.set())
        await message.answer(f"Добро пожаловать {message.from_user.first_name}!\nВам даны права разработчика.\nДля"
                             f" начала рекомендуем ознакомиться с правилами и принципами работы бота.\n"
                             f"Удачной работы!", reply_markup = keyboard.get_worker_start_kbd())
    else:

        await st.UserStates.user_start_state.set()
        await message.answer(f"Здаравствуйте {message.from_user.first_name}!\nВас преветствует LabaHelperBot.",
                             reply_markup=keyboard.get_user_start_kbd())


@dp.message_handler(content_types=['text'], state=st.UserStates.user_start_state)
async def first_user_page_message(message, state: FSMContext):
    """User choose bot abilities"""
    if message.text == 'Заказать лабу':
        await st.UserStates.user_choose_language_state.set()
        await message.answer(f"Выберите язык программирования", reply_markup = keyboard.get_languages_kbd())


    elif message.text == 'Помощь':
        #TODO
        pass
    elif message.text == 'Мои заказы':
        #TODO
        pass
    else:
        await message.answer("Извините, но я вас не понимаю!", reply_markup=keyboard.get_user_start_kbd())


@dp.message_handler(content_types=['text'], state=st.UserStates.user_choose_language_state)
async def first_user_page_message(message, state: FSMContext):
    if message.text in config.languages != -1:
        async with state.proxy() as data:
            data['language'] = message.text
            await st.UserStates.user_send_photo_state.set()
            await message.answer(f"Вы выбрали {data['language']}\nОтправте фотографию вашего условия.")
    else:
        await message.answer("Я тебя не понимаю!\nПопробуй ещё раз!", reply_markup = keyboard.get_languages_kbd())

# @dp.message_handler(commands=['help'], state='*')
# async def help_message(message):
#     """Help menu"""
#
#     await message.answer("There is must be help box!")
#
#
# @dp.message_handler(commands=['cancel'], state='*')
# async def cancel_command(message, state: FSMContext):
#     """Help menu"""
#
#     await state.finish()
#     await message.answer("Canceled!", reply_markup=keyboard.get_start_kbd())
#
#
# @dp.message_handler(commands=['rules'])
# async def rules(message):
#     """Show rules"""
#
#     await message.answer("There will be rules!")
#
#
# @dp.message_handler()
# async def start_menu(message):
#     """Start menu"""
#
#     if message.text == "Заказать лабу":
#         if await database.check_order_existence(message):
#             await message.answer("Choose language!", reply_markup=keyboard.get_language_kbd())
#             await states.UserStates.inter_language.set()
#         else:
#             await message.answer("U already have order!")
#     elif message.text == "Правила":
#         """Rules"""
#
#         await rules(message)
#     elif message.text == "Помощь":
#         """Help box"""
#
#         await help_message(message)
#     else:
#         await bot.send_message(message.chat.id, "I don't understand you!")
#
#
# @dp.message_handler(content_types=['text'], state=states.UserStates.inter_language)
# async def choose_language(message, state: FSMContext):
#     """User choose language"""
#
#     if list.languages.count(message.text) == 1:
#         async with state.proxy() as data:
#             data['language'] = message.text
#         await states.UserStates.inter_condition.set()
#         await message.answer("Enter condition!", reply_markup=keyboard.clear_kbd())
#     elif message.text == "Cancel":
#         await cancel_command(message, state)
#     else:
#         await message.answer("I don't understand u. Choose one of below languages!")
#
#
# @dp.message_handler(content_types=['text'], state=states.UserStates.inter_condition)
# async def inter_condition(message, state: FSMContext):
#     async with state.proxy() as data:
#         data['condition'] = message.text
#     await states.UserStates.condition_check.set()
#     await message.answer(f"Your condition is:\n{data['condition']}\n\nDo you want to change it?(Да/ Нет)",
#                          reply_markup=keyboard.yes_no_kbd())
#
#
# @dp.message_handler(content_types=['text'], state=states.UserStates.condition_check)
# async def approve_condition(message, state: FSMContext):
#     markup = types.ReplyKeyboardRemove()
#
#     if message.text == "Да":
#         await states.UserStates.inter_condition.set()
#         await message.answer("Inter your condition:", reply_markup=markup)
#     elif message.text == "Нет":
#         await message.answer("Is there smth special?")
#         await states.UserStates.addition_condition_check.set()
#     else:
#         await message.answer("I don't understand u!")
#
#
# @dp.message_handler(content_types=['text'], state=states.UserStates.addition_condition_check)
# async def special_condition_check(message, state):
#     markup = types.ReplyKeyboardRemove()
#     await states.UserStates.addition_condition.set()
#     if message.text == "Да":
#         await message.answer("Enter special condition:", reply_markup=markup)
#     elif message.text == "Нет":
#         await special_condition(message, state)
#     else:
#         await message.answer("I don't understand u!")
#
#
# @dp.message_handler(content_types=['text'], state=states.UserStates.addition_condition)
# async def special_condition(message, state):
#     async with state.proxy() as data:
#         data['special'] = message.text
#     await message.answer(f"Your order:\n\nLanguage: {data['language']}\nCondition: {data['condition']}\n"
#                          f"Special: {data['special']}\n\nDo u want to send it?", reply_markup=keyboard.yes_no_kbd())
#     await states.UserStates.send_order.set()
#
#
# @dp.message_handler(content_types=['text'], state=states.UserStates.send_order)
# async def send_order(message, state):
#     if message.text == "Да":
#         async with state.proxy() as data:
#             await database.add_order(message, data)
#         await message.answer("Sent", reply_markup=keyboard.get_start_kbd())
#         await state.finish()
#     elif message.text == "Нет":
#         await cancel_command(message, state)
#     else:
#         await message.answer("I don't understand u!")
#
#
# @dp.channel_post_handler()
# async def channel_message(message):
#     info = []
#     info = message.text.split('\n')
#     await bot.send_message(info[0], f"Order: {info[1]}\n\nSuggested price: {info[3]}",
#                            reply_markup=keyboard.get_accept_ikb())


# @dp.callback_query_handler(text="accept_price")
# async def pay(callback: types.CallbackQuery, state: FSMContext):
#     await callback.message.answer("pay")


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
