import copy
import decimal

from easytradesdk.Const import KlinePeriod

from easytradetesting.BackTestContext import BackTestContext
from easytradetesting.BackTestOrder import BackTestOrder
from easytradesdk.AbsTradeApi import AbsTradeApi
from easytradesdk.support.Condition import OrderSignal


class TradeApi(AbsTradeApi):

    def __init__(self, backTestContext: BackTestContext):
        self.__backTestContext = backTestContext

    def getOrder(self, clientOrderId):

        """
            从数据库中获取回测订单
            :param clientOrderId:
            :return:
        """

        return self.__backTestContext.dataSource.getBackTestOrder(clientOrderId)

    def queryOrders(self, startTimeMills=None, endTimeMills=None, tc=None, symbol=None, instanceId=None, limit=50):

        """
            从数据库查询回测订单
            :param startTimeMills:
            :param endTimeMills:
            :param tc:
            :param symbol:
            :param instanceId:
            :param limit:   default is 50
            :return:
        """
        return self.__backTestContext.dataSource.queryBackTestOrders(startTimeMills=startTimeMills, endTimeMills=endTimeMills, tc=tc, symbol=symbol, limit=limit)

    def addMarketOrder(self, tc, symbol, quantity: decimal, side, qtyScale=2, orderSignal: OrderSignal = None, orderData: dict = None):

        """
        市价买入
        :param tc:
        :param symbol:
        :param quantity:
        :param side:
        :param qtyScale:
        :param orderSignal:
        :param orderData:
        :return:
        """

        if not qtyScale:
            qtyScale = 2

        _currentTimeMills = self.__backTestContext.getExecutingTimeMills()
        _klines = self.__backTestContext.getMarketApi().fetchLatestKline(tc, symbol, KlinePeriod.MIN_1, endTimeMills=_currentTimeMills, limit=1)

        if _klines is None or len(_klines) == 0:
            raise Exception("No latest 1m kline found to " + str(_currentTimeMills) + " timeMills")

        _orderData = orderData if orderData else {}
        _price = _klines[0].openingPrice
        _pow = decimal.Decimal(pow(10, qtyScale))
        _quantity = decimal.Decimal(str(quantity))
        _quantity = decimal.Decimal(int(_quantity * _pow)) / _pow

        _buySlippage = self.__backTestContext.buySlippage
        _sellSlippage = self.__backTestContext.sellSlippage

        if side == 'buy' and _buySlippage and _buySlippage.value > 0:
            if _buySlippage.slippageType == 1:
                _price = _price + _price * _buySlippage.value
            else:
                _price = _price + _buySlippage.value
        if side == 'sell' and _sellSlippage and _sellSlippage.value > 0:
            if _sellSlippage.slippageType == 1:
                _price = _price - _price * _sellSlippage.value
            else:
                _price = _price - _sellSlippage.value

        _positionsBeforeDeal = copy.deepcopy(self.__backTestContext.getPosition(tc, symbol))

        _success = self.__backTestContext.updatePositionAfterDeal(tc, symbol, side, _price * _quantity, _quantity)
        if not _success:
            print("order failed")
            return None

        _positionsAfterDeal = copy.deepcopy(self.__backTestContext.getPosition(tc, symbol))

        orderSignal.executedCallBack()

        _testOrder = BackTestOrder.build(
            _currentTimeMills, tc, symbol, side, "market", _price, _quantity,
            self.__backTestContext.getStrategyParams(), _positionsBeforeDeal, _positionsAfterDeal, orderSignal, orderData)

        self.__backTestContext.dataSource.saveBackTestOrder(_testOrder)
        self.__backTestContext.backTestOrders.append(_testOrder)

        return _testOrder

    def addLimitOrder(self, tc, symbol, price: decimal.Decimal, quantity: decimal.Decimal, side, qtyScale=2, orderSignal: OrderSignal = None,
                      orderData: dict = None):

        raise Exception("limit order not supported")

    def buyMarketOrder(self, tc, symbol, quantity: decimal.Decimal, qtyScale=2, orderSignal: OrderSignal = None, orderData: dict = None):
        return self.addMarketOrder(tc, symbol, quantity, 'buy', qtyScale, orderSignal, orderData)

    def sellMarketOrder(self, tc, symbol, quantity: decimal.Decimal, qtyScale=2, orderSignal: OrderSignal = None, orderData: dict = None):
        return self.addMarketOrder(tc, symbol, quantity, 'sell', qtyScale, orderSignal, orderData)

    def buyLimitOrder(self, tc, symbol, price: decimal.Decimal, quantity: decimal.Decimal, qtyScale=2, orderSignal: OrderSignal = None, orderData: dict = None):
        return self.addLimitOrder(tc, symbol, price, quantity, 'buy', qtyScale, orderSignal, orderData)

    def sellLimitOrder(self, tc, symbol, price: decimal.Decimal, quantity: decimal.Decimal, qtyScale=2, orderSignal: OrderSignal = None, orderData: dict = None):
        return self.addLimitOrder(tc, symbol, price, quantity, 'sell', qtyScale, orderSignal, orderData)
