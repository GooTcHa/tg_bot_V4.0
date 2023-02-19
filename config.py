from aiohttp import web

from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update

from enum import Enum

token = '5579843295:AAF11lonl-kELUgF50-Tp3arYgw0BeRzOeE'

#https://api.telegram.org/bot5579843295:AAF11lonl-kELUgF50-Tp3arYgw0BeRzOeE/setwebhook?url=https://d6dd-46-216-120-51.eu.ngrok.io


host = '127.0.0.1'
user = 'root'
password = 'gotcha'
db_name = 'db'


languages = {'C++', 'Java', 'ASSEMBLER'}

main_account = 1208266563

#
crypto = AioCryptoPay(token='6615:AAqfEMEaHHvCrFRPvVnWuJ96xzvvur8Q1fq', network=Networks.TEST_NET)


##########################################################

WEBHOOK_HOST = 'https://d6dd-46-216-120-51.eu.ngrok.io'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 5000

##########################################################

class HTTPMethods(str, Enum):
    """Available HTTP methods."""

    POST = "POST"
    GET = "GET"


class Networks(str, Enum):
    """Cryptobot networks"""

    MAIN_NET = "https://pay.crypt.bot"
    TEST_NET = "https://testnet-pay.crypt.bot"


class Assets(str, Enum):
    """Cryptobot assets"""

    BTC = "BTC"
    TON = "TON"
    ETH = "ETH"
    USDT = "USDT"
    USDC = "USDC"
    BUSD = "BUSD"


class PaidButtons(str, Enum):
    """Cryptobot paid button names"""

    VIEW_ITEM = "viewItem"
    OPEN_CHANNEL = "openChannel"
    OPEN_BOT = "openBot"
    CALLBACK = "callback"


class InvoiceStatus(str, Enum):
    """Invoice status"""

    ACTIVE = "active"
    PAID = "paid"
    EXPIRED = "expired"

