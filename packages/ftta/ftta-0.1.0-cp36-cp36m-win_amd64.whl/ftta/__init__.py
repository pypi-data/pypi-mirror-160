
from . import _ftta
import numpy as np

def MA(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.MA(a.astype(np.float64), N)

def MA_A(a : np.ndarray, N : np.ndarray) -> np.ndarray:
	 return _ftta.MA_A(a.astype(np.float64), N.astype(np.float64))

def EMA(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.EMA(a.astype(np.float64), N)

def SMA(a : np.ndarray, N : int, M : int) -> np.ndarray:
	 return _ftta.SMA(a.astype(np.float64), N, M)

def WMA(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.WMA(a.astype(np.float64), N)

def DMA(a : np.ndarray, A : np.ndarray) -> np.ndarray:
	 return _ftta.DMA(a.astype(np.float64), A.astype(np.float64))

def COUNT(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.COUNT(a.astype(np.float64), N)

def COUNT_A(a : np.ndarray, N : np.ndarray) -> np.ndarray:
	 return _ftta.COUNT_A(a.astype(np.float64), N.astype(np.float64))

def SUM(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.SUM(a.astype(np.float64), N)

def SUM_A(a : np.ndarray, N : np.ndarray) -> np.ndarray:
	 return _ftta.SUM_A(a.astype(np.float64), N.astype(np.float64))

def REF(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.REF(a.astype(np.float64), N)

def REFIF(x : np.ndarray, c : np.ndarray, v : np.ndarray) -> np.ndarray:
	 return _ftta.REFIF(x.astype(np.float64), c.astype(np.float64), v.astype(np.float64))

def REFXV(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.REFXV(a.astype(np.float64), N)

def REF_A(a : np.ndarray, N : np.ndarray) -> np.ndarray:
	 return _ftta.REF_A(a.astype(np.float64), N.astype(np.float64))

def LLV(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.LLV(a.astype(np.float64), N)

def LLV_A(a : np.ndarray, N : np.ndarray) -> np.ndarray:
	 return _ftta.LLV_A(a.astype(np.float64), N.astype(np.float64))

def HHV(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.HHV(a.astype(np.float64), N)

def HHV_A(a : np.ndarray, N : np.ndarray) -> np.ndarray:
	 return _ftta.HHV_A(a.astype(np.float64), N.astype(np.float64))

def BARSINCE(x : np.ndarray) -> np.ndarray:
	 return _ftta.BARSINCE(x)

def BARLAST(x : np.ndarray) -> np.ndarray:
	 return _ftta.BARLAST(x)

def BARSLAST(x : np.ndarray) -> np.ndarray:
	 return _ftta.BARSLAST(x)

def CROSS(x : np.ndarray, y : np.ndarray) -> np.ndarray:
	 return _ftta.CROSS(x.astype(np.float64), y.astype(np.float64))

def FIF(x : np.ndarray, a : np.ndarray, b : np.ndarray) -> np.ndarray:
	 return _ftta.FIF(x, a.astype(np.float64), b.astype(np.float64))

def SLOPE(Y : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.SLOPE(Y.astype(np.float64), N)

def CURRBARSCOUNT(Y : np.ndarray) -> np.ndarray:
	 return _ftta.CURRBARSCOUNT(Y.astype(np.float64))

def BACKCOUNT(x : np.ndarray) -> np.ndarray:
	 return _ftta.BACKCOUNT(x)

def STD(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.STD(a.astype(np.float64), N)

def STDDEV(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.STDDEV(a.astype(np.float64), N)

def STDP(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.STDP(a.astype(np.float64), N)

def AVEDEV(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.AVEDEV(a.astype(np.float64), N)

def FILTER(a : np.ndarray, N : int) -> np.ndarray:
	 return _ftta.FILTER(a.astype(np.float64), N)

