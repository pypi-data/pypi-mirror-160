import statistics, numpy as np


class gc:
    def __init__(self, data_series):
        '''
        :param data_series: list or pandas series
        '''
        self.series_1 = data_series

    def cov(self):
        if len(self.series_1) > 0:
            std_dev = statistics.stdev(self.series_1)
            std_dev = round(std_dev, 2)
            data_mean = statistics.mean(self.series_1)
            cov2 = std_dev / data_mean
            return round(cov2,3)**2
        else:
            return "please pass a series instead of single number"
