import decimal
from datetime import datetime

from easytradesdk.Serializer import DeserializableObject


class DepthValue(DeserializableObject):

    def __init__(self):
        self.price = None
        self.quantity = None

    def getObjectMapper(self):
        return {"price": decimal.Decimal, "quantity": decimal.Decimal}


class Depth(DeserializableObject):

    def __init__(self, bids=None, asks=None, lastUpdateMills=0):
        if bids is None:
            bids = []
        if asks is None:
            asks = []
        self.bids = bids
        self.asks = asks
        self.lastUpdateMills = lastUpdateMills
        self.bids = []
        self.asks = []

    def getObjectMapper(self):
        return {"bids": DepthValue, "asks": DepthValue}

    def getOffsetMills(self):
        _currentMills = int(round(datetime.now().timestamp() * 1000))
        return _currentMills - self.lastUpdateMills
