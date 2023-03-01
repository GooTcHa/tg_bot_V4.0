from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiohttp import web

from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update

import config

storage = MemoryStorage()
bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=storage)
# dp.middleware.setup(LoggingMiddleware())

web_app = web.Application()
crypto = AioCryptoPay(token='6615:AAqfEMEaHHvCrFRPvVnWuJ96xzvvur8Q1fq', network=Networks.TEST_NET)


@crypto.pay_handler()
async def invoice_paid(update: Update) -> None:
    print(update)


async def create_invoice(app) -> None:
    invoice = await crypto.create_invoice(asset='TON', amount=0.005)
    print(invoice.pay_url)


async def close_session(app) -> None:
    await crypto.close()


web_app.add_routes([web.post('/', dp.setup_middleware(LoggingMiddleware()))])
web_app.on_startup.append(create_invoice)
web_app.on_shutdown.append(close_session)
web.run_app(app=web_app, host='0.0.0.0', port=443)