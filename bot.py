import asyncio
import os

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import uuid

import logging
import keyboard
import states as st
import config
import db

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

loop = asyncio.get_event_loop()
storage = MemoryStorage()
bot = Bot(token=config.token)
dp = Dispatcher(bot,loop=loop, storage=storage)
# dp.middleware.setup(LoggingMiddleware())


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
    print(message)
    # arr = (await config.crypto.get_exchange_rates())
    # for i in arr:
    #     print(i)
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
            await message.answer(f"Заказ №{order['order_id']} успешно оплачен!\nВот ссылка на исполнителя: {worker_link}\nСпасибо за сотрудничество!")
            await bot.send_message(order['worker_id'], f"Ваше предложение в {order['price']}$ на заказ №{order['order_id']} было принято!\nCcылка на заказчика: @{message.from_user.username}\nСпасибо за сотрудничесвто!")
            await st.UserStates.user_start_state.set()
    else:
        if await db.ifUserIsWorker(message):
            await db.update_worker_info(message)
            await st.UserStates.worker_start_state.set()
            await message.answer(f"Добро пожаловать {message.from_user.first_name}!\nВам даны права разработчика.\nДля"
                                 f" начала рекомендуем ознакомиться с правилами и принципами работы бота.\n"
                                 f"Удачной работы!", reply_markup=keyboard.worker_start_ikb())
        else:
            await db.update_user_info(message)
            await st.UserStates.user_start_state.set()
            await message.answer(f"Здаравствуйте {message.from_user.first_name}!\nВас приветствует LabaHelperBot.",
                                 reply_markup=keyboard.user_start_ikb())


@dp.message_handler(commands=['menu'], state='*')
async def menu(message, state: FSMContext):
    if await db.ifUserIsWorker(message):
        await db.update_worker_info(message)
        await st.UserStates.worker_start_state.set()
        await message.answer(f"Вас приветствует LabaHelperBot - бот для помощи в написании лобораторных работ", reply_markup=keyboard.worker_start_ikb())
    else:

        await st.UserStates.user_start_state.set()
        await message.answer(f"Вас приветствует LabaHelperBot - бот для помощи в написании лобораторных работ",
                             reply_markup=keyboard.user_start_ikb())

@dp.message_handler()
async def start_message(message, state: FSMContext):
    if await db.ifUserIsWorker(message):
        await db.update_worker_info(message)
        await st.UserStates.worker_start_state.set()
        await message.answer(f"Вас приветствует LabaHelperBot", reply_markup=keyboard.worker_start_ikb())
    else:

        await st.UserStates.user_start_state.set()
        await message.answer(f"Вас приветствует LabaHelperBot",
                             reply_markup=keyboard.user_start_ikb())


@dp.callback_query_handler(text='send_exclamation', state='*')
async def exclamation(callback: types.CallbackQuery, state: FSMContext):
    order = await db.get_order_by_key(callback.message.caption.split('\n')[0][1:])
    await st.UserStates.pre_exclamation_state.set()
    async with state.proxy() as data:
        data['order'] = order
        await callback.message.answer("Опишите причину спора:")
        await callback.message.delete()


@dp.message_handler(content_types=['text'], state=st.UserStates.pre_exclamation_state)
async def pre_exclamation(message, state: FSMContext):
    async with state.proxy() as data:
        data['reason'] = message.text
        await st.UserStates.exclamation_state.set()
        await message.answer(f"Причина спора: {message.text}\n\nВы уверены, что хотите отправить?", reply_markup=keyboard.bool_kbd())


