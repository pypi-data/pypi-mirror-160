import numpy as np

class gc:
    '''
    Exception handled:
    - If length of series is greater than 1
    - If mean of series is greater than 0
    '''
    def __init__(self, data_series):
        '''
        :param data_series: list or pandas series
        '''
        self.series_1 = np.array(data_series)

    def cov(self):
        try:
            if (len(self.series_1) > 1) & (np.mean(self.series_1) > 0):
                std_dev = np.std(self.series_1)
                data_mean = np.mean(self.series_1)
                cov2 = std_dev / data_mean
                return round((cov2)**2,3)
            else:
                return "please pass a series instead of single number or mean of series needs to be greater than zero"

        except:
            return "please pass a series instead of single number or mean of series needs to be greater than zero"


