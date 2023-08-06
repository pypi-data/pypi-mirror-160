from typing import Any, Dict
import numpy as np

class DRAWNUMBER:
    def __init__(self, cond: np.ndarray, price: np.ndarray, var: Any, offset: float = 0) -> None:
        #self.cond = cond
        #self.price = price
        #self.var = var
        self.signs = list(map(lambda v: (*v, var), filter(lambda x: x[0] != '0', zip(range(len(cond)), price, cond))))
        self.offset = offset

    def __call__(self, line: Dict[str, Any]) -> Any:
        line['option']['style'] = 'draw'
        line['name'] = ''