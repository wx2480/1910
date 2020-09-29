import numpy as np
import pandas as pd


class FactorBase(object):
    @staticmethod
    def rolling_window(a, window):
        shape = (a.shape[0] - window + 1, window, a.shape[1])
        strides = (a.strides[0], a.strides[1], a.strides[0], a.strides[1])
        return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

    @staticmethod
    def long_short_strength(_data):
        data = _data.copy()

        cols_bp, cols_bs, cols_ap, cols_as = [], [], [], []
        for i in range(1, 21):
            cols_bp.append('bp{}'.format(i))
            cols_bs.append('bs{}'.format(i))
            cols_ap.append('ap{}'.format(i))
            cols_as.append('as{}'.format(i))

        buy_strength = (data[cols_bp].values * data[cols_bs].values).sum(axis=1)
        sell_strength = (data[cols_ap].values * data[cols_as].values).sum(axis=1)

        factor = np.log(buy_strength) / np.log(sell_strength) - 1
        factor = pd.Series(factor, index=data.index, name='factor')
        factor = pd.concat([factor, data[['ts', 'recTs']]], axis=1)
        factor.reset_index(inplace=True, drop=True)

        return factor

    @staticmethod
    def up_vol(_data, window=200):
        def f(ret):
            mean = ret.mean()
            a = np.sum(np.square(ret[ret > mean] - mean)) / len(ret)
            return a / np.std(ret)

        data = _data.copy()
        cols_bp, cols_bs, cols_ap, cols_as = [], [], [], []
        for i in range(1, 21):
            cols_bp.append('bp{}'.format(i))
            cols_bs.append('bs{}'.format(i))
            cols_ap.append('ap{}'.format(i))
            cols_as.append('as{}'.format(i))

        buy_strength = (data[cols_bp].values * data[cols_bs].values).sum(axis=1)
        sell_strength = (data[cols_ap].values * data[cols_as].values).sum(axis=1)

        mid_price = (data['ap1'].values - data['bp1'].values) * (buy_strength /
                                                                 (buy_strength + sell_strength)) + data['ap1'].values
        mid_price = pd.Series(mid_price, index=data.index)
        mid_price_ret = np.log(mid_price).diff()
        factor = mid_price_ret.rolling(window=window).apply(f, raw=True)

        factor = pd.Series(factor, index=data.index, name='factor')
        factor = pd.concat([factor, data[['ts', 'recTs']]], axis=1)
        factor.reset_index(inplace=True, drop=True)

        return factor

    @staticmethod
    def net_sell(_data):
        data = _data.copy()

        data.loc[:, 'dir0'] = data.loc[:, 'dir'].apply(lambda x: 1 if x == 'BUY' else -1)
        factor = data.loc[:, 'px'].values * data.loc[:, 'vol'].values * data.loc[:, 'dir0'].values

        factor = pd.Series(factor, index=data.index, name='factor')
        factor = pd.concat([factor, data[['ts', 'recTs']]], axis=1)
        factor.reset_index(inplace=True, drop=True)

        return factor

    @staticmethod
    def buy_concentrate(_data, window=200):
        def f(vol):
            return np.sum(np.square(vol))/np.square(np.sum(vol))
        data = _data.copy()
        data = data[data['dir'] == 'BUY']
        factor = data['vol'].rolling(window).apply(f, raw=True)

        factor = pd.Series(factor, index=data.index, name='factor')
        factor = pd.concat([factor, data[['ts', 'recTs']]], axis=1)
        factor.reset_index(inplace=True, drop=True)

        return factor
