"""
poissonregime module.
"""

"""
MIT License

Copyright (c) 2021 Johannes Buchner
Copyright (c) 2016 Max Ahnen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__version__ = '0.5.1'

import scipy.special
import scipy.stats
import numpy as np

from gamma_limits_sensitivity import li_ma_significance

# This is the smallest number we can process within the numerical precision available
tiny = np.finfo(float).tiny

def significance_from_pvalue(pvalue):
    """
    Return the significance (i.e., the z-score) for a given probability, i.e., the number of standard deviations (sigma)
    corresponding to the probability

    :param pvalue: input probability
    :return: z-score (or significance in units of sigma)
    """

    # Make sure that we can compute this score (i.e., the pvalue is not too small)
    if np.any(pvalue <= tiny):
        raise ArithmeticError("One or more pvalues are too small for a significance computation.")

    # This is equivalent to sqrt(2) * erfinv(1 - 2 * pvalue) but faster
    return -scipy.special.ndtri(pvalue)

def pvalue_from_significance(zscore):
    """
    Return the probability for a given significance.

    :param pvalue: z-score (or significance in units of sigma)
    :return: probability
    """
    return scipy.special.ndtr(-np.asarray(zscore))

def significance(n, b, alpha, k=0):
    """
    Returns the significance for detecting n counts when alpha * b are expected.
    If sigma=0 and k=0 (default), this is the case with no additional systematic error and the classic result
    from Li & Ma (1983) is used. Example::

        significance(n, b, alpha)

    If k>0 then eq.7 from Vianello (2018) is used, which assumes that k is the upper boundary on the fractional
    systematic uncertainty. Example::
 
        significance(n, b, alpha, k=0.1)

    If k<0, then alpha * b is assumed to have no uncertainties.

    :param n: observed counts (can be an array)
    :param b: expected background counts (can be an array)
    :param alpha: ratio of the source observation efficiency and background observation efficiency
        (either a float, or an array of the same shape of n)
    :param k: maximum fractional systematic uncertainty expected (either a float, or an array of the same shape of n)
    :return: the significance (z score) for the measurement(s)
    """

    if k < 0:
        return significance_from_pvalue(scipy.stats.poisson.sf(n, alpha * b))

    sign = np.where(n >= alpha * b, 1, -1)
    return sign * li_ma_significance(n, b, alpha * (k + 1))

def posterior(rate, n, b, alpha, exposure=1.0):
    """
    Returns the posterior of a source count rate for detecting n counts when alpha * b are expected.

    :param rate: count rate (can be an array)
    :param n: observed counts (can be an array)
    :param b: expected background counts (can be an array)
    :param alpha: ratio of the source observation efficiency and background observation efficiency
    :param exposure: exposure time, area, volume, or similar to convert the rate to expected source counts.
        (either a float, or an array of the same shape of n)
    :return: the likelihood value
    """

    nexp = exposure * rate
    t_1 = 1 + b + n
    hb = 0.5 + b
    thb = 1.5 + b
    return scipy.stats.poisson.pmf(n + b, nexp) * scipy.special.hyperu(hb, t_1, (1 + 1. / alpha) * nexp) / scipy.special.hyp2f1(hb, t_1, thb, -1/alpha) * scipy.special.gamma(thb)
    #return sign * li_ma_significance(n, b, alpha * (k + 1))


def uncertainties_rate(k, q=pvalue_from_significance([0, -1, +1]), exposure=1.0):
    """
    Give error bars on the number of events, given k detections.

    :param k: number of hits, events, detections or sources.
    :param q: quantile(s) to consider. 0.5 is the median, use pvalue_from_significance to convert from sigma units.
    :param exposure: exposure time, area, volume, or similar to normalise to a rate.
    :return: error bars on the number of events. By default, the median, lower and upper 1 sigma estimates.

    Caveat: this assumes a uniform prior on the number of events.
    """
    assert isinstance(k, (int, np.integer)) or isinstance(k, np.ndarray) and k.dtype == int, "k must be integer"
    assert np.all(q > 0), "Quantile must be between zero and one."
    assert np.all(q < 1), "Quantile must be between zero and one."
    return scipy.special.gammainccinv(k + 1, q) / exposure


def uncertainties_fraction(k, n, q=pvalue_from_significance([0, -1, +1])):
    """
    Give error bars on a fraction, given k positives out of n possible.

    :param k: number of hits, events, detections or sources.
    :param n: number of opportunities, total sample size, time bins, slots.
    :param q: quantile(s) to consider. 0.5 is the median, use pvalue_from_significance to convert from sigma units.

    :return: error bars on the fraction. By default, the median, lower and upper 1 sigma estimates.

    See e.g., https://arxiv.org/abs/1012.0566
    """
    assert isinstance(k, (int, np.integer)) or isinstance(k, np.ndarray) and k.dtype == int, "k must be integer"
    assert isinstance(n, (int, np.integer)) or isinstance(n, np.ndarray) and n.dtype == int, "n must be integer"
    assert np.all(k<=n), "k must be smaller than n."
    assert np.all(q > 0), "Quantile must be between zero and one."
    assert np.all(q < 1), "Quantile must be between zero and one."
    return scipy.special.betaincinv(k + 1, n + 1 - k, q)


if __name__ == '__main__':
    print("1 sigma quantiles:", pvalue_from_significance([0, -1, +1]))
    print("1 sigma:", significance_from_pvalue(pvalue_from_significance([0, -1, +1])))
    print('rate for one of ten:', uncertainties_fraction(1, 10))
    print('rate for three events:', uncertainties_rate(3))
    print('rate for no events:', uncertainties_rate(0))
    print('significance of five events when 0.01 expected:', significance(5, 10, 0.01, k=-1), significance(5, 10, 0.01), significance(5, 10, 0.01, k=0.1))
    rate = np.linspace(0.01, 10, 40)
    print('likelihood:', np.vstack((rate, posterior(rate, 4, 0, 0.01))).transpose())
