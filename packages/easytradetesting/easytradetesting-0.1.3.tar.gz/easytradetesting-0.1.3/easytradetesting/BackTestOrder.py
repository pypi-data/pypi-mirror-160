import copy
import decimal
import uuid
from datetime import datetime

from easytradesdk.entity.Order import Order
from easytradesdk.entity.Position import Position
from easytradesdk.support.Condition import OrderSignal


class BackTestOrder(Order):

    def __init__(self):
        super().__init__()
        self.posTotalAmountAfterDeal = None  # 交易后那一刻的仓位总价值金额

    @staticmethod
    def build(timeMills, tc, symbol, side, orderType, dealPrice, dealQuantity, strategyParams, posBeforeDeal, posAfterDeal, orderSignal: OrderSignal, orderData: dict):
        _order = BackTestOrder()
        _order.id = None
        _order.tc = tc  # BINANCE, HUO_BI
        _order.symbol = symbol  # BTC_USDT, ETH_USDT
        _order.clientOrderId = str(uuid.uuid4())
        _order.price = dealPrice  # 买卖价格, 市价单价格为0
        _order.totalQty = dealQuantity  # 下单量
        _order.dealQty = dealQuantity  # 实际成交量
        _order.type = orderType  # limit, market
        _order.side = side  # buy, sell
        _order.status = "DEALED"
        _order.time = datetime.utcfromtimestamp(timeMills / 1000)
        _order.timeMills = timeMills  # 下单时间戳, 对应回测时序执行的时间戳
        _order.actualDealQty = dealQuantity  # 扣除手续费之后的实际成交量
        _order.actualDealAmount = dealQuantity * dealPrice  # 扣除手续费之后的实际成交额
        _order.totalDealAmount = _order.actualDealAmount
        _order.totalFeeAmount = 0
        _order.strategyParams = strategyParams  # 下单时的策略参数
        _order.orderData = orderData  # 交易数据, dict 类型
        _order.orderSignal = copy.deepcopy(orderSignal)  # 交易信号对象
        _order.posBeforeDeal = posBeforeDeal  # 交易完成前的仓位信息
        _order.posAfterDeal = posAfterDeal  # 交易完成之后那一刻的仓位信息
        _order.posTotalAmountAfterDeal = _order.posAfterDeal.remainAmount + _order.posAfterDeal.remainHolding * dealPrice  # 交易完成之后那一刻仓位的总金额
        return _order

    def getObjectMapper(self):
        return {
            "time": datetime,
            "price": decimal.Decimal, "totalQty": decimal.Decimal,
            "dealQty": decimal.Decimal, "actualDealQty": decimal.Decimal,
            "actualDealAmount": decimal.Decimal, "totalFeeAmount": decimal.Decimal,
            "orderSignal": OrderSignal, "posBeforeDeal": Position, "posAfterDeal": Position, "orderData": dict, "strategyParams": dict
        }
