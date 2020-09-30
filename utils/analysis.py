import pandas as pd


class Analysis(object):
    @staticmethod
    def time_corr(factor: pd.Series, ret: pd.Series) -> float:
        ans = pd.DataFrame(factor).corrwith(ret, method='spearman')
        # factor = np.argsort(np.argsort(factor))
        # ret = np.argsort(np.argsort(ret))
        # N = len(ret)
        # ans = 1 - np.sum(np.square(factor - ret)) * 6 / (N * (N * N - 1))
        return ans.iloc[0]