@dp.message_handler(content_types=['text'], state=st.UserStates.exclamation_state)
async def send_exclamation(message, state: FSMContext):
    if message.text == "Да":
        async with state.proxy() as data:
            if data['order']['user_id'] == message.chat.id:
                if data['order']['photo']:
                    await bot.send_photo(config.main_account, photo=data['order']['photo'],
                                         caption=f"СПОР(З)\nЗаказ {data['order']['order_id']}\n"
                                                 f"Язык: {data['order']['language']}\nУсловие: {data['order']['text']}\n"
                                                 f"Причина: {data['reason']}\nЗаказчик: {await db.get_user_link(data['order']['user_id'])}\n"
                                                 f"Исполнитель: {await db.get_worker_link(data['order']['worker_id'])}",
                                         reply_markup=keyboard.exclamation_ikb())
                else:
                    await bot.send_document(config.main_account, document=data['order']['doc'],
                                            caption=f"СПОР(З)\nЗаказ {data['order']['order_id']}\n"
                                                    f"Язык: {data['order']['language']}\nУсловие: {data['order']['text']}\n"
                                                    f"Причина: {data['reason']}\nЗаказчик: {await db.get_user_link(data['order']['user_id'])}\n"
                                                    f"Исполнитель: {await db.get_worker_link(data['order']['worker_id'])}",
                                            reply_markup=keyboard.exclamation_ikb())
                await bot.send_message(data['order']['worker_id'], f"Заказчик: {await db.get_user_link(data['order']['user_id'])} открыл спор на заказ №{data['order']['order_id']}\n"
                                                                   f"Причина: {data['reason']}")
            else:
                if data['order']['photo']:
                    await bot.send_photo(config.main_account, photo=data['order']['photo'], caption=f"СПОР(Р)\nЗаказ {data['order']['order_id']}\n"
                                                            f"Язык: {data['order']['language']}\nУсловие: {data['order']['text']}\n"
                                                            f"Причина: {data['reason']}\nЗаказчик: {await db.get_user_link(data['order']['user_id'])}\n"
                                                            f"Исполнитель: {await db.get_worker_link(data['order']['worker_id'])}",
                                                            reply_markup=keyboard.exclamation_ikb())
                else:
                    await bot.send_document(config.main_account, document=data['order']['doc'],
                                         caption=f"СПОР(Р)\nЗаказ {data['order']['order_id']}\n"
                                                 f"Язык: {data['order']['language']}\nУсловие: {data['order']['text']}\n"
                                                 f"Причина: {data['reason']}\nЗаказчик: {await db.get_user_link(data['order']['user_id'])}\n"
                                                 f"Исполнитель: {await db.get_worker_link(data['order']['worker_id'])}",
                                         reply_markup=keyboard.exclamation_ikb())
                await bot.send_message(data['order']['user_id'], f"Работник: {await db.get_worker_link(data['order']['worker_id'])} открыл спор на заказ №{data['order']['order_id']}\n"
                                                                 f"Причина: {data['reason']}")
        await message.answer("Жалоба отправлена!", reply_markup=keyboard.clear_kbd())
        await db.set_order_state(data['order']['order_id'], 4)
        await state.finish()
    elif message.text == "Нет":
        await message.answer("Жалоба удалена!", reply_markup=keyboard.clear_kbd())
        await state.finish()
    else:
        await message.answer("Я вас не понимаю, воспользуйтесь кнопками!")

############################################################################
###USER PART################################################################
############################################################################


# @dp.message_handler(content_types=['text'], state=st.UserStates.user_start_state)
# async def first_user_page_message(message, state: FSMContext):
#     """User choose bot abilities"""
#     if message.text == 'Заказать лабу':
#         if await db.if_user_has_order(message.chat.id):
#             await st.UserStates.user_choose_language_state.set()
#             await message.answer(f"Выберите язык программирования", reply_markup=keyboard.languages_kbd())
#         else:
#             await message.answer(f"У вас уже есть активный заказ!")
#
#     elif message.text == 'Помощь':
#         await message.answer("Этот раздел откроется в ближайшем будующем(")
#     elif message.text == 'Mои заказы':
#         await db.get_user_order(message, bot)
#     else:
#         await message.answer("Извините, но я вас не понимаю!")


