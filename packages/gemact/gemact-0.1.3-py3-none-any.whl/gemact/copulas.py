import numpy as np
from scipy.stats import multivariate_normal, norm, t, gamma, uniform, multivariate_t, logser
from . import helperfunctions as hf
import time # used for setting random number generator seed if None
from twiggy import quick_setup, log

quick_setup()
logger = log.name('copulas')

## Clayton
class ClaytonCopula:
    """
    Clayton copula.

    :param par: copula parameter.
    :type par: ``float``
    :param dim: copula dimension.
    :type dim: ``int``
    """

    def __init__(self, par, dim):
        self.par = par
        self.dim = dim

    @property
    def par(self):
        return self.__par

    @par.setter
    def par(self, value):
        if value < 0:
            raise ValueError('Input "par" must be non-negative')
        self.__par = value

    @property
    def dim(self):
        return self.__dim

    @dim.setter
    def dim(self, value):
        self.__dim = value

    def cdf(self, x):
        """
        Cumulative distribution function.

        :param x: Array with shape (N, d) where N is the number of points and d the dimension.
        :type x: ``numpy.ndarray``
        :return: Cumulative distribution function in x.
        :rtype: ``numpy.ndarray``
        """
        assert x.shape[1] == self.dim, 'x dimension is not equal to copula dimension.'

        if len(x.shape) == 1:
            if (x <= 0).any():
                return 0
            else:
                return (np.sum(np.minimum(x, 1) ** (-self.par) - 1) + 1) ** -(1 / self.par)
        
        N = len(x)
        output = np.array([0.] * N)
        index = ~np.array(x <= 0).any(axis=1)
        output[index] = (np.sum(np.minimum(x[index, :], 1) ** (-self.par) - 1, axis=1) + 1) ** (-1 / self.par)
        return output
    
    def rvs(self, size=1, random_state=None):
        """
        Random variates.

        :param size: random variates sample size (default is 1).
        :type size: ``int``
        :param random_state: random state for the random number generator.
        :type random_state: ``int``

        :return: Random variates.
        :rtype: ``numpy.float64`` or ``numpy.ndarray``        
        """
        random_state = int(time.time()) if random_state is None else random_state
        assert isinstance(random_state, int), logger.error("random_state has to be an integer")

        try:
            size=int(size)
        except:
            logger.error('Please provide size as an integer')

        gamma_simul = gamma.rvs(1/self.par, size=[size, 1], random_state=random_state)
        exp_simul = gamma.rvs(1, size=[size, self.dim], random_state=random_state+2)
        output = (1 + exp_simul/gamma_simul)**(-1/self.par)
        return(output)
    
## Frank
class FrankCopula:
    """
    Frank copula.

    :param par: copula parameter.
    :type par: ``float``
    :param dim: copula dimension.
    :type dim: ``int``
    """

    def __init__(self, par, dim):
        self.par = par
        self.dim = dim

    @property
    def par(self):
        return self.__par

    @par.setter
    def par(self, value):
        if value < 0:
            raise ValueError('The input "par" must be non-negative')
        self.__par = value

    @property
    def dim(self):
        return self.__dim

    @dim.setter
    def dim(self, value):
        assert isinstance(value, int), logger.error('"dim" has to be an integer')
        self.__dim = value

    def cdf(self, x):
        """
        Cumulative distribution function.

        :param x: Array with shape (N, d) where N is the number of points and d the dimension.
        :type x: ``numpy.ndarray``
        :return: Cumulative distribution function in x.
        :rtype: ``numpy.ndarray``
        """
        assert x.shape[1] == self.dim, 'x dimension is not equal to copula dimension.'

        if len(x.shape) == 1:
            if (x <= 0).any():
                return 0
            else:
                d = len(x)
                return -1 / self.par * np.log(
                    1 + np.prod(np.exp(-self.par * np.minimum(x, 1)) - 1) / (np.exp(-self.par) - 1) ** (d - 1))
        N = len(x)
        d = len(x[0])
        output = np.array([0.] * N)
        index = ~np.array(x <= 0).any(axis=1)
        output[index] = -1 / self.par * np.log(
            1 + np.prod(np.exp(-self.par * np.minimum(x[index, :], 1)) - 1, axis=1) / (np.exp(-self.par) - 1) ** (d - 1))
        return output
    
    def rvs(self, size=1, random_state=None):
        """
        Random variates.

        :param size: random variates sample size (default is 1).
        :type size: ``int``
        :param random_state: random state for the random number generator.
        :type random_state: ``int``

        :return: Random variates.
        :rtype: ``numpy.float64`` or ``numpy.ndarray``        
        """
        random_state = int(time.time()) if random_state is None else random_state
        assert isinstance(random_state, int), logger.error("random_state has to be an integer")

        try:
            size=int(size)
        except:
            logger.error('Please provide size as an integer')

        logarithmic_simul = logser.rvs(1-np.exp(-self.par), size=[size, 1], random_state=random_state)
        exp_simul = gamma.rvs(1, size=[size, self.dim], random_state=random_state)
        output = -1/self.par * np.log(1 + np.exp(-exp_simul/logarithmic_simul)*(np.exp(-self.par) - 1))
        return(output)

