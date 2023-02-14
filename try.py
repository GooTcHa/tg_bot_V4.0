from aiohttp import web

from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update


web_app = web.Application()
crypto = AioCryptoPay(token='6615:AAqfEMEaHHvCrFRPvVnWuJ96xzvvur8Q1fq', network=Networks.TEST_NET)


@crypto.pay_handler()
async def invoice_paid(update) -> None:
    print(2)
    for i in update:
        print(i, "1", sep="\n")

    return web.Response(text="Hello, world")



async def create_invoice(app) -> None:
    invoice = await crypto.create_invoice(asset='TON', amount=0.005)
    print(invoice.pay_url)


async def close_session(app) -> None:
    await crypto.close()


# def start():
#     web_app.add_routes([web.post('/crypto-secret-path', crypto.get_updates)])
#     web_app.on_startup.append(create_invoice)
#     web_app.on_shutdown.append(close_session)
#     runner = web.AppRunner(web_app)
#     await runner.setup()
#     site = web.TCPSite(runner, 'localhost', 5000)
#     await site.start()
#     # wait for finish signal
#     await runner.cleanup()


if __name__ == '__main__':
    web_app.add_routes([web.post('/', crypto.get_updates)])
    web_app.on_startup.append(create_invoice)
    web_app.on_shutdown.append(close_session)
    web.run_app(app=web_app, host='localhost', port=4000)