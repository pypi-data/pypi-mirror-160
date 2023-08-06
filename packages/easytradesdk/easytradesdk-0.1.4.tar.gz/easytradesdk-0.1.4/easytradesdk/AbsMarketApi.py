import abc


class AbsMarketApi(metaclass=abc.ABCMeta):

    def fetchKline(self, tc, symbol, klinePeriod, startTimeMills=None, endTimeMills=None, limit=200):
        pass

    def fetchLatestKline(self, tc, symbol, klinePeriod, endTimeMills=None, limit=200, excludeCurrent=None):
        pass

    def fetchDepth(self, tc, symbol, depthLimit=20):
        pass

    def fetchTicker(self, tc, symbol):
        pass
