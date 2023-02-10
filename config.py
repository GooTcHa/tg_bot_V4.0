from aiocryptopay import AioCryptoPay, Networks
from enum import Enum

token = '5579843295:AAF11lonl-kELUgF50-Tp3arYgw0BeRzOeE'


host = '127.0.0.1'
user = 'root'
password = 'gotcha'
db_name = 'db'


languages = {'C++' , 'Java', 'ASSEMBLER'}

main_account = 1208266563

#
crypto = AioCryptoPay(token='6615:AAqfEMEaHHvCrFRPvVnWuJ96xzvvur8Q1fq', network=Networks.TEST_NET)


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

