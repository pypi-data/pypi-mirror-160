import hashlib
import hmac
import json

import requests

from easytradesdk import Serializer
from easytradesdk.entity.Kline import Kline


class DataFetcher:

    def __init__(self, serverAddress, apiKey, secret, https=True):

        if serverAddress is None:
            raise Exception('serverAddress is blank')

        if serverAddress.startswith('http://') or serverAddress.startswith('https://'):
            if https and not serverAddress.startswith("https://"):
                raise Exception("server address should use https")
            self.__serverAddress = serverAddress
        else:
            self.__serverAddress = ("https://" if https else "http://") + serverAddress

        self.__apiKey = apiKey
        self.__secret = secret
        self.URL_MARKET_GET_KLINE = self.__serverAddress + "/kline/list"
        self.URL_MARKET_GET_LATEST_KLINE = self.__serverAddress + "/kline/list/latest"
        self.URL_MARKET_COUNT_KLINE = self.__serverAddress + "/kline/count"

        self.__apiKey = apiKey
        self.__secret = secret

    def fetchKline(self, tc, symbol, klinePeriod, startTimeMills=None, endTimeMills=None, limit=200):

        """
            根据k线时间查询K线，返回结果按照K线时间升序排序
            :param tc:          交易所
            :param symbol:      交易标的
            :param klinePeriod: K 线周期
            :param startTimeMills:   开始时间戳
            :param endTimeMills:     结束时间戳
            :param limit:       查询数量, 默认200, 服务器最多一次返回1000条
        :return:
        """

        if startTimeMills is None and endTimeMills is None:
            raise Exception("startTimeMills or endTimeMills is required")

        postData = {
            "tc": tc,
            "symbol": symbol,
            "klineInterval": klinePeriod,
            "startTimeMills": startTimeMills,
            "endTimeMills": endTimeMills,
            "limit": limit,
            "apiKey": self.__apiKey
        }
        _sign = self.__sign(postData)
        postData['sign'] = _sign

        res = requests.post(self.URL_MARKET_GET_KLINE, postData)
        result = json.loads(res.text)
        if result["code"] == 0:
            return Serializer.dictListToObjectList(result["data"], Kline)
        else:
            raise Exception(result["msg"])

    def fetchLatestKline(self, tc, symbol, klinePeriod, endTimeMills=None, limit=200):

        """
            查询最近k线数据, 返回结果按照K线时间升序排序
            :param tc:          交易所
            :param symbol:      交易标的
            :param klinePeriod: K 线周期
            :param endTimeMills:    截止时间戳
            :param limit:       查询数量, 默认200, 服务器最多一次返回1000条
        :return:
        """
        postData = {
            "tc": tc,
            "symbol": symbol,
            "klineInterval": klinePeriod,
            "endTimeMills": endTimeMills,
            "limit": limit,
            "apiKey": self.__apiKey
        }
        _sign = self.__sign(postData)
        postData['sign'] = _sign

        res = requests.post(self.URL_MARKET_GET_LATEST_KLINE, postData)
        result = json.loads(res.text)
        if result["code"] == 0:
            return Serializer.dictListToObjectList(result["data"], Kline)
        else:
            raise Exception(result["msg"])

    def countKline(self, tc, symbol, klinePeriod, startTimeMills=None, endTimeMills=None):

        if startTimeMills is None and endTimeMills is None:
            raise Exception("startTimeMills or endTimeMills is required")

        postData = {
            "tc": tc,
            "symbol": symbol,
            "klineInterval": klinePeriod,
            "startTimeMills": startTimeMills,
            "endTimeMills": endTimeMills,
            "apiKey": self.__apiKey
        }

        _sign = self.__sign(postData)
        postData['sign'] = _sign

        res = requests.post(self.URL_MARKET_COUNT_KLINE, postData)
        result = json.loads(res.text)

        if result["code"] == 0:
            return result['data']
        else:
            raise Exception(result["msg"])

    def __sign(self, data: dict):

        for key in list(data.keys()):
            if not data.get(key):
                del data[key]

        data = {k: data[k] for k in sorted(data)}
        _sign = '&'.join(['{0}={1}'.format(k, v) for k, v in data.items()])
        _sign = hmac.new(self.__secret.encode('utf-8'), _sign.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        return _sign
