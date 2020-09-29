import numpy as np


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
