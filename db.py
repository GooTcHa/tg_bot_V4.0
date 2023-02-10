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

                for i in arr:
                    if i['deadline'] < date - day:
                        await delete_order(i['order_id'], bot)
                    elif i['doc']:
                        await bot.send_document(message.chat.id, i['doc'], caption=f"#{i['order_id']}\nУсловие: {i['text']}",
                                                reply_markup=keyboard.worker_watch_ikb())
                    else:
                        await bot.send_photo(message.chat.id, i['photo'], caption=f"#{i['order_id']}\nУсловие: {i['text']}",
                                             reply_markup=keyboard.worker_watch_ikb())
        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def delete_order(order_id, bot):
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
                cur.execute(f"SELECT user_id FROM order_list WHERE order_id='{order_id}';")
                user_id = cur.fetchone()
                cur.execute(f"DELETE FROM order_list WHERE order_id='{order_id}';")
                connection.commit()
                await bot.send_message(user_id, f"Ваш заказ №{order_id} был удалён в связи с истечением срока давности.")

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def accept_order(user_id, bot):
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
                cur.execute(f"UPDATE order_list SET deadline='{date}', state='1'  WHERE user_id='{user_id}';")
                connection.commit()
                await bot.send_message(user_id, "Ваш заказ был одобрен и опубликован!")

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
                cur.execute(f"INSERT INTO price_offer(order_id, worker_id, price) VALUES('{order}', '{worker_id}', '{price}');")
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
                cur.execute(f"SELECT * FROM price_offer WHERE order_id='{work}' AND price='{price}';")

                if cur.fetchall() == ():
                    return False
                return True

        finally:
            connection.close()

    except Exception as ex:
        print(ex)


async def accept_price(work, price, bot):
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
                cur.execute(f"INSERT ;")
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
            cur.execute("DELETE FROM price_offer;")
            connection.commit()

    except Exception as ex:
        print(ex)