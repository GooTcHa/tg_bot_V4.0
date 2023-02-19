from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import uuid

import logging
import keyboard
import states as st
import config
import db


storage = MemoryStorage()
bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


@dp.message_handler(commands=['start'], state='*')
async def start_chat(message, state: FSMContext):
    """User start chat"""
    if len(message.text.split(" ")) == 2:
        order = message.text.split(" ")[1]
        invoice = await db.get_order_invoice(message.chat.id, order)
        arr = await config.crypto.get_invoices(status='paid', count=20)
        a1 = list(filter(lambda x: x.invoice_id == invoice, arr))
        if a1 == ():
            await message.answer(f"Вы пока что не оплатили заказ!")
        else:
            order = await db.order_was_paid(order)
            worker_link = await db.get_worker_link(order['worker_id'])
            await db.delete_offer(order['order_id'], order['worker_id'])
            await message.answer(f"Заказ №{order['order_id']} успешно оплачен!\nВот ссылка на исполнителя: {worker_link}\nСпасибо за сотрудничество!", reply_markup=keyboard.user_start_kbd())
            await bot.send_message(order['worker_id'], f"Ваше предложение в {order['price']}TON на заказ №{order['order_id']} было принято!\nCcылка на заказчика: @{message.from_user.username}\nСпасибо за сотрудничесвто!")
    else:
        if await db.ifUserIsWorker(message):
            await db.update_worker_info(message)
            await st.UserStates.worker_start_state.set()
            await message.answer(f"Добро пожаловать {message.from_user.first_name}!\nВам даны права разработчика.\nДля"
                                 f" начала рекомендуем ознакомиться с правилами и принципами работы бота.\n"
                                 f"Удачной работы!", reply_markup=keyboard.worker_start_kbd())
        else:
            await db.update_user_info(message)
            await st.UserStates.user_start_state.set()
            await message.answer(f"Здаравствуйте {message.from_user.first_name}!\nВас приветствует LabaHelperBot.",
                                 reply_markup=keyboard.user_start_kbd())


@dp.message_handler()
async def start_message(message, state: FSMContext):
    # TODO normalise
    if await db.ifUserIsWorker(message):
        await db.update_worker_info(message)
        await st.UserStates.worker_start_state.set()
        await message.answer(f"Добро пожаловать {message.from_user.first_name}!\nВам даны права разработчика.\nДля"
                             f" начала рекомендуем ознакомиться с правилами и принципами работы бота.\n"
                             f"Удачной работы!", reply_markup=keyboard.worker_start_kbd())
    else:

        await st.UserStates.user_start_state.set()
        await message.answer(f"Здаравствуйте {message.from_user.first_name}!\nВас преветствует LabaHelperBot.",
                             reply_markup=keyboard.user_start_kbd())


@dp.callback_query_handler(text='send_exclamation', state='*')
async def send_exclamation(callback: types.CallbackQuery, state: FSMContext):
    #TODO
    await callback.message.answer("Эта функция нахоится на этапе разработки!")
    await callback.message.delete()


############################################################################
###USER PART################################################################
############################################################################


@dp.message_handler(content_types=['text'], state=st.UserStates.user_start_state)
async def first_user_page_message(message, state: FSMContext):
    """User choose bot abilities"""
    if message.text == 'Заказать лабу':
        if await db.if_user_has_order(message.chat.id):
            await st.UserStates.user_choose_language_state.set()
            await message.answer(f"Выберите язык программирования", reply_markup=keyboard.languages_kbd())
        else:
            await message.answer(f"У вас уже есть активный заказ!")

    elif message.text == 'Помощь':
        await message.answer("Этот раздел откроется в ближайшем будующем(")
    elif message.text == 'Mои заказы':
        await db.get_user_order(message, bot)
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
            await bot.send_document(config.main_account, data['doc'], caption=f"{data['order']}\nОписание: {message.text}",
                                    reply_markup=keyboard.accept_order_ikb())
        else:
            await bot.send_photo(config.main_account, data['photo'], caption=f"{data['order']}\nОписание: {message.text}",
                                 reply_markup=keyboard.accept_order_ikb())
        await st.UserStates.user_start_state.set()
        await message.answer(f"Ваш заказ №{data['order']} сохранён и отправлен на проверку!", reply_markup=keyboard.user_start_kbd())


@dp.callback_query_handler(text='accept_price', state='*')
async def accept_price(callback: types.CallbackQuery, state: FSMContext):
    work = callback.message.text.split('\n')[0].split(' ')[-1]
    price = callback.message.text.split(' ')[-1][:-1]

    worker = await db.is_offer_available(work, price)
    if worker is not None:

        invoice = await config.crypto.create_invoice(asset='USDT', amount=price,
                                                     paid_btn_url=f"https://t.me/LabaHelperBot?start={work}",
                                                     paid_btn_name="callback", expires_in=1800)
        await db.user_choose_price(callback.message.chat.id, worker, work, invoice.invoice_id, price)
        await callback.message.answer(f"Отлично!\n Вот ссылка на оплату: {invoice.pay_url}\nЦена: {price}USDT\nУ вас 30 минут на оплату")
        # await st.UserStates.successful_user_payment_state.set()
    else:
        await callback.message.answer(f"Извините, но срок давности этого предложения уже прошёл!")
    await callback.message.delete()


