
import wget

class datasets(object):

    def demo():
        '''demo is used to demonstrate typical examples about this class.'''
        demostr = '''
import clubear as cb
cb.datasets.get('mini_airline') # download mini-version Airline data (2008.csv)

cb.datasets.get('mini_airline_sql') # download mini-version Airline SQL file (2008.sql)

cb.datasets.get('mini_airline', 'D:/') # the location of the downloaded file can also be specified
'''
        print(demostr)

    def get(target, downpath='.'):
        if target == None: print('datasets: The dataset name is needed.'); return
        if not isinstance(target,str): print('datasets: The dataset name must be a str.'); return

        if target == 'mini_airline':
            url = 'https://github.com/rockfc196/clubearTest/raw/master/2008.csv.zip'
        elif target == 'mini_airline_sql':
            url = 'https://github.com/rockfc196/clubearTest/raw/master/2008.sql.zip'

        location = wget.download(url, downpath)
        print('\n', target, 'downloading finished! The file location is :', location)
