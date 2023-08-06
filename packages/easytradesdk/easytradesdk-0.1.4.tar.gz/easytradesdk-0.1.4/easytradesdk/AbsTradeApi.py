import abc
import decimal
from easytradesdk.support.Condition import OrderSignal


class AbsTradeApi(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def getOrder(self, clientOrderId):
        """
            根据用户订单ID获取订单信息
            :param clientOrderId: 订单编号
            :return:
        """
        pass

    @abc.abstractmethod
    def queryOrders(self, startTimeMills=None, endTimeMills=None, tc=None, symbol=None, instanceId=None, limit=50):
        """
            根据订单时间戳查询订单信息，默认查询50条数据
            :param tc:              交易所
            :param symbol:          交易标的
            :param startTimeMills:  开始时间（下单时间）
            :param endTimeMills:    结束时间戳（下单时间）
            :param instanceId:      实例编号
            :param limit: default = 50
            :return:
        """
        pass

    # 下市价买单
    @abc.abstractmethod
    def buyMarketOrder(self, tc, symbol, quantity: decimal.Decimal, qtyScale=2, orderSignal: OrderSignal = None, orderData: dict = None):
        pass

    # 下市价卖单
    @abc.abstractmethod
    def sellMarketOrder(self, tc, symbol, quantity: decimal.Decimal, qtyScale=2, orderSignal: OrderSignal = None, orderData: dict = None):
        pass

    # 限价买单
    @abc.abstractmethod
    def buyLimitOrder(self, tc, symbol, price: decimal.Decimal, quantity: decimal.Decimal, qtyScale=2, orderSignal: OrderSignal = None, orderData: dict = None):
        pass

    # 限价卖单
    @abc.abstractmethod
    def sellLimitOrder(self, tc, symbol, price: decimal.Decimal, quantity: decimal.Decimal, qtyScale=2, orderSignal: OrderSignal = None, orderData: dict = None):
        pass
