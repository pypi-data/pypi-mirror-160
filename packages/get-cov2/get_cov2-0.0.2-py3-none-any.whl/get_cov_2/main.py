import statistics, numpy as np


class get_cov:
    def __init__(self, data_series):
        self.series_1 = data_series

    def cov(self):
        std_dev = statistics.stdev(self.series_1)
        std_dev = round(std_dev, 2)
        data_mean = statistics.mean(self.series_1)
        cov2 = std_dev / data_mean
        return round(cov2,3)**2
