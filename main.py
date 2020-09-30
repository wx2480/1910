from utils.data import Data
from utils.factorBase import FactorBase
from utils.analysis import Analysis
import datetime
import numpy as np
import pandas as pd


def to_datetime_ms(x, delay=0):
    return datetime.datetime.fromtimestamp((float(x) + delay) / 1000)


def EMA(x: pd.Series, beta: float = 0.9) -> float:
    ans = 0
    for i in x.values:
        ans = ans * (1 - beta) + i * beta
    return ans


def resample_factor(factor, delay=0, comp: str = 'mean') -> pd.Series:
    factor.recTs = factor.recTs.apply(to_datetime_ms, delay=delay)
    factor.set_index('recTs', inplace=True)
    return factor['factor'].resample('3s').mean()


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
    buy_c = FactorBase.order_concentrate(trade)

    data = ob
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

    mid_price.index = mid_price.index.map(to_datetime_ms)
    mid_price = mid_price.resample('3s').last()

    ret = -1 * np.log(mid_price).diff(-1)

    long_short_strength = resample_factor(long_short_strength, delay=0).resample('3s').last()
    up_vol = resample_factor(up_vol, delay=0).resample('3s').last()
    net_sell = resample_factor(net_sell, delay=0)
    buy_c = resample_factor(buy_c, delay=0).resample('3s').last()

    print('long_sort: ', Analysis.time_corr(long_short_strength.values, ret.values))
    print('up_vol: ', Analysis.time_corr(up_vol.values, np.abs(ret.values)))
    print('net_sell: ', Analysis.time_corr(net_sell.values, ret.values))
    print('buy_c: ', Analysis.time_corr(buy_c.values, np.abs(ret.values)))
