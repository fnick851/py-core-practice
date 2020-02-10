import os.path as path
import pandas as pd


def assert_msg(condition, msg):
    if not condition:
        raise Exception(msg)


def read_file(filename):
    # absolute path
    filepath = path.join(path.dirname(__file__), filename)

    # assert file existence
    assert_msg(path.exists(filepath), "The file does not exist.")

    # read CSV file
    return pd.read_csv(filepath,
                       index_col=0,
                       parse_dates=True,
                       infer_datetime_format=True)


def SMA(values, n):
    """
    simple moving average
    """
    return pd.Series(values).rolling(n).mean()


def crossover(series1, series2) -> bool:
    """
    check if two series cross at the end
    :param series1:  series one
    :param series2:  series two
    :return:         True for crossed, False for not crossed
    """
    return series1[-2] < series2[-2] and series1[-1] > series2[-1]
