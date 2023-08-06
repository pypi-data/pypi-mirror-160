import abc


class AbsInstance(metaclass=abc.ABCMeta):

    # 实例初始化
    @abc.abstractmethod
    def init(self, context):
        pass

    # 实例销毁
    @abc.abstractmethod
    def destroy(self, context):
        pass

    # 实例执行函数，子类需要重写
    @abc.abstractmethod
    def execute(self, context):
        pass

    @abc.abstractmethod
    def executeStopLoss(self, context):
        pass

    @abc.abstractmethod
    def executeStopProfit(self, context):
        pass


class Instance(AbsInstance):

    def __init__(self):
        # 延时执行, 默认6秒
        self.executeDelaySeconds = 6

    def init(self, context):
        pass

    # 实例销毁
    def destroy(self, context):
        pass

    # 实例执行函数，子类需要重写
    def execute(self, context):
        pass

    # 默认的止损算法，子类可以重写
    def executeStopLoss(self, context):
        pass

    # 执行止盈操作, 子类可以重写
    def executeStopProfit(self, context):
        pass
