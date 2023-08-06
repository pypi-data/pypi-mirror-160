import pymysql

from easytradetesting.BackTestOrder import BackTestOrder
from easytradetesting.DataSource import DataSource
from easytradesdk import Serializer
from easytradesdk.entity.Kline import Kline


class MySqlDataSource(DataSource):

    def __init__(self, host="localhost", port=3306, user=None, password=None, database=None):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database
        self.__connection = self.connect()

    def connect(self):

        """
            连接数据库
            :return:
        """
        return pymysql.connect(host=self.__host,
                               port=self.__port,
                               user=self.__user,
                               password=self.__password,
                               database=self.__database,
                               charset="utf8")

    def close(self):

        """
            关闭数据库连接
            :return:
        """
        self.__connection.close()

    def createKlineTable(self, tc, symbol, klinePeriod):

        """
            创建K线表，若表已经存在则不再进行创建
            :param tc:              交易所
            :param symbol:          交易标的
            :param klinePeriod:   K线周期
            :return: 
        """""
        sql = """
            CREATE TABLE IF NOT EXISTS `${tableName}` (
            `timeMills` bigint(20) unsigned NOT NULL COMMENT 'K线起始时间戳',
            `endTimeMills` bigint(20) unsigned DEFAULT NULL COMMENT 'K线结束时间戳',
            `startTime` datetime NOT NULL COMMENT 'K线起始时间',
            `endTime` datetime DEFAULT NULL COMMENT 'K线结束时间',
            `tc` varchar(30) DEFAULT NULL COMMENT '交易所',
            `symbol` varchar(30) DEFAULT NULL COMMENT '交易标的',
            `timeInterval` varchar(10) DEFAULT NULL COMMENT 'K线周期',
            `openingPrice` decimal(30,10) NOT NULL COMMENT 'K线第一笔成交价（开盘价）',
            `closingPrice` decimal(30,10) NOT NULL COMMENT 'K线最后一笔成交价（收盘价）',
            `highPrice` decimal(30,10) NOT NULL COMMENT 'K线期间最高价（最高价）',
            `lowPrice` decimal(30,10) NOT NULL COMMENT 'K线期间最低价（最低价）',
            `volume` decimal(30,10) DEFAULT NULL COMMENT 'K线期间成交额',
            `quantity` decimal(30,10) DEFAULT NULL COMMENT 'K线期间成交量',
            `cnt` int(10) DEFAULT NULL COMMENT 'K线期间成交笔数',
            `buyVolume` decimal(30,10) DEFAULT NULL COMMENT '主动买入成交额',
            `buyQuantity` decimal(30,10) DEFAULT NULL COMMENT '主动买入成交量',
            PRIMARY KEY (`timeMills`),
            KEY `idx_endTimeMills` (`endTimeMills`) USING BTREE,
            KEY `idx_startTime` (`startTime`) USING BTREE,
            KEY `idx_endTime` (`endTime`) USING BTREE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """

        sql = sql.replace("${tableName}", DataSource.resolveKlineTableName(tc, symbol, klinePeriod))
        cursor = self.__connection.cursor()

        try:
            cursor.execute(sql)
        finally:
            cursor.close()

    def saveKline(self, tc, symbol, klinePeriod, kline):

        """
            保存单个K线数据, K 线重复将不会报错，可以重复执行
            :param tc:              交易所
            :param symbol:          交易标的
            :param kline:           k线对象
            :param klinePeriod:   k线时间戳
            :return:
        """
        cursor = self.__connection.cursor()
        if kline is None:
            return

        sql = 'insert ignore into ' + DataSource.resolveKlineTableName(tc, symbol, klinePeriod) + \
              ' (timeMills,endTimeMills,startTime,endTime,tc,symbol,timeInterval,openingPrice,closingPrice,highPrice,lowPrice,' \
              ' volume,quantity,cnt,buyVolume,buyQuantity)' \
              ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        try:
            cursor.execute(sql, (kline.timeMills, kline.endTimeMills,
                                 kline.startTime, kline.endTime,
                                 kline.tc, kline.symbol, kline.timeInterval,
                                 kline.openingPrice, kline.closingPrice,
                                 kline.highPrice, kline.lowPrice,
                                 kline.volume, kline.quantity,
                                 kline.cnt, kline.buyVolume, kline.buyQuantity))
            self.__connection.commit()
        finally:
            cursor.close()

    def saveKlines(self, tc, symbol, klinePeriod, klines):

        """
            批量保存k线数据，如果遇到重复，将报错并回滚
            :param tc:      交易所
            :param symbol:  交易标的
            :param klinePeriod:  k线周期
            :param klines:  K线对象列表
            :return:
        """
        cursor = self.__connection.cursor()
        if klines:
            data = ((klines[i].timeMills, klines[i].endTimeMills,
                     klines[i].startTime, klines[i].endTime,
                     klines[i].tc, klines[i].symbol, klines[i].timeInterval,
                     klines[i].openingPrice, klines[i].closingPrice,
                     klines[i].highPrice, klines[i].lowPrice,
                     klines[i].volume, klines[i].quantity,
                     klines[i].cnt, klines[i].buyVolume, klines[i].buyQuantity) for i in range(0, len(klines)))
            sql = 'insert into ' + DataSource.resolveKlineTableName(tc, symbol, klinePeriod) + \
                  ' (timeMills,endTimeMills,startTime,endTime,tc,symbol,timeInterval,openingPrice,closingPrice,highPrice,lowPrice,' \
                  ' volume,quantity,cnt,buyVolume,buyQuantity)' \
                  ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
                cursor.executemany(sql, data)
                self.__connection.commit()
            except Exception as e:
                self.__connection.rollback()
            finally:
                cursor.close()

    def queryKline(self, tc, symbol, klinePeriod, startTimeMills=None, endTimeMills=None, limit=200):

        """
            从数据库查询 K 线数据
            :param tc:              交易所
            :param symbol:          交易标的
            :param klinePeriod:     K 线周期
            :param startTimeMills:   开始时间戳   开始时间戳和结束时间戳两者必须填一个
            :param endTimeMills:     结束时间戳
            :param limit:           记录数，默认 200
        :return:   k 线对象列表
        """

        if startTimeMills is None and endTimeMills is None:
            raise Exception("startTimeMills or endTimeMills is required")
        params = []
        sql = "select * from " + DataSource.resolveKlineTableName(tc, symbol, klinePeriod) + " where 1=1"
        if startTimeMills is not None:
            sql += " and timeMills >= %s"
            params.append(startTimeMills)
        if endTimeMills is not None:
            sql += " and timeMills <= %s"
            params.append(endTimeMills)
        sql += " order by timeMills asc limit %s"
        params.append(limit)

        cursor = self.__connection.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql, params)
            return Serializer.dictListToObjectList(cursor.fetchall(), Kline)
        finally:
            cursor.close()

    def queryLatestKline(self, tc, symbol, klinePeriod, endTimeMills=None, limit=200):

        """
            查询最近的 K 线，按照K线时间升序排序¬
            :param tc:              交易所
            :param symbol:          交易标的
            :param klinePeriod:        K 线周期
            :param endTimeMills:    K线截止时间
            :param limit:           记录数，默认 200
            :return:
        """
        params = []
        sql = "select * from " + DataSource.resolveKlineTableName(tc, symbol, klinePeriod) + " where 1=1 "
        if endTimeMills:
            sql += " and timeMills <= %s"
            params.append(endTimeMills)
        sql += " order by timeMills desc limit %s"
        params.append(limit)

        cursor = self.__connection.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql, params)
            klines = Serializer.dictListToObjectList(cursor.fetchall(), Kline)
            if len(klines) > 0:
                klines.sort(key=lambda x: x.timeMills, reverse=False)
            return klines
        finally:
            cursor.close()

    def countKline(self, tc, symbol, klinePeriod, startTimeMills=None, endTimeMills=None):
        """
            查询 K 线数量
            :param tc:
            :param symbol:
            :param klinePeriod:
            :param startTimeMills:
            :param endTimeMills:
            :return:
        """
        params = []
        sql = "select count(*) as cnt from " + DataSource.resolveKlineTableName(tc, symbol, klinePeriod) + " where 1=1 "

        if startTimeMills is not None:
            sql += " and timeMills >= %s"
            params.append(startTimeMills)
        if endTimeMills is not None:
            sql += " and timeMills <= %s"
            params.append(endTimeMills)

        cursor = self.__connection.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql, params)
            return cursor.fetchone()['cnt']
        finally:
            cursor.close()

    def createBackTestOrderTable(self):

        sql = """
                CREATE TABLE IF NOT EXISTS `${tableName}` (
                `id` int(10) NOT NULL AUTO_INCREMENT,
                `clientOrderId` varchar(50) NOT NULL COMMENT '订单id',
                `tc` varchar(30) DEFAULT NULL COMMENT '交易所',
                `symbol` varchar(30) DEFAULT NULL COMMENT '交易标的',
                `price` decimal(30,10) DEFAULT NULL COMMENT '成交价',
                `totalQty` decimal(30,10) DEFAULT NULL COMMENT '挂单量',
                `dealQty` decimal(30,10) DEFAULT NULL COMMENT '成交量',
                `type` varchar(20) DEFAULT NULL COMMENT '交易类型: limit, market',
                `side` varchar(20) DEFAULT NULL COMMENT '交易方向: buy, sell',
                `status` varchar(30) DEFAULT NULL COMMENT '交易状态, FILLED(完全成交)',
                `actualDealQty` decimal(30,10) DEFAULT NULL COMMENT '实际成交量',
                `actualDealAmount` decimal(30,10) DEFAULT NULL COMMENT '实际成交额',
                `time` datetime DEFAULT NULL COMMENT '下单时间 (对应回测时序的那个时间)',
                `timeMills` bigint(20) DEFAULT NULL COMMENT '下单时间戳（对应回测时序的那个时间戳）',
                `orderSignal` json DEFAULT NULL COMMENT 'json 格式订单信号数据',
                `orderData` json DEFAULT NULL COMMENT 'jsoN 格式订单数据(用户自定义的一些数据)',
                `posBeforeDeal` json DEFAULT NULL COMMENT '交易前仓位快照',
                `posAfterDeal` json DEFAULT NULL COMMENT '交易后仓位快照',
                `posTotalAmountAfterDeal` decimal(30,10) DEFAULT NULL COMMENT '交易后仓位总价值金额',
                PRIMARY KEY (`id`),
                UNIQUE KEY `uk_clientOrderId` (`clientOrderId`) USING BTREE,
                KEY `idx_time` (`time`) USING BTREE,
                KEY `idx_timeMills` (`timeMills`) USING BTREE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """

        sql = sql.replace("${tableName}", DataSource.resolveBackTestOrderTableName())
        cursor = self.__connection.cursor()

        try:
            cursor.execute(sql)
        finally:
            cursor.close()

    def saveBackTestOrder(self, backTestOrder):

        """
            保存回测订单
            :param backTestOrder:
            :return:
        """
        cursor = self.__connection.cursor()

        data = (backTestOrder.clientOrderId, backTestOrder.tc,
                backTestOrder.symbol, backTestOrder.price,
                backTestOrder.totalQty, backTestOrder.dealQty,
                backTestOrder.type, backTestOrder.side,
                backTestOrder.status, backTestOrder.actualDealQty,
                backTestOrder.actualDealAmount, backTestOrder.time, backTestOrder.timeMills,
                Serializer.objectToJson(backTestOrder.orderSignal), Serializer.objectToJson(backTestOrder.orderData),
                Serializer.objectToJson(backTestOrder.posBeforeDeal), Serializer.objectToJson(backTestOrder.posAfterDeal),
                backTestOrder.posTotalAmountAfterDeal)

        sql = 'insert into ' + DataSource.resolveBackTestOrderTableName() + \
              ' (clientOrderId,tc,symbol,price,totalQty,dealQty,type,side,status,actualDealQty,' \
              ' actualDealAmount,time,timeMills,orderSignal,orderData,posBeforeDeal,posAfterDeal,posTotalAmountAfterDeal)' \
              ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql, data)
            backTestOrder.id = self.__connection.insert_id()
            self.__connection.commit()
        except Exception as e:
            self.__connection.rollback()
            raise Exception(e)
        finally:
            cursor.close()

    def saveBackTestOrders(self, backTestOrders, deleteDataBeforeSave=False):

        """
            批量保存回测订单
            :param backTestOrders:
            :param deleteDataBeforeSave:
            :return:
        """

        cursor = self.__connection.cursor()

        data = ((backTestOrders[i].clientOrderId, backTestOrders[i].tc,
                 backTestOrders[i].symbol, backTestOrders[i].price,
                 backTestOrders[i].totalQty, backTestOrders[i].dealQty,
                 backTestOrders[i].type, backTestOrders[i].side,
                 backTestOrders[i].status, backTestOrders[i].actualDealQty,
                 backTestOrders[i].actualDealAmount, backTestOrders[i].time, backTestOrders[i].timeMills,
                 Serializer.objectToJson(backTestOrders[i].orderSignal), Serializer.objectToJson(backTestOrders[i].orderData),
                 Serializer.objectToJson(backTestOrders[i].posBeforeDeal), Serializer.objectToJson(backTestOrders[i].posAfterDeal),
                 backTestOrders[i].posTotalAmountAfterDeal) for i in range(0, len(backTestOrders)))

        sql = 'insert into ' + DataSource.resolveBackTestOrderTableName() + \
              ' (clientOrderId,tc,symbol,price,totalQty,dealQty,type,side,status,actualDealQty,' \
              ' actualDealAmount,time,timeMills,orderSignal,orderData,posBeforeDeal,posAfterDeal,posTotalAmountAfterDeal)' \
              ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.executemany(sql, data)
            self.__connection.commit()
        except Exception as e:
            self.__connection.rollback()
            raise Exception(e)
        finally:
            cursor.close()

    def getBackTestOrder(self, clientOrderId):

        """
            根据订单号获取回测订单
            :param clientOrderId:
            :return:
        """

        if not clientOrderId:
            raise Exception("clientOrderId is required")

        sql = "select * from " + DataSource.resolveBackTestOrderTableName() + " where clientOrderId = %s"

        cursor = self.__connection.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql, [clientOrderId])
            return Serializer.dictToObject(cursor.fetchone(), BackTestOrder)
        finally:
            cursor.close()

    def queryBackTestOrders(self, startTimeMills=None, endTimeMills=None, tc=None, symbol=None, limit=50):

        """
            查询回测订单
            :param startTimeMills:     开始时间，下单时对应的时间周期
            :param endTimeMills:       结束时间，下单时对应的时间周期
            :param tc:
            :param symbol:
            :param limit:
            :return:
        """
        params = []
        sql = "select * from " + DataSource.resolveBackTestOrderTableName() + " where 1=1"

        if tc:
            params.append(tc)
            sql += "and tc= %s"
        if symbol:
            params.append(symbol)
            sql += "and symbol= %s"
        if startTimeMills:
            params.append(startTimeMills)
            sql += " and timeMills >= %s"
        if endTimeMills:
            params.append(endTimeMills)
            sql += " and timeMills <= %s"
        params.append(limit)
        sql += " order by timeMills asc limit %s"
        cursor = self.__connection.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql, params)
            return Serializer.dictListToObjectList(cursor.fetchall(), BackTestOrder)
        finally:
            cursor.close()

    def truncateBackTestOrders(self):

        sql = "truncate table " + DataSource.resolveBackTestOrderTableName()
        cursor = self.__connection.cursor()

        try:
            cursor.execute(sql)
        finally:
            cursor.close()
