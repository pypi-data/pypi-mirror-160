import decimal
from datetime import datetime

from easytradesdk.Serializer import DeserializableObject


class Ticker(DeserializableObject):

    def __init__(self, price=None, lastUpdateMills=0):
        self.price = price
        self.lastUpdateMills = lastUpdateMills

    def getObjectMapper(self):
        return {"price": decimal.Decimal}

    def getOffsetMills(self):
        _currentMills = int(round(datetime.now().timestamp() * 1000))
        return _currentMills - self.lastUpdateMills
