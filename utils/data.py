import pandas as pd


# load data
class Data(object):
    def __init__(self, path='E:\\fintech\\data\\'):
        self._path = path
        self._trade = {}
        self._ob = {}
        self.filename = ''

    def read(self, nrows, name, time):
        self.filename = str(name) + '.' + str(time)

        data = pd.read_csv(self._path + name + '.' + time, nrows=nrows, header=None, low_memory=False)

        self._ob[str(name) + '.' + str(time)] = data[data[0] == 'ob'].iloc[:, :84]
        ob_columns = ['kind', 'ts', 'recTs', 'pro']
        dtype = {}
        for i in ['a', 'b']:
            for j in range(1, 21):
                ob_columns.append(i + 'p' + str(j))
                ob_columns.append(i + 's' + str(j))
                for k in ['p', 's']:
                    dtype[i + k + str(j)] = float
        self._ob[str(name) + '.' + str(time)].columns = ob_columns

        self._ob[str(name) + '.' + str(time)] = self._ob[str(name) + '.' + str(time)].astype(dtype)

        self._trade[str(name) + '.' + str(time)] = data[data[0] == 'trade'].dropna(axis=1).iloc[:, :8]
        trade_columns = ['kind', 'pro', 'ts', 'px', 'vol', 'dir', 'tid', 'recTs']
        self._trade[str(name) + '.' + str(time)].columns = trade_columns

        dtype = {'ts': int, 'px': float, 'vol': float, 'dir': str, 'recTs': int}
        self._trade[str(name) + '.' + str(time)] = self._trade[str(name) + '.' + str(time)].astype(dtype)

    def get_pro(self, kind, pro):
        data = getattr(self, '_' + kind)[self.filename]
        data = data[data['pro'] == pro]
        return data
