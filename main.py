from utils.data import Data
from utils.factorBase import FactorBase
from utils.analysis import Analysis
from utils.operations import Tool
import numpy as np
import pandas as pd

if __name__ == '__main__':
    # 种类: BINANCE_PERPETUALFWD_BTC_USDT
    # filename: data.market.v2.BTC.log.20200825

    A = Data()
    d = A.chunk_read(nrows=1000000, name='data.market.v2.BTC.log', time='20200825')

    ans = {}
    ans['long_short'] = []
    ans['up_vol'] = []
    ans['net_sell'] = []
    ans['buy_c'] = []

    for i in d:
        # load data
        trade = Data.data_extract(i, kind='trade')
        ob = Data.data_extract(i, kind='ob')
        # trade = A._trade['data.market.v2.BTC.log.20200825']
        # ob = A._ob['data.market.v2.BTC.log.20200825']
        trade = trade[trade['pro'] == 'BINANCE_PERPETUALFWD_BTC_USDT']
        ob = ob[ob['pro'] == 'BINANCE_PERPETUALFWD_BTC_USDT']

        # Calculation factors
        long_short_strength = FactorBase.long_short_strength(ob)
        up_vol = FactorBase.up_vol(ob)
        net_sell = FactorBase.net_sell(trade)
        buy_c = FactorBase.order_concentrate(trade)

        # Calculate the rate of return
        ret = Tool.mid_price_ret(ob)

        # Processing factors
        long_short_strength = Tool.resample_factor(long_short_strength, delay=200)
        up_vol = Tool.resample_factor(up_vol, delay=200)
        net_sell = Tool.resample_factor(net_sell, delay=200)
        buy_c = Tool.resample_factor(buy_c, delay=200)

        # Output to screen
        ans['long_short'].append(Analysis.time_corr(long_short_strength, ret))
        ans['up_vol'].append(Analysis.time_corr(up_vol, np.abs(ret)))
        ans['net_sell'].append(Analysis.time_corr(net_sell, ret))
        ans['buy_c'].append(Analysis.time_corr(buy_c, np.abs(ret)))
        print('long_sort: ', Analysis.time_corr(long_short_strength, ret))
        print('up_vol: ', Analysis.time_corr(up_vol, np.abs(ret)))
        print('net_sell: ', Analysis.time_corr(net_sell, ret))
        print('buy_c: ', Analysis.time_corr(buy_c, np.abs(ret)))
        print('')

    pd.DataFrame(ans).to_csv('corr.csv')
