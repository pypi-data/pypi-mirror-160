import datetime
import decimal

from easytradesdk.Serializer import DeserializableObject
from easytradesdk.entity.Position import Position
from easytradesdk.support.Condition import OrderSignal


class Order(DeserializableObject):

    def __init__(self):
        self.instanceId = None  # 实例编号
        self.strategyInstanceType = None  # 实例类型
        self.tc = None  # 交易所
        self.symbol = None  # 交易标的
        self.orderId = None # 交易所订单编号
        self.clientOrderId = None  # 生成的客户端订单ID
        self.price = None  # 买卖价格, 市价单价格为0
        self.totalQty = None  # 下单量
        self.dealQty = None  # 实际成交量
        self.type = None  # limit, market
        self.side = None  # buy, sell
        self.status = None  # new, partially_dealed, dealed, rejected, expired
        self.time = None
        self.timeMills = None
        self.updateTimeMills = None
        self.totalDealAmount = None
        self.totalFeeAmount = None  # 手续费金额
        self.feeSymbol = None  # 手续费标的
        self.dealDetails = None  # 手续费标的
        self.strategyParams = None  # 下单时的策略参数
        self.orderData = None  # 用户订单数据
        self.orderSignal = None  # 订单信号数据
        self.actualDealQty = None  # 扣除手续费之后的实际成交量
        self.actualDealAmount = None  # 扣除手续费之后的实际成交额
        self.posBeforeDeal = None  # 交易前那一刻的仓位, 仅实盘有值
        self.posAfterDeal = None  # 交易后那一刻的仓位, 仅实盘有值
        self.positions = None

    def getObjectMapper(self):
        return {
            "time": datetime.datetime,
            "price": decimal.Decimal, "totalQty": decimal.Decimal,
            "dealQty": decimal.Decimal, "actualDealQty": decimal.Decimal,
            "actualDealAmount": decimal.Decimal, "totalFeeAmount": decimal.Decimal, "totalDealAmount": decimal.Decimal,
            "strategyParams": dict, "orderData": dict, "orderSignal": OrderSignal, "positions": Position}
