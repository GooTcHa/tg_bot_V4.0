import pymysql
from config import host, user, password, db_name

async def connect_db():
    pass
    # try:
    #     connection = pymysql.connect(
    #         host=host,
    #         port=3306,
    #         user=user,
    #         password=password,
    #         database=db_name,
    #         cursorclass=pymysql.cursors.DictCursor
    #     )
    #     print("Database was connected!")
    #     with connection.cursor() as cur:
    #         cur.execute(f"INSERT INTO worker_list (worker_id, worker_name, worker_balance) VALUES (1208266563, 'name', 13.40)")
    #         connection.commit()
    #
    #         if not cur.fetchall():
    #             return False
    #         return True
    #
    # except Exception as ex:
    #     print(ex)

connection: pymysql.connect


"""CHECK IF USER HAS WORKER STATUS"""
async def ifUserIsWorker(message) -> bool:
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
        with connection.cursor() as cur:
            cur.execute(f"SELECT * FROM worker_list WHERE worker_id = {message.chat.id}")
            if not cur.fetchall():
                return False
            return True

    except Exception as ex:
        print(ex)


# import sqlite3
# from pathlib import Path
# import os.path
# from random import randint
#
#
# async def database_connect() -> None:
#     global db, cursor
#
#     sqlite_file = 'D:\\Projects\\Python\\try-bot\\data\\db.db'
#     if os.path.exists(sqlite_file):
#         print('File exists')
#     else:
#         print('File NOT exists')
#     db = sqlite3.connect(sqlite_file)
#     cursor = db.cursor()
#
#
# async def add_user(message):
#     cursor.execute(f"SELECT * FROM users WHERE userid = {message.chat.id} ;")
#     if not cursor.fetchall():
#         cursor.execute(""f"INSERT INTO users(userid) VALUES({message.chat.id});""")
#         db.commit()
#
#
# async def check_order_existence(message):
#     cursor.execute(f"SELECT * FROM user_order WHERE userid = {message.chat.id} ;")
#     if not cursor.fetchall():
#         return True
#
#     return False
#
#
# async def add_order(message, data):
#     cursor.execute(f"SELECT order_id FROM user_order;")
#     o_id = randint(1000, 9999)
#     while cursor.fetchall().count(o_id) > 0:
#         o_id = randint(1000, 9999)
#     cursor.execute(""f"INSERT INTO user_order VALUES(?, ?, ?, ?, ?, ?, ?);""", (message.chat.id, f"{data['language']}",
#                                                                              data['condition'], data['special'], '',
#                                                                              "wait", o_id))
#     db.commit()