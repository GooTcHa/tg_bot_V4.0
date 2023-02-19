import datetime
from random import randint

import pymysql
from config import host, user, password, db_name
import keyboard


async def connect_db():
    pass


async def ifUserIsWorker(message) -> bool:
    """CHECK IF USER HAS WORKER STATUS"""
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Database was connected!")
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT * FROM worker_list WHERE worker_id = {message.chat.id}")
                if not cur.fetchall():
                    return False
                return True
        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def saveUserOrder(message, data) -> None:
    """SAVE USER ORDER"""
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Database was connected!")
        try:
            with connection.cursor() as cur:
                num = randint(1000, 9999)
                cur.execute(f"""SELECT user_id FROM order_list""")
                while cur.fetchall().count(num) > 0:
                    num = randint(1000, 9999)
                data['order'] = num
                date = datetime.date.today()
                day = datetime.timedelta(days=2)
                date = date + day
                if data['doc']:
                    cur.execute(f"INSERT INTO order_list(order_id, user_id, language, doc,"
                                f" text, deadline, state) VALUES('{num}', '{message.chat.id}','{data['language']}',"
                                f" '{data['doc']}', '{data['descr']}', '{date}', 0)")
                else:
                    cur.execute(f"INSERT INTO order_list(order_id, user_id, language, photo,"
                                f" text, deadline, state) VALUES('{num}', '{message.chat.id}','{data['language']}',"
                                f" '{data['photo']}', '{data['descr']}', '{date}', 0)")
                connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print("error1")
        print(ex)


async def printFreeOrders(message, bot) -> None:
    """SAVE USER ORDER"""
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT * FROM order_list WHERE state='1'")
                arr = cur.fetchall()
                date = datetime.date.today()
                day = datetime.timedelta(days=2)
                if arr != ():
                    for i in arr:
                        if i['deadline'] < date - day:
                            order = await delete_order(i['order_id'])
                            await bot.send_message(order['user_id'], f"Ваш заказ №{order['order_id']} был удалён в связи с окончанием срока давности!")
                        elif i['doc']:
                            await bot.send_document(message.chat.id, i['doc'],
                                                    caption=f"#{i['order_id']}\nУсловие: {i['text']}",
                                                    reply_markup=keyboard.worker_watch_ikb())
                        else:
                            await bot.send_photo(message.chat.id, i['photo'],
                                                 caption=f"#{i['order_id']}\nУсловие: {i['text']}",
                                                 reply_markup=keyboard.worker_watch_ikb())
                else:
                    await message.answer("Свободных заказов нет☹", reply_markup=keyboard.worker_start_kbd())
        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def delete_order(order_id):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT * FROM order_list WHERE order_id='{order_id}';")
                user_id = cur.fetchone()
                cur.execute(f"DELETE FROM order_list WHERE order_id='{order_id}';")
                connection.commit()
                return user_id

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def accept_order(order_id, bot):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                date = datetime.date.today()
                day = datetime.timedelta(days=2)
                date = date + day
                cur.execute(f"UPDATE order_list SET deadline='{date}', state='1'  WHERE order_id='{order_id}';")
                connection.commit()
                cur.execute(f"SELECT user_id FROM order_list WHERE order_id='{order_id}';")
                await bot.send_message(cur.fetchone()['user_id'], f"Ваш заказ №{order_id} был одобрен и опубликован!")

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def get_user_id(order) -> int:
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT user_id FROM order_list WHERE order_id='{order}';")
                return cur.fetchone()['user_id']

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def save_offer(order, worker_id, price):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(
                    f"INSERT INTO price_offer(order_id, worker_id, price) VALUES('{order}', '{worker_id}', '{price}');")
                connection.commit()
                print(1)
        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def is_offer_available(work, price) -> bool:
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT worker_id FROM price_offer WHERE order_id='{work}' AND price='{price}';")
                temp = cur.fetchone()['worker_id']
                # print(temp)
                return temp

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def user_choose_price(user_id, worker, work, invoice_id, price):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("DB connected!")
        try:
            with connection.cursor() as cur:
                cur.execute(f"UPDATE worker_list SET worker_state='1' WHERE worker_id='{worker}';")
                connection.commit()

                cur.execute(
                    f"UPDATE order_list SET worker_id='{worker}', price='{price}', invoice_id='{invoice_id}', state='2'"
                    f" WHERE order_id='{work}';")
                connection.commit()

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def get_order_invoice(user_id, work_id):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT invoice_id FROM order_list WHERE order_id='{work_id}' AND user_id='{user_id}';")
                return cur.fetchone()['invoice_id']

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def order_was_paid(order):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            date = datetime.date.today()
            day = datetime.timedelta(days=7)
            date = date + day
            with connection.cursor() as cur:
                cur.execute(f"UPDATE order_list SET deadline='{date}', state='3' WHERE order_id='{order}';")
                connection.commit()

                cur.execute(f"SELECT * FROM order_list WHERE order_id='{order}';")
                return cur.fetchone()

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def update_worker_info(message):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(
                    f"UPDATE worker_list SET worker_link='@{message.from_user.username}' WHERE worker_id='{message.chat.id}';")
                connection.commit()

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def update_user_info(message):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT * FROM user_list WHERE user_id='{message.chat.id}';")
                result = cur.fetchone()
                if result is None:
                    cur.execute(f"INSERT INTO user_list(user_id, user_link) VALUES ('{message.chat.id}', '@{message.from_user.username}');")
                    connection.commit()
                else:
                    cur.execute(
                        f"UPDATE user_list SET user_link='@{message.from_user.username}' WHERE user_id='{message.chat.id}';")
                    connection.commit()

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def get_worker_link(worker):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT worker_link FROM worker_list WHERE worker_id='{worker}';")
                link = cur.fetchone()['worker_link']
                return link

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def get_user_link(user_id):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT user_link FROM user_list WHERE user_id='{user_id}';")
                link = cur.fetchone()['user_link']
                return link

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def get_user_order(message, bot):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT * FROM order_list WHERE user_id='{message.chat.id}';")
                orders = cur.fetchall()

                if orders == ():
                    await message.answer(f"У вас, пока что, нет активных заказов☹")
                else:
                    for order in orders:
                        if order['state'] == 0:
                            if order['doc']:
                                await bot.send_document(message.chat.id, order['doc'],
                                                        caption=f"#{order['order_id']}\nУсловие: {order['text']}\nСтатус: Заказ находится на проверке",
                                                        reply_markup=keyboard.user_work_02_ikb())
                            else:
                                await bot.send_photo(message.chat.id, order['photo'],
                                                     caption=f"#{order['order_id']}\nУсловие: {order['text']}\nСтатус: Заказ находится на проверке",
                                                     reply_markup=keyboard.user_work_02_ikb())
                        elif order['state'] == 1:
                            if order['doc']:
                                await bot.send_document(message.chat.id, order['doc'],
                                                        caption=f"#{order['order_id']}\nУсловие: {order['text']}\nСтатус: Заказ одобрен и доступен для исполнителей",
                                                        reply_markup=keyboard.user_work_1_ikb())
                            else:
                                await bot.send_photo(message.chat.id, order['photo'],
                                                     caption=f"#{order['order_id']}\nУсловие: {order['text']}\nСтатус: Заказ одобрен и доступен для исполнителей",
                                                     reply_markup=keyboard.user_work_1_ikb())
                        elif order['state'] == 2:
                            if order['doc']:
                                await bot.send_document(message.chat.id, order['doc'],
                                                        caption=f"#{order['order_id']}\nУсловие: {order['text']}\nСтатус: Заказ находится на стадии ожидания оплаты",
                                                        reply_markup=keyboard.user_work_02_ikb())
                            else:
                                await bot.send_photo(message.chat.id, order['photo'],
                                                     caption=f"#{order['order_id']}\nУсловие: {order['text']}\nСтатус: Заказ находится на стадии ожидания оплаты",
                                                     reply_markup=keyboard.user_work_02_ikb())
                        elif order['state'] == 3:
                            if order['doc']:
                                await bot.send_document(message.chat.id, order['doc'],
                                                        caption=f"#{order['order_id']}\nУсловие: {order['text']}\nИсполнитель: {await get_worker_link(order['worker_id'])}\nДедлайн: {order['deadline']}",
                                                        reply_markup=keyboard.user_work_3_ikb())
                            else:
                                await bot.send_photo(message.chat.id, order['photo'],
                                                     caption=f"#{order['order_id']}\nУсловие: {order['text']}\nИсполнитель: {await get_worker_link(order['worker_id'])}\nДедлайн: {order['deadline']}",
                                                     reply_markup=keyboard.user_work_3_ikb())
        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def if_user_has_order(user_id):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT * FROM order_list WHERE user_id='{user_id}';")
                order = cur.fetchone()
                if order is not None:
                    return False
                return True
        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def get_worker_order(bot, message):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT * FROM order_list WHERE worker_id='{message.chat.id}';")
                orders = cur.fetchall()
                if orders == ():
                    await message.answer("У вас пока нет активных заказов")
                else:
                    for order in orders:
                        if order['doc']:
                            await bot.send_document(message.chat.id, order['doc'],
                                                    caption=f"#{order['order_id']}\nУсловие: {order['text']}\nЗаказчик: {await get_user_link(order['user_id'])}\nДедлайн: {order['deadline']}",
                                                    reply_markup=keyboard.worker_work_ikb())
                        else:
                            await bot.send_photo(message.chat.id, order['photo'],
                                                 caption=f"#{order['order_id']}\nУсловие: {order['text']}\nЗаказчик: {await get_user_link(order['user_id'])}\nДедлайн: {order['deadline']}",
                                                 reply_markup=keyboard.worker_work_ikb())
        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def get_order_by_key(order_id):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT * FROM order_list WHERE order_id='{order_id}';")
                order = cur.fetchone()
                return order
        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def save_history(order):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cur:
                print(order, sep='\n')
                cur.execute(f"INSERT INTO order_history(order_id, user_id, worker_id, language, photo, doc, text, price)"
                            f" VALUES('{order['order_id']}', '{order['user_id']}', '{order['worker_id']}', "
                            f"'{order['language']}', '{order['photo']}', '{order['doc']}', '{order['text']}', "
                            f"'{order['price']}');")
                connection.commit()
                cur.execute(f"DELETE FROM order_list WHERE order_id='{order['order_id']}';")
                connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cur:
            cur.execute(f"DELETE FROM order_history;")
            connection.commit()

    except Exception as ex:
        print(ex)


