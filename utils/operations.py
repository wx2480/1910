import datetime
import numpy as np
import pandas as pd


class Tool(object):
    @staticmethod
    def to_datetime_ms(x, delay=0):
        return datetime.datetime.fromtimestamp((float(x) + delay) / 1000)

    @staticmethod
    def EMA(x: pd.Series, beta: float = 0.9) -> float:
        ans = 0
        for i in x.values:
            ans = ans * (1 - beta) + i * beta
        return ans

    @staticmethod
    def resample_factor(factor, delay=0, comp: str = 'mean') -> pd.Series:
        _factor = factor.copy()
        _factor.recTs = _factor.recTs.apply(Tool.to_datetime_ms, delay=delay)
        _factor.set_index('recTs', inplace=True)
        # return _factor['factor'].resample('3s').mean()
        return _factor['factor'].resample('3s').apply(Tool.EMA)

    @staticmethod
    def mid_price_ret(ob, interval='3s'):
        data = ob.copy()
        cols_bp, cols_bs, cols_ap, cols_as = [], [], [], []
        for i in range(1, 21):
            cols_bp.append('bp{}'.format(i))
            cols_bs.append('bs{}'.format(i))
            cols_ap.append('ap{}'.format(i))
            cols_as.append('as{}'.format(i))

        buy_strength = (data[cols_bp].values * data[cols_bs].values).sum(axis=1)
        sell_strength = (data[cols_ap].values * data[cols_as].values).sum(axis=1)

        # mid_price
        mid_price = (data['ap1'].values - data['bp1'].values) * (buy_strength /
                                                                 (buy_strength + sell_strength)) + data['ap1'].values
        mid_price = pd.Series(mid_price, index=data.recTs)

        mid_price.index = mid_price.index.map(Tool.to_datetime_ms)
        mid_price = mid_price.resample(interval).last()

        return -1 * np.log(mid_price).diff(-1)


class operations(object):
    @staticmethod
    def power(factors, beta):
        factors = np.power(factors, beta)
        return factors

    @staticmethod
    def truncate(factors, ratio, kind='mid'):
        if kind == 'mid':
            median = np.median(factors)
            rule = np.median(np.abs(factors - median))
            factors_up, factors_down = median + ratio * rule, median - ratio * rule
        elif kind == 'ratio':
            factors_max = np.max(factors)
            factors_min = np.min(factors)
            rule = (factors_max - factors_min) * ratio
            factors_up, factors_down = factors_max - rule, factors_min + rule
        else:
            print('param kind is not in [mid, ratio]')
            return None

        factors = factors[(factors > factors_down) & (factors < factors_up)]
        return factors

    @staticmethod
    def normalization(factors, rank=False):
        pass