## Gumbel
class GumbelCopula:
    """
    Gumbel copula.

    :param par: copula parameter.
    :type par: ``float``
    :param dim: copula dimension.
    :type dim: ``int``
    """

    def __init__(self, par, dim):
        self.par = par
        self.dim = dim

    @property
    def par(self):
        return self.__par

    @par.setter
    def par(self, value):
        if value < 0:
            raise ValueError("The input 'par' must be non-negative")
        self.__par = value

    @property
    def dim(self):
        return self.__dim

    @dim.setter
    def dim(self, value):
        assert isinstance(value, int), logger.error('"dim" has to be an integer')
        self.__dim = value

    def cdf(self, x):
        """
        Cumulative distribution function.

        :param x: Array with shape (N, d) where N is the number of points and d the dimension.
        :type x: ``numpy.ndarray``
        :return: Cumulative distribution function in x.
        :rtype: ``numpy.ndarray``
        """
        assert x.shape[1] == self.dim, 'x dimension is not equal to copula dimension.'

        if len(x.shape) == 1:
            if (x <= 0).any():
                return 0
            else:
                return np.exp(-np.sum((-np.log(np.minimum(x, 1))) ** self.par) ** (1 / self.par))

        output = np.array([0.] * x.shape[0])
        index = ~np.array(x <= 0).any(axis=1)
        output[index] = np.exp(-np.sum((-np.log(np.minimum(x[index, :], 1))) ** self.par, axis=1) ** (1 / self.par))
        return output

    def rvs(self, size=1, random_state=None):
        """
        Random variates.

        :param size: random variates sample size (default is 1).
        :type size: ``int``
        :param random_state: random state for the random number generator.
        :type random_state: ``int``

        :return: Random variates.
        :rtype: ``numpy.float64`` or ``numpy.ndarray``        
        """
        random_state = int(time.time()) if random_state is None else random_state
        assert isinstance(random_state, int), logger.error("random_state has to be an integer")

        try:
            size=int(size)
        except:
            logger.error('Please provide size as an integer')

        a_ = 1/self.par
        unif_simul = (uniform.rvs(size=[size, 1], random_state=random_state)-0.5)*np.pi
        exp_simul = gamma.rvs(1, size=[size, 1], random_state=random_state)        
        stable_simul = np.sin(a_*(np.pi/2 + unif_simul))/\
            np.cos(unif_simul)**(1/a_) *\
                (np.cos(unif_simul - a_*(np.pi/2 + unif_simul))/exp_simul)**((1 - a_)/a_)
        exp_simul = gamma.rvs(1, size=[size, self.dim], random_state=random_state+2)
        output = np.exp(-(exp_simul/stable_simul)**(1/self.par))
        return(output)

