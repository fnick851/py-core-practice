import numpy as np
import pandas as pd
from numbers import Number

from strategy import Strategy, SmaCross
from utils import read_file, assert_msg, crossover, SMA


class ExchangeAPI:
    def __init__(self, data, cash, commission):
        assert_msg(
            0 < cash, "Initial cash amount should be bigger than zero, the input is:：{}".format(cash))
        assert_msg(0 <= commission <= 0.05,
                   "A reasonbable process fee is typically lower than 5%, the input is: {}".format(commission))
        self._inital_cash = cash
        self._data = data
        self._commission = commission
        self._position = 0
        self._cash = cash
        self._i = 0

    @property
    def cash(self):
        """
        :return: return the current cash amount
        """
        return self._cash

    @property
    def position(self):
        """
        :return: recturn the current position
        """
        return self._position

    @property
    def initial_cash(self):
        """
        :return: return initial cash amount
        """
        return self._inital_cash

    @property
    def market_value(self):
        """
        :return: return current market value
        """
        return self._cash + self._position * self.current_price

    @property
    def current_price(self):
        """
        :return: return current market price
        """
        return self._data.Close[self._i]

    def buy(self):
        """
        spend all cash to buy in, with current market price
        """
        self._position = float(
            self._cash * (1 - self._commission) / self.current_price)
        self._cash = 0.0

    def sell(self):
        """
        sell all remaining stock
        """
        self._cash += float(self._position *
                            self.current_price * (1 - self._commission))
        self._position = 0.0

    def next(self, tick):
        self._i = tick


class Backtest:
    """
    Backtest: read historical data, execute strategy, simulate transaction and estimate gain/loss

    When initialized, call Backtest.run to backtest

    instance, or `backtesting.backtesting.Backtest.optimize` to
    optimize it.
    """

    def __init__(self,
                 data: pd.DataFrame,
                 strategy_type: type(Strategy),
                 broker_type: type(ExchangeAPI),
                 cash: float = 10000,
                 commission: float = .0):
        """
        Construct a backtest object.

        Parameters：
        :param data:            pd.DataFrame        OHLCV data in pandas Dataframe format
        :param broker_type:     type(ExchangeAPI)   API type of the exchange
        :param strategy_type:   type(Strategy)      Type of the strategy
        :param cash:            float               Initial cash amount
        :param commission:       float              Process fee amount percentage
        """

        assert_msg(issubclass(strategy_type, Strategy),
                   'strategy_type is not an instance of Strategy class')
        assert_msg(issubclass(broker_type, ExchangeAPI),
                   'strategy_type is not an instance of Strategy class')
        assert_msg(isinstance(commission, Number),
                   'commission is not an instance of float class')

        data = data.copy(False)

        if 'Volume' not in data:
            data['Volume'] = np.nan

        # validate OHLC
        assert_msg(len(data.columns & {'Open', 'High', 'Low', 'Close', 'Volume'}) == 5,
                   ("The input data is not in the correct format. It should at least include the following columns："
                    "'Open', 'High', 'Low', 'Close'"))

        # check for null values
        assert_msg(not data[['Open', 'High', 'Low', 'Close']].max().isnull().any(),
                   ('Part of OHLC data has null values, please remove or interpolate those. '))

        # sort based on time
        if not data.index.is_monotonic_increasing:
            data = data.sort_index()

        # initialize exchange and strategy
        self._data = data  # type: pd.DataFrame
        self._broker = broker_type(data, cash, commission)
        self._strategy = strategy_type(self._broker, self._data)
        self._results = None

    def run(self) -> pd.Series:
        """
        Run the backtest. Returns `pd.Series` with results and statistics.

        Keyword arguments are interpreted as strategy parameters.
        """
        strategy = self._strategy
        broker = self._broker

        strategy.init()

        # backtest start and end position
        start = 100
        end = len(self._data)

        # update market and execute strategy
        for i in range(start, end):
            # move the market status to `i`
            broker.next(i)
            strategy.next(i)

        self._results = self._compute_result(broker)
        return self._results

    def _compute_result(self, broker):
        s = pd.Series()
        s['initial market value'] = broker.initial_cash
        s['end market value'] = broker.market_value
        s['gain/loss'] = broker.market_value - broker.initial_cash
        return s


def main():
    BTCUSD = read_file('BTCUSD_GEMINI.csv')
    ret = Backtest(BTCUSD, SmaCross, ExchangeAPI, 10000.0, 0.003).run()
    print(ret)


if __name__ == '__main__':
    main()
