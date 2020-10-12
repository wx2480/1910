import pandas as pd
from typing import Iterator


# load data
# 需要搞一个分chunks读取的和数据处理的函数，静态方法，方便调用
# 可以直接从gzip文件中读取，改一下需要
class Data(object):
    def __init__(self, path: str = 'E:\\fintech\\data\\'):
        self._path = path
        self._trade = {}
        self._ob = {}
        self.filename = ''

    def read(self, nrows: int, name: str, time: int):
        self.filename = str(name) + '.' + str(time)

        data = pd.read_csv(self._path + name + '.' + time, nrows=nrows, header=None, low_memory=False)
        self._ob[str(name) + '.' + str(time)] = self.data_extract(data, kind='ob')
        self._trade[str(name) + '.' + str(time)] = self.data_extract(data, kind='trade')

    def chunk_read(self, nrows: int, name: str, time: int) -> Iterator:
        data = pd.read_csv(self._path + name + '.' + time,
                           usecols=[i for i in range(95)],
                           chunksize=nrows,
                           header=None,
                           low_memory=False)
        return data

    @staticmethod
    def data_extract(data: pd.DataFrame, kind: str):
        _data = data.copy()
        if kind == 'ob':
            _data = _data[_data[0] == 'ob'].iloc[:, :84]
            ob_columns = ['kind', 'ts', 'recTs', 'pro']
            dtype = {}
            for i in ['a', 'b']:
                for j in range(1, 21):
                    ob_columns.append(i + 'p' + str(j))
                    ob_columns.append(i + 's' + str(j))
                    for k in ['p', 's']:
                        dtype[i + k + str(j)] = float
            _data.columns = ob_columns
            _data = _data.astype(dtype)
        elif kind == 'trade':
            _data = _data[_data[0] == 'trade'].dropna(axis=1).iloc[:, :8]
            trade_columns = ['kind', 'pro', 'ts', 'px', 'vol', 'dir', 'tid', 'recTs']
            _data.columns = trade_columns

            dtype = {'ts': str, 'px': float, 'vol': float, 'dir': str, 'recTs': str}
            _data = _data.astype(dtype)

        return _data

    def get_pro(self, kind: str, pro: str) -> pd.DataFrame:
        data = getattr(self, '_' + kind)[self.filename]
        data = data[data['pro'] == pro]
        return data
