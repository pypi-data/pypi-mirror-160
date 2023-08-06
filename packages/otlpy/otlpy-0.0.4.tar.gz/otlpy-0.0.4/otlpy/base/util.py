import numpy as np


def bid_ticksize(price: float, ticksize: float) -> float:
    return float(np.floor(price / ticksize) * ticksize)


def ask_ticksize(price: float, ticksize: float) -> float:
    return float(np.ceil(price / ticksize) * ticksize)
