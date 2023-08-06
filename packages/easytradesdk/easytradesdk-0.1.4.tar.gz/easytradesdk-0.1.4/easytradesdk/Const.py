class TCConst:

    def __init__(self):
        self.__BINANCE = "BINANCE"

    @property
    def BINANCE(self):
        return self.__BINANCE


class SymbolConst:

    def __init__(self):
        self.__BTC_USDT = "BTC_USDT"
        self.__ETH_BTC = "ETH_BTC"
        self.__ETH_USDT = "ETH_USDT"

    @property
    def BTC_USDT(self):
        return self.__BTC_USDT

    @property
    def ETH_BTC(self):
        return self.__ETH_BTC

    @property
    def ETH_USDT(self):
        return self.__ETH_USDT


class KlinePeriodConst:

    def __init__(self):
        self.__MIN_1 = "1m"
        self.__MIN_3 = "3m"
        self.__MIN_5 = "5m"
        self.__MIN_15 = "15m"
        self.__MIN_30 = "30m"
        self.__HOUR_1 = "1h"
        self.__HOUR_2 = "2h"
        self.__HOUR_4 = "4h"
        self.__HOUR_6 = "6h"
        self.__HOUR_8 = "8h"
        self.__HOUR_12 = "12h"
        self.__DAY_1 = "1d"
        self.__DAY_3 = "3d"
        self.__WEEK_1 = "1w"
        self.__MONTH_1 = "1M"

    @property
    def MIN_1(self):
        return self.__MIN_1

    @property
    def MIN_3(self):
        return self.__MIN_3

    @property
    def MIN_5(self):
        return self.__MIN_5

    @property
    def MIN_15(self):
        return self.__MIN_15

    @property
    def MIN_30(self):
        return self.__MIN_30

    @property
    def HOUR_1(self):
        return self.__HOUR_1

    @property
    def HOUR_2(self):
        return self.__HOUR_2

    @property
    def HOUR_4(self):
        return self.__HOUR_4

    @property
    def HOUR_6(self):
        return self.__HOUR_6

    @property
    def HOUR_8(self):
        return self.__HOUR_8

    @property
    def HOUR_12(self):
        return self.__HOUR_12

    @property
    def DAY_1(self):
        return self.__DAY_1

    @property
    def DAY_3(self):
        return self.__DAY_3

    @property
    def WEEK_1(self):
        return self.__WEEK_1

    @property
    def MONTH_1(self):
        return self.__MONTH_1


TC = TCConst()
Symbol = SymbolConst()
KlinePeriod = KlinePeriodConst()