## Gaussian
class GaussCopula:
    """
    Gaussian copula.
    :param corr: Correlation matrix.
    :type corr: ``numpy.ndarray``
    """

    def __init__(self, corr):
        self.corr = corr

    @property
    def corr(self):
        return self.__corr

    @corr.setter
    def corr(self, value):
        if not isinstance(value, np.ndarray):
            raise ValueError('the correlation matrix needs to be a numpy array')
        if not np.allclose(value, np.transpose(value)):
            raise ValueError('the correlation matrix must be a symmetric square matrix')
        if not np.allclose(np.diagonal(value), np.ones(value.shape[0])):
            raise ValueError('%r is not a correlation matrix' % value)
        self.__corr = value

    @property
    def dim(self):
        return self.corr.shape[0]

    def cdf(self, x):
        """
        Cumulative distribution function.

        :param x: Array with shape (N, d) where N is the number of points and d the dimension.
        :type x: ``numpy.ndarray``
        :return: Cumulative distribution function in x.
        :rtype: ``numpy.ndarray``
        """
        return multivariate_normal.cdf(norm.ppf(x), cov=self.corr)
        
    def rvs(self, size=1, random_state=None):
        """
        Random variates.

        :param size: random variates sample size (default is 1).
        :type size: ``int``
        :param random_state: random state for the random number generator.
        :type random_state: ``int``

        :return: Random variates.
        :rtype: ``numpy.float64`` or ``numpy.ndarray``        
        """
        random_state = int(time.time()) if random_state is None else random_state
        assert isinstance(random_state, int), logger.error("random_state has to be an integer")

        try:
            size=int(size)
        except:
            logger.error('Please provide size as an integer')

        simul = multivariate_normal.rvs(
            mean=np.zeros(self.dim),
            cov=self.corr,
            size=size,
            random_state=random_state
            )
        return(norm.cdf(simul))

## TCopula
class TCopula:
    """
    T-Student copula.
    
    :param corr: Correlation matrix.
    :type corr: ``numpy.ndarray``
    :param df: Degree of freedom.
    :type df: ``int``
    """

    def __init__(self, corr, df):
        self.corr = corr
        self.df = df
        self.__error_cdf = None

    @property
    def dim(self):
        return self.corr.shape[0]

    @property
    def corr(self):
        return self.__corr

    @corr.setter
    def corr(self, value):
        if not isinstance(value, np.ndarray):
            raise ValueError('the correlation matrix needs to be a numpy array')
        if not np.allclose(value, np.transpose(value)):
            raise ValueError("the correlation matrix must be a symmetric square matrix")
        if not np.allclose(np.diagonal(value), np.ones(value.shape[0])):
            raise ValueError('%r is not a correlation matrix' % value)
        self.__corr = value
    
    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, value):
        assert isinstance(value, int), logger.error('"df" has to be an integer')
        self.__df = value

    @property
    def error_cdf(self):
        return self.__error_cdf

    def cdf(self, x, tolerance=1e-4, max_evaluations=1e+6, n_repetitions=30):
        q = t(self.df).ppf(x)
        (prob, err) = hf.multivariate_t_cdf(q, self.corr, self.df, tolerance, max_evaluations, n_repetitions)
        self.__error_cdf = err
        return prob
    
    def rvs(self, size=1, random_state=None):
        """
        Random variates.

        :param size: random variates sample size (default is 1).
        :type size: ``int``
        :param random_state: random state for the random number generator.
        :type random_state: ``int``

        :return: Random variates.
        :rtype: ``numpy.float64`` or ``numpy.ndarray``        
        """
        random_state = int(time.time()) if random_state is None else random_state
        assert isinstance(random_state, int), logger.error("random_state has to be an integer")

        try:
            size = int(size)
        except:
            logger.error('Please provide size as an integer')

        simul = multivariate_t.rvs(
            df=self.df,
            shape=self.corr,
            size=size,
            random_state=random_state
            )
        return(t.cdf(simul, df=self.df))    
