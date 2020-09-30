import numpy as np
import pandas as pd


class Analysis(object):
    @staticmethod
    def time_corr(factor, ret):
        # a = pd.DataFrame(factor).corrwith(pd.Series(ret), method='spearman')
        factor = np.argsort(np.argsort(factor))
        ret = np.argsort(np.argsort(ret))
        N = len(ret)
        ans = 1 - np.sum(np.square(factor - ret)) * 6 / (N * (N * N - 1))
        return ans
