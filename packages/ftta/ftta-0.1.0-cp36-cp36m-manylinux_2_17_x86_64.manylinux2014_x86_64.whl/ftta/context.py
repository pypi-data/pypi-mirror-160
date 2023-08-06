from typing import Any, Dict, List
import numpy as np
import json
import ftta.draw


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, ftta.draw.DRAWNUMBER):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)




class FormulaResult():
    """ 指标计算结果 """
    def get(self, name: str) -> np.ndarray:
        """ 获取指标结果中某一条线的数据 """
        pass

    def line(self, name: str) -> Dict[str, Any]:
        """ 获取指标结果中某一条线, 包括数据和属性 """
        pass

    def lines(self) -> List[Dict[str, Any]]:
        """ 获取所有线 """
        pass

class FormulaRef():
    """ 指标引用 """

    def execute(self, *agrs) -> FormulaResult:
        pass

class FormulaCtx:
    """ 指标运行时，提供指标运行必要的基础，如数据，代码列表，引用等 """
    def D(self, field: str, code: str, period: str) -> np.ndarray:
        """ 取序列数据函数 """
        pass

    def F(self, name: str, period: str) -> FormulaRef:
        """ 引用其他指标函数 """
        pass

class FormulaDataFeed:
    def kline(self, field: str, code: str, period: str) -> np.ndarray:
        """ 取K线数据 """
        pass
    def captial(self, field: str, code: str) -> np.ndarray:
        """ 取财务数据函数，一般需要将其向量化填充 """
        pass

    def set_main_code(self, code: str):
        """ 设置主代码，其他代码的数据将以主代码的日期进行对齐 """
        pass

class DummyFormulaResult(FormulaResult):
    def get(self, name: str):
        return np.arange(10.0, dtype=np.float64)


class DummyFormula(FormulaRef):

    def __init__(self, name: str, period: str) -> None:
        self.name = name
        self.period = period

    def execute(self, *agrs):
        return DummyFormulaResult()

class DummyFeed(FormulaDataFeed):

    def kline(self, field: str, code: str, period: str) -> np.ndarray:
        return np.arange(10, dtype=np.float64)


class SimpleFormulaCtx(FormulaCtx):

    def __init__(self, feed) -> None:
        self.code = 'sh000001'
        self.period = ''
        self.feed = feed
        self.feed.set_main_code(self.code)

    def D(self, field: str, code: str, period: str) -> np.ndarray:
        if len(period) == 0:
            period = self.period
            
        return self.feed.kline(field, code, period)

    def F(self, name: str, period: str) -> DummyFormula:
        return DummyFormula(name, period)


def ctx(feed = None) -> FormulaCtx:
    if feed == None:
        feed = DummyFeed()
    return SimpleFormulaCtx(feed)

