from utils import assert_msg, crossover, SMA
import abc
import numpy as np
from typing import Callable


class Strategy(metaclass=abc.ABCMeta):
    """
    Abstract strategy class

    For your own strategy, you need to implement these two methods:
    Strategy.init
    Strategy.next
    """

    def __init__(self, broker, data):
        """
        Construct strategy object

        @params broker:  ExchangeAPI    API interface
        @params data:    list           market data
        """
        self._indicators = []
        self._broker = broker
        self._data = data
        self._tick = 0

    def I(self, func: Callable, *args) -> np.ndarray:
        """
        Calculate buy/sell direction vector.
        The vector is an array, the length corresponds to historical data.
        It is used to decide whether to buy or sell on a give point in time.

        An example for SMA:
        def init():
            self.sma = self.I(utils.SMA, self.data.Close, N)
        """
        value = func(*args)
        value = np.asarray(value)
        assert_msg(value.shape[-1] == len(self._data.Close),
                   'The length of the direction vector mus the same as the length of the dataset.')

        self._indicators.append(value)
        return value

    @property
    def tick(self):
        return self._tick

    @abc.abstractmethod
    def init(self):
        """
        Initialize strategy.
        You can also calculate certain parameters for the strategy here, for example:
        Based on historical data, one can:
        - calculate buy/sell direction vector
        - train model/initialize model parameters
        """
        pass

    @abc.abstractmethod
    def next(self, tick):
        """
        Step through and execute the strategy on a certain tick.
        A tick is a point in time.
        data[tick] is the market price at tick.
        """
        pass

    def buy(self):
        self._broker.buy()

    def sell(self):
        self._broker.sell()

    @property
    def data(self):
        return self._data


class SmaCross(Strategy):
    # size of small window SMA
    fast = 30

    # size of big window SMA
    slow = 90

    def init(self):
        # calculate both fast and slow SMA on every tick
        self.sma1 = self.I(SMA, self.data.Close, self.fast)
        self.sma2 = self.I(SMA, self.data.Close, self.slow)

    def next(self, tick):
        # buy all, if fast passes slow
        if crossover(self.sma1[:tick], self.sma2[:tick]):
            self.buy()

        # sell all, if flow passes fast
        elif crossover(self.sma2[:tick], self.sma1[:tick]):
            self.sell()

        # do nothing
        else:
            pass
