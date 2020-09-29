import numpy as np


class Analysis(object):
    @staticmethod
    def time_corr(factor, ret):
        factor = np.argsort(factor)
        ret = np.argsort(ret)
        N = len(ret)
        return 1 - np.sum(np.square(factor - ret)) * 6 / (N * (N - 1) * (N - 1))