@dp.callback_query_handler(text='accept_solution', state='*')
async def accept_price(callback: types.CallbackQuery, state: FSMContext):
    try:
        print(callback.message.caption.split('\n')[0][1:])
        order = await db.get_order_by_key(callback.message.caption.split('\n')[0][1:])
        b = True
        while b:
            try:
                await config.crypto.transfer(user_id=order['worker_id'], asset='USDT', amount=order['price'], spend_id=f"{uuid.uuid4()}")
                b = False
            except Exception as ex:
                print(ex)
                b = True
        print(1)
        await db.save_history(order)
        await bot.send_message(order['worker_id'], f"Заказчик отметил, что заказ №{order['order_id']} был выполнен\n"
                                                  f"На ваш счёт было зачислено {order['price']} USDT\n"
                                                  f"Спасибо за сотрудничество!")
        await callback.message.delete()
        await callback.message.answer(f"Заказ был отмечен как выполненый!")

    except Exception as ex:
        print(ex)
        await callback.message.answer("Ошибка!\nПопробуйте позже!")


@dp.callback_query_handler(text='delete_order', state='*')
async def accept_order(callback: types.CallbackQuery, state: FSMContext):
    order = await db.delete_order(callback.message.caption.split('\n')[0][1:])
    await callback.message.answer(f"Ваш заказ №{order['order_id']} был успешно удалён!")
    await callback.message.delete()


@dp.callback_query_handler(text='check_offers', state='*')
async def user_check_offers(callback: types.CallbackQuery, state: FSMContext):
    #TODO
    await callback.message.answer("Эта функция нахоится на этапе разработки!")


@dp.callback_query_handler(text='check_deadline', state='*')
async def user_check_deadline(callback: types.CallbackQuery, state: FSMContext):
    #TODO
    await callback.message.answer("Эта функция нахоится на этапе разработки!")


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
        await message.answer("Этот раздел откроется в ближайшем будующем(")
    elif message.text == 'Mои работы':
        await db.get_worker_order(bot, message)
    else:
        await message.answer("Извините, но я вас не понимаю!", reply_markup=keyboard.user_start_kbd())


@dp.callback_query_handler(text='offer_price', state='*')
async def offer_price(callback: types.CallbackQuery, state: FSMContext):
    await st.UserStates.worker_price_state.set()
    await callback.message.answer(f"Предложите свою цену в $:")
    async with state.proxy() as data:
        data['order'] = callback.message.caption[1:5]
    await callback.message.delete()


@dp.message_handler(content_types=['text'], state=st.UserStates.worker_price_state)
async def send_worker_price(message, state: FSMContext):
    arr = message.text.split('.')
    b = True
    if len(arr) == 1:
        if not message.text.isdigit:
            b = False
    elif len(arr) == 2:
        try:
            num = float(message.text)
        except:
            b = False
    else:
        b = False

    if b:
        num = round(float(message.text), 3)
        if num < 2:
            await message.answer("Сумма слишком маленькая!\nМинимальное предложение - 2$")
        elif num > 200:
            await message.answer("Сумма слишком большая!\nМакцимально возможное предложение - 200$")
        else:
            async with state.proxy() as data:
                user = await db.get_user_id(data['order'])
                await db.save_offer(data['order'], message.chat.id, num)
                await bot.send_message(user, f"На ваш заказ № {data['order']}\nПришло предложение цены: {num}$",
                                       reply_markup=keyboard.user_accept_price_ikb())
                await message.answer(f"Ваше предложение в {num}$ было отправлено", reply_markup=keyboard.worker_start_kbd())
                await state.finish()
    else:
        await message.answer("Неподходящий формат записи!\nПопробуйте ещё раз")


########################################################################
###MY PART#############################################################
########################################################################


@dp.callback_query_handler(text='accept_order', state='*')
async def accept_order(callback: types.CallbackQuery, state: FSMContext):
    await db.accept_order(int(callback.message.caption.split('\n')[0]), bot)
    await callback.message.delete()


@dp.callback_query_handler(text='decline_order', state='*')
async def decline_order(callback: types.CallbackQuery, state: FSMContext):
    await st.UserStates.admin_decline_order_state.set()
    async with state.proxy() as data:
        data['order'] = callback.message.caption.split('\n')[0]
        await callback.message.answer("Укажите причину отказа:")


@dp.message_handler(content_types=['text'], state=st.UserStates.admin_decline_order_state)
async def admin_decline_order(message, state: FSMContext):
    async with state.proxy() as data:
        user = await db.get_user_id(data['order'])
        await db.delete_order(data['order'])
        await bot.send_message(user, f"Ваш заказ №{data['order']} был отклонён по причине:\n{message.text}")
        await state.finish()


@dp.callback_query_handler(text='ban_user', state='*')
async def ban_user(callback: types.CallbackQuery, state: FSMContext):
    # TODO
    await callback.message.answer("Этот раздел находится в разработке")

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT,
    )


