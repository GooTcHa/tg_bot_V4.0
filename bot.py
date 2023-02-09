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

        await st.UserStates.worker_start_state.set()
        await message.answer(f"Добро пожаловать {message.from_user.first_name}!\nВам даны права разработчика.\nДля"
                             f" начала рекомендуем ознакомиться с правилами и принципами работы бота.\n"
                             f"Удачной работы!", reply_markup=keyboard.worker_start_kbd())
    else:

        await st.UserStates.user_start_state.set()
        await message.answer(f"Здаравствуйте {message.from_user.first_name}!\nВас преветствует LabaHelperBot.",
                             reply_markup=keyboard.user_start_kbd())

############################################################################
###USER PART###############################################################
############################################################################
@dp.message_handler(content_types=['text'], state=st.UserStates.user_start_state)
async def first_user_page_message(message, state: FSMContext):
    """User choose bot abilities"""
    if message.text == 'Заказать лабу':
        await st.UserStates.user_choose_language_state.set()
        await message.answer(f"Выберите язык программирования", reply_markup = keyboard.languages_kbd())


    elif message.text == 'Помощь':
        #TODO
        pass
    elif message.text == 'Мои заказы':
        #TODO
        pass
    else:
        await message.answer("Извините, но я вас не понимаю!", reply_markup=keyboard.user_start_kbd())


@dp.message_handler(content_types=['text'], state=st.UserStates.user_choose_language_state)
async def save_user_language(message, state: FSMContext):
    if message.text in config.languages != -1:
        async with state.proxy() as data:
            data['language'] = message.text
            await st.UserStates.user_send_photo_state.set()
            await message.answer(f"Вы выбрали {data['language']}\nОтправте фотографию вашего условия.",
                                 reply_markup=keyboard.clear_kbd())
    else:
        await message.answer("Я тебя не понимаю!\nПопробуй ещё раз!", reply_markup = keyboard.languages_kbd())


@dp.message_handler(lambda message: not message.photo, state=st.UserStates.user_send_photo_state)
async def user_wrong_photo_message(message, state: FSMContext):
    await message.answer(f"Это не фото! Попробуйте ещё раз!")


@dp.message_handler(content_types=['photo'], state=st.UserStates.user_send_photo_state)
async def save_user_photo_as_photo(message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        data['doc'] = None
        await st.UserStates.user_send_description_state.set()
        await message.answer(f"Фотография условия сохранена!\nОсталось ввести дополнительные сведения"
                             f" о лабораторной: ", reply_markup=keyboard.empty_description_kbd())


@dp.message_handler(content_types=['document'], state=st.UserStates.user_send_photo_state)
async def save_user_photo_as_doc(message, state: FSMContext):
    async with state.proxy() as data:
        data['doc'] = message.document.file_id
        data['photo'] = None
        await st.UserStates.user_send_description_state.set()
        await message.answer(f"Фотография условия сохранена!\nОсталось ввести дополнительные сведения"
                             f" о лабораторной: ", reply_markup=keyboard.empty_description_kbd())


@dp.message_handler(content_types=['text'], state=st.UserStates.user_send_description_state)
async def user_send_description(message, state: FSMContext):
    async with state.proxy() as data:
        data['descr'] = message.text
        await db.saveUserOrder(message, data)
        if data['doc']:
            await bot.send_document(config.main_account, data['doc'], caption=f"{message.chat.id}\n{data}",
                                    reply_markup=keyboard.accept_order_ikb(), caption_entities=f"{message.chat.id}")
        else:
            await bot.send_photo(config.main_account, data['photo'], f"{message.chat.id}\n{data}",
                                 reply_markup=keyboard.accept_order_ikb(), caption_entities=f"{message.chat.id}")
        await message.answer("Ваш заказ сохранён и отправлен на проверку!")


#########################################################################
###WORKER PART##########################################################
#########################################################################


@dp.message_handler(content_types=['text'], state=st.UserStates.worker_start_state)
async def worker_first_message(message, state: FSMContext):
    """User choose bot abilities"""
    if message.text == 'Получить список заказов':
        await message.answer(f"Доступные заказы: ", reply_markup=keyboard.clear_kbd())
        await db.printFreeOrders(message, bot)

    elif message.text == 'Помощь':
        #TODO create help menu
        pass
    elif message.text == 'Mои работы':
        #TODO create work list
        pass
    else:
        await message.answer("Извините, но я вас не понимаю!", reply_markup=keyboard.user_start_kbd())


@dp.callback_query_handler(text='offer_price')
async def offer_price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Предложите свою цену в $:")
    with state.proxy() as data:
        data['order'] = callback.message.caption[1:4]
    await st.UserStates.worker_price_state.set()


@dp.message_handler(content_types=['text'], state=st.UserStates.worker_price_state)
async def send_worker_price(message, state: FSMContext):
    if message.text.isdigit():
        if 5 > int(message.text) > 200:
            # TODO price check
            await message.answer("Цена слишком высокая!")
        else:
            with state.proxy() as data:
                user = await db.get_user_id(data['order'])
                await bot.send_message(user, f"На ваш заказ №{data['order']} пришло предложение цены: {message.text}$",
                                       reply_markup=keyboard.user_accept_price_ikb())
                await db.save_offer(data['order'], message.chat.id, int(message.text))
                await message.answer("Ваше предложение было отправлено")
########################################################################
###MY PART#############################################################
########################################################################


@dp.callback_query_handler(text='accept_order')
async def accept_order(callback: types.CallbackQuery, state: FSMContext):
    print(callback.message)

    await db.accept_order(int(callback.message.caption.split('\n')[0]), bot)


@dp.callback_query_handler(text='decline_order')
async def decline_order(callback: types.CallbackQuery, state: FSMContext):
    pass
    #TODO


@dp.callback_query_handler(text='ban_user')
async def ban_user(callback: types.CallbackQuery, state: FSMContext):
    pass
    #TODO


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
