import abc


class DataSource(metaclass=abc.ABCMeta):

    @staticmethod
    def resolveKlineTableName(tc, symbol, klinePeriod):
        return "easytrade_kline_" + tc.lower() + "_" + symbol.lower() + "_" + klinePeriod

    @staticmethod
    def resolveBackTestOrderTableName():
        return "easytrade_backtestorder"

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    def createKlineTable(self, tc, symbol, klinePeriod):
        pass

    @abc.abstractmethod
    def saveKline(self, tc, symbol, klinePeriod, kline):
        pass

    @abc.abstractmethod
    def saveKlines(self, tc, symbol, klinePeriod, klines):
        pass

    @abc.abstractmethod
    def queryKline(self, tc, symbol, klinePeriod, startTimeMills=None, endTimeMills=None, limit=200):
        pass

    @abc.abstractmethod
    def queryLatestKline(self, tc, symbol, klinePeriod, endTimeMills=None, limit=200):
        pass

    @abc.abstractmethod
    def countKline(self, tc, symbol, klinePeriod, startTimeMills=None, endTimeMills=None):
        pass

    @abc.abstractmethod
    def createBackTestOrderTable(self):
        pass

    @abc.abstractmethod
    def saveBackTestOrder(self, backTestOrder):
        pass

    @abc.abstractmethod
    def saveBackTestOrders(self, backTestOrders):
        pass

    @abc.abstractmethod
    def getBackTestOrder(self, clientOrderId):
        pass

    @abc.abstractmethod
    def queryBackTestOrders(self, startTimeMills=None, endTimeMills=None, tc=None, symbol=None, limit=50):
        pass

    @abc.abstractmethod
    def truncateBackTestOrders(self):
        pass
