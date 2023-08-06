import abc


class AbsContext(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def getPosition(self, tc, symbol):
        pass

    @abc.abstractmethod
    def getPositions(self):
        pass

    @abc.abstractmethod
    def getStrategyParams(self):
        pass

    @abc.abstractmethod
    def getExecutePeriod(self):
        pass

    @abc.abstractmethod
    def getExecutingTimeMills(self):
        pass

    @abc.abstractmethod
    def getMarketApi(self):
        pass

    @abc.abstractmethod
    def getTradeApi(self):
        pass

    @abc.abstractmethod
    def calculateMaxAvailableBuyQuantity(self, tc, symbol, amount=None, offsetPrice=None, scale=2):
        pass
