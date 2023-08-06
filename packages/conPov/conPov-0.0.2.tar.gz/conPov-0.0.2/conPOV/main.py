import numpy as np
from scipy.stats import rv_discrete


class ConPov:

    def __init__(self,a,n):
        '''
        :param a: is a list and sum of all elements should be equal to 1
        :param n: is a integer value
        '''
        self.series = a
        self.single_value = n

    def conpov(self):
        '''
        :return: Self convolution of discrete distribution
        '''
        n1 = self.single_value
        basis = [self.single_value]
        while n1 > 1:
            basis.append(int(n1 / 2))
            n1 = int(n1 / 2)
        basis.reverse()
        res = self.series
        basis.remove(1)
        for i in basis:
            res = np.convolve(res, res)
            if i % 2 == 1:
                res = np.convolve(res, self.series)
        res = np.array(res)
        x = np.array([idx for idx, val in enumerate(res) if val != 0])
        y = res[res != 0]

        y = y / y.sum()
        custm = rv_discrete(name='custom', values=[x, y])
        return custm.pmf(x)



