from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update

from enum import Enum

token = '5579843295:AAF11lonl-kELUgF50-Tp3arYgw0BeRzOeE'

how_to_pay = "BQACAgUAAxkBAAIaa2P-9jSXZh8-g2rdK4nt12Dfe2HqAAIyBwACSFH4VxKHGGvQLXBsLgQ"
how_to_oerder = "BQACAgUAAxkBAAIalWP_DrdvMz35lPQmIoonZgXmxHfoAAJcBwACSFH4V2DXuFnPkdFlLgQ"

#https://api.telegram.org/bot5579843295:AAF11lonl-kELUgF50-Tp3arYgw0BeRzOeE/setwebhook?url=https://81.200.157.100/

cf = 1.5

# host = 'localhost'
# user = 'root'
# password = 'gotcha'
# db_name = 'db'

host = '45.8.96.167'
user = 'gen_user'
password = 'dpp5tggbf6'
db_name = 'default_db'


languages = {'C++', 'Java', 'ASSEMBLER'}

main_account = 1208266563
support_account = 5517807465

#
crypto = AioCryptoPay(token='6615:AAqfEMEaHHvCrFRPvVnWuJ96xzvvur8Q1fq', network=Networks.TEST_NET)


##########################################################

WEBHOOK_HOST = 'https://81.200.157.100'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '81.200.157.100'
WEBAPP_PORT = 22

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

