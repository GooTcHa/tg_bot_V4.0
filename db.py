from datetime import datetime
from random import random

import pymysql
from config import host, user, password, db_name


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
            async with connection.cursor() as cur:
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
            async with connection.cursor() as cur:
                num = random.randint(1000, 9999)
                cur.execute(f"""SELECT user_id FROM order_list""")
                while num in cur.fetchall != -1:
                    num = random.randint(1000, 9999)
                date = datetime.date.today()
                day = datetime.timedelta(days=2)
                date = date + day
                if data['doc']:
                    cur.execute(f"INSERT INTO order_list(order_id, user_id, language, doc,"
                                f" text, deadline, state) VALUES('{num}', '{message.chat.id}',{data['language']},"
                                f" {data['doc']}, {data['descr']}, {date}, 0)")
                else:
                    cur.execute(f"INSERT INTO order_list(order_id, user_id, language, photo,"
                                f" text, deadline, state) VALUES('{num}', '{message.chat.id}',{data['language']},"
                                f" {data['photo']}, {data['descr']}, {date}, 0)")
                connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print("error1")
        print(ex)


async def printFreeOrders() -> None:
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
        pass
        #TODO print free orders
        # with connection.cursor() as cur:
        async with connection.cursor() as cur:
            cur.execute(f"INSERT INTO order_list () VALUES ({3})")


    except Exception as ex:
        print(ex)


async def accept_order(user_id):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        async with connection.cursor() as cur:
            date = datetime.date.today()
            day = datetime.timedelta(days=2)
            date = date + day
            cur.execute(f"UPDDATE order_list SET state = {1}, deadline = {date} WHERE user_id = {user_id}")
            connection.commit()

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

            # str = "ldfg"
            # # cur.execute(f"INSERT INTO order_list(order_id, user_id, worker_id, language) VALUES({1235}, {1235}, {2131}, {str});")
            # # connection.commit()
            # # cur.execute("SELECT * FROM order_list")
            cur.execute(f"INSERT INTO try(tt, pp, yy) VALUES(23123, 23242, '{'skdf'}');")
            connection.commit()
            # cur.execute("SELECT * FROM try")
            # print(cur.fetchall(), sep='\n')

    except Exception as ex:
        print(ex)