@dp.callback_query_handler(text='create_order', state='*')
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    if await db.if_user_has_order(callback.message.chat.id):
        await st.UserStates.user_choose_language_state.set()
        await callback.message.answer(f"Выберите язык программирования", reply_markup=keyboard.languages_kbd())
        await callback.message.delete()
    else:
        await callback.message.answer(f"У вас есть один активный заказ!")


@dp.callback_query_handler(text='user_orders', state='*')
async def user_orders(callback: types.CallbackQuery, state: FSMContext):
    await db.get_user_order(callback.message, bot)


@dp.message_handler(content_types=['text'], state=st.UserStates.user_choose_language_state)
async def save_user_language(message, state: FSMContext):
    if message.text in config.languages != -1:
        async with state.proxy() as data:
            data['language'] = message.text
            await st.UserStates.user_send_photo_state.set()
            await message.answer(f"Вы выбрали {data['language']}\nОтправте фотографию вашего условия.",
                                 reply_markup=keyboard.clear_kbd())
    else:
        await message.answer("Я тебя не понимаю!\nПопробуй ещё раз!", reply_markup=keyboard.languages_kbd())


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
            await bot.send_document(config.main_account, data['doc'], caption=f"{data['order']}\nЯзык: {data['language']}\n"
                                                                              f"Описание: {message.text}",
                                    reply_markup=keyboard.accept_order_ikb())
        else:
            await bot.send_photo(config.main_account, data['photo'], caption=f"{data['order']}\nЯзык: {data['language']}\n"
                                                                             f"Описание: {message.text}",
                                 reply_markup=keyboard.accept_order_ikb())
        await st.UserStates.user_start_state.set()
        await message.answer(f"Ваш заказ №{data['order']} сохранён и отправлен на проверку!", reply_markup=keyboard.clear_kbd())


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
        # print(callback.message.caption.split('\n')[0].split(' ')[1][1:])
        order = await db.get_order_by_key(callback.message.caption.split('\n')[0].split(' ')[1][1:])
        b = True
        while b:
            try:
                await config.crypto.transfer(user_id=order['worker_id'], asset='USDT', amount=order['price'],
                                             spend_id=f"{uuid.uuid4()}")
                await config.crypto.transfer(user_id=config.main_account, asset='USDT',
                                             amount=order['my_price'] - order['price'], spend_id=f"{uuid.uuid4()}",
                                             comment=f"Процент за работу {order['order_id']}")
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
    order_id = callback.message.caption.split('\n')[0][1:]
    await db.get_price_offers(order_id, callback.message)


#########################################################################
###WORKER PART##########################################################
#########################################################################

# @dp.message_handler(content_types=['text'], state=st.UserStates.worker_start_state)
# async def worker_first_message(message, state: FSMContext):
#     """User choose bot abilities"""
#     if message.text == 'Получить список заказов':
#         await message.answer(f"Доступные заказы: ")
#         await db.printFreeOrders(message, bot)
#
#     elif message.text == 'Помощь':
#         await message.answer("Этот раздел откроется в ближайшем будующем(")
#     elif message.text == 'Mои работы':
#         await db.get_worker_order(bot, message)
#     else:
#         await message.answer("Извините, но я вас не понимаю!", reply_markup=keyboard.user_start_kbd())


@dp.callback_query_handler(text='free_orders', state='*')
async def free_orders(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Доступные заказы: ")
    await db.printFreeOrders(callback.message, bot)
    # await callback.message.delete()


@dp.callback_query_handler(text='worker_orders', state='*')
async def free_orders(callback: types.CallbackQuery, state: FSMContext):
    await db.get_worker_order(bot, callback.message)


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
        if not message.text.isdigit():
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
                await bot.send_message(user, f"На ваш заказ № {data['order']}\nПришло предложение цены: {num + config.cf}$",
                                       reply_markup=keyboard.user_accept_price_ikb())
                await message.answer(f"Ваше предложение в {num}$ было отправлено")
                await st.UserStates.worker_start_state.set()
    else:
        await message.answer("Неподходящий формат записи!\nПопробуйте ещё раз")


@dp.callback_query_handler(text='order_executed', state='*')
async def execute_order(callback: types.CallbackQuery, state: FSMContext):
    order_id = callback.message.caption.split('\n')[0][1:]
    order = await db.get_order_by_key(order_id)
    if order['photo']:
        await bot.send_photo(chat_id=order['user_id'], photo=order['photo'], caption=f"Заказ №{order['order_id']}\nУсловие: {order['text']}\n\n"
                             f"{await db.get_worker_link(order['worker_id'])} отметил ваш заказ как выполненный",
                             reply_markup=keyboard.user_accept_solution_ikb())
    else:
        await bot.send_document(chat_id=order['user_id'], document=order['doc'],
                                caption=f"Заказ №{order['order_id']}\nУсловие: {order['text']}\n\n"
                                f"{await db.get_worker_link(order['worker_id'])} отметил ваш заказ как выполненный",
                                reply_markup=keyboard.user_accept_solution_ikb())

    await callback.message.answer(f"Пользователю было отправлено сообщение о выполнении заказа!"
                                  f"\nОжидайте подтверждения...")
    await callback.message.delete()
    await st.UserStates.worker_start_state.set()

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


@dp.callback_query_handler(text='user_r', state='*')
async def user_r(callback: types.CallbackQuery, state: FSMContext):
    order = await db.get_order_by_key(callback.message.caption.split('\n')[1].split(' ')[1])
    b = True
    while b:
        try:
            await config.crypto.transfer(user_id=order['user_id'], asset='USDT', amount=order['my_price'],
                                         spend_id=f"{uuid.uuid4()}")
            b = False
        except Exception as ex:
            print(ex)
            b = True

    await db.save_history(order['order_id'])
    await bot.send_message(order['user_id'], f"Спор по заказу №{order['order_id']} был разрешён в вашу пользу\n"
                                             f"На ваш счёт ыло зачислено {order['my_price']} USDT")
    await bot.send_message(order['worker_id'], f"Cпор по заказу №{order['order_id']} был разрешён в пользу заказчика")


@dp.callback_query_handler(text='worker_r', state='*')
async def worker_r(callback: types.CallbackQuery, state: FSMContext):
    order = await db.get_order_by_key(callback.message.caption.split('\n')[1].split(' ')[1])
    b = True
    while b:
        try:
            await config.crypto.transfer(user_id=order['worker_id'], asset='USDT', amount=order['price'],
                                         spend_id=f"{uuid.uuid4()}")
            b = False
        except Exception as ex:
            print(ex)
            b = True

    await db.save_history(order)
    await bot.send_message(order['worker_id'], f"Спор по заказу №{order['order_id']} был разрешён в вашу пользу\n"
                                             f"На ваш счёт ыло зачислено {order['price']} USDT")
    await bot.send_message(order['user_id'],
                           f"Cпор по заказу №{order['order_id']} был разрешён в пользу исполнителя")


@dp.callback_query_handler(text='decline_excl', state='*')
async def decline_excl(callback: types.CallbackQuery, state: FSMContext):
    order = await db.get_order_by_key(callback.message.caption.split('\n')[1].split(' ')[1])
    await db.set_order_state(order['order_id'], 3)
    await bot.send_message(order['user_id'], f"Спор на заказ №{order['order_id']} был отменён")
    await bot.send_message(order['worker_id'], f"Спор на заказ №{order['order_id']} был отменён")


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           loop=loop)

    # start_webhook(
    #     dispatcher=dp,
    #     webhook_path=config.WEBHOOK_PATH,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     host=config.WEBAPP_HOST,
    #     port=int(os.environ.get("PORT", 443))
    # )


