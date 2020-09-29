from utils.data import Data
from utils.factorBase import FactorBase
from utils.analysis import Analysis
import numpy as np
import pandas as pd

if __name__ == '__main__':
    # 种类: BINANCE_PERPETUALFWD_BTC_USDT
    # filename: data.market.v2.BTC.log.20200825

    A = Data()
    A.read(nrows=300000, name='data.market.v2.BTC.log', time='20200825')
    trade = A._trade['data.market.v2.BTC.log.20200825']
    ob = A._ob['data.market.v2.BTC.log.20200825']
    trade = trade[trade['pro'] == 'BINANCE_PERPETUALFWD_BTC_USDT']
    ob = ob[ob['pro'] == 'BINANCE_PERPETUALFWD_BTC_USDT']

    long_short_strength = FactorBase.long_short_strength(ob)
    up_vol = FactorBase.up_vol(ob)
    net_sell = FactorBase.net_sell(trade)
    buy_c = FactorBase.buy_concentrate(trade)

    data = ob
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
    ret = -1 * np.log(mid_price).diff(-200).shift(-2)
    print(Analysis.time_corr(long_short_strength['factor'].values, ret))
    print(Analysis.time_corr(up_vol['factor'].values, np.abs(ret)))
    # print(Analysis.time_corr(net_sell['factor'].values, ret))
    # print(Analysis.time_corr(buy_c['factor'].values, ret))

    # print(long_short_strength)
    # print(up_vol)

    # a = pd.read_csv(
    # r'E:\fintech\data\data.market.v2.BTC.log.20200825',
    # chunksize=20000,
    # header=None,
    # low_memory=False
    # )
