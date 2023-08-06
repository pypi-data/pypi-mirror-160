import decimal

from easytradesdk.AbsContext import AbsContext
from easytradesdk.Const import KlinePeriod


class BackTestContext(AbsContext):

    def __init__(self):
        self.__executePeriod = None
        self.__executingTimeMills = None
        self.__marketApi = None
        self.__tradeApi = None
        self.__positions = {}
        self.__strategyParams = {}

        self.dataSource = None
        self.memoryDataSource = None
        self.backTestStartTime = None
        self.backTestEndTime = None
        self.buySlippage = None
        self.sellSlippage = None
        self.backTestOrders = []

    def getPosition(self, tc, symbol):

        if self.__positions:
            _key = tc + ":" + symbol
            if _key in self.__positions:
                return self.__positions[_key]

        return None

    def getPositions(self):
        return self.__positions

    def setPositions(self, positions):
        self.__positions = positions

    def getStrategyParams(self):
        return self.__strategyParams

    def setStrategyParams(self, strategyParams):
        self.__strategyParams = strategyParams

    def getExecutePeriod(self):
        return self.__executePeriod

    def setExecutePeriod(self, executePeriod):
        self.__executePeriod = executePeriod

    def getExecutingTimeMills(self):
        return self.__executingTimeMills

    def setExecutingTimeMills(self, executingTimeMills):
        self.__executingTimeMills = executingTimeMills

    def getMarketApi(self):
        return self.__marketApi

    def setMarketApi(self, marketApi):
        self.__marketApi = marketApi

    def getTradeApi(self):
        return self.__tradeApi

    def setTradeApi(self, tradeApi):
        self.__tradeApi = tradeApi

    def updatePositionAfterDeal(self, tc, symbol, side, dealAmount, dealQuantity):

        """
            回测订单生成后更新仓位信息
            :param tc:              交易所
            :param symbol:          交易标的
            :param side:            交易方向
            :param dealAmount:      成交额
            :param dealQuantity:    成交量
            :return:
        """
        _position = self.getPosition(tc, symbol)

        if not _position:
            raise Exception("tc->{}, symbol->{}, position not initialized".format(tc, symbol))

        if side == 'buy':
            _offsetAmount = _position.remainAmount - dealAmount
            if _offsetAmount < 0:
                print("remain amount not enough")
                return False

            _position.remainAmount = _offsetAmount
            _position.remainHolding = _position.remainHolding + dealQuantity
            _position.lastDealAmount = dealAmount
            _position.lastDealQuantity = dealQuantity
        elif side == 'sell':
            _offsetQuantity = _position.remainHolding - dealQuantity
            if _offsetQuantity < 0:
                print("remain holding not enough")
                return False
            _position.remainAmount = _position.remainAmount + dealAmount
            _position.remainHolding = _offsetQuantity
            _position.lastDealAmount = dealAmount
            _position.lastDealQuantity = dealQuantity
        else:
            raise Exception("invalid side")
        return True

    def calculateMaxAvailableBuyQuantity(self, tc, symbol, amount=None, offsetPrice=None, scale=2):

        """
            根据仓位剩余金额、参数金额以及价格偏移量计算最大可购买量
            :param tc:      交易所
            :param symbol:  交易标的
            :param amount:  能够购买的最大金额, 如果是 None, 则使用仓位的剩余金额来计算，否则使用 amount 参数来计算
            :param offsetPrice:  价格偏移量默认为0，如果不为 0 则根据当前执行时序最近1分钟 K 线的开盘价 + offsetPrice 来计算
            :param scale:   保留精度，默认保留2位小数，不四舍五入
            :return:
        """

        _amount = amount

        if _amount is None:

            _position = self.getPosition(tc, symbol)

            if not _position:
                raise Exception("tc->{}, symbol->{}, position not initialized".format(tc, symbol))

            _amount = _position.remainAmount
        else:
            _amount = decimal.Decimal(str(amount))

        _currentTimeMills = self.getExecutingTimeMills()
        _klines = self.getMarketApi().fetchLatestKline(tc, symbol, KlinePeriod.MIN_1, endTimeMills=_currentTimeMills, limit=1)

        if _klines is None or len(_klines) == 0:
            raise Exception("No latest 1m kline found to " + str(_currentTimeMills) + " timeMills")

        _price = _klines[0].openingPrice

        if offsetPrice is not None:
            _price = _price + decimal.Decimal(str(offsetPrice))

        _slippage = self.buySlippage

        if _slippage and _slippage.value > 0:

            if _slippage.slippage_type == 1:
                _price = _price + _price * _slippage.value
            else:
                _price = _price + _slippage.value

        _pow = pow(10, scale)

        # 最大可购买量
        _quantity = decimal.Decimal(int(_amount / _price * _pow)) / decimal.Decimal(str(_pow))

        return _quantity
