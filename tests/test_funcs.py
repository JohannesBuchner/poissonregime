import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_allclose

from hypothesis import example, given, assume, strategies as st
import hypothesis.extra.numpy

from poissonregime import significance_from_pvalue, pvalue_from_significance, uncertainties_rate, uncertainties_fraction

sigstrategy = st.floats(allow_nan=False, allow_infinity=False, min_value=-7, max_value=7)
probstrategy = st.floats(allow_nan=False, allow_infinity=False, min_value=0, max_value=1)
countstrategy = st.integers(min_value=0, max_value=100000000)

@given(st.one_of(sigstrategy, hypothesis.extra.numpy.arrays(np.float, shape=hypothesis.extra.numpy.array_shapes(), elements=sigstrategy)))
@example(0)
@example(-1)
@example(np.array([0.0, -1, +1]))
def test_sig(s):
	p = pvalue_from_significance(s)
	o = significance_from_pvalue(p)
	print(s, p, o)
	assert_allclose(o, s, atol=1e-5)

@given(st.one_of(probstrategy, hypothesis.extra.numpy.arrays(np.float, shape=hypothesis.extra.numpy.array_shapes(), elements=probstrategy)))
@example(0.1)
@example(0.5)
@example(np.array([0.5, 0.01, 0.99]))
def test_p(p):
	assume(np.all(p>0))
	assume(np.all(p<1))
	s = significance_from_pvalue(p)
	o = pvalue_from_significance(s)
	print(s, p, o)
	assert_allclose(o, p, atol=1e-5)

@given(st.one_of(countstrategy, hypothesis.extra.numpy.arrays(int, shape=hypothesis.extra.numpy.array_shapes(), elements=countstrategy)), probstrategy)
@example(1, 0.5)
@example(np.array([1]), 0.5)
def test_rate(k, q):
	assume(np.all(q>0))
	assume(np.all(q<1))
	frac = uncertainties_rate(k=k, q=q)
	assert np.all(frac>0)
	#if q > 0.8:
	#	assert frac >= k

@st.composite
def twoarraystrategy(draw):
	shape = draw(hypothesis.extra.numpy.array_shapes())
	k = draw(hypothesis.extra.numpy.arrays(int, shape=shape, elements=countstrategy))
	kmore = draw(hypothesis.extra.numpy.arrays(int, shape=shape, elements=countstrategy))
	q = draw(probstrategy)
	return (k, kmore, q)

@st.composite
def twointstrategy(draw):
	return draw(countstrategy), draw(countstrategy), draw(probstrategy)

@given(st.one_of(twointstrategy(), twoarraystrategy()))
#@given(twoarraystrategy())
@example((0, 0, 0.5))
def test_fraction(p):
	k, kmore, q = p
	n = k + kmore
	assume(np.all(q>0))
	assume(np.all(q<1))
	frac = uncertainties_fraction(k=k, q=q, n=n)
	assert np.all(frac>=0)
	assert np.all(frac<=1)


"""
    print("1 sigma quantiles:", pvalue_from_significance([0, -1, +1]))
    print("1 sigma:", significance_from_pvalue(pvalue_from_significance([0, -1, +1])))
    print('rate for one of ten:', uncertainties_fraction(1, 10))
    print('rate for three events:', uncertainties_rate(3))
    print('rate for no events:', uncertainties_rate(0))
    print('significance of five events when 0.01 expected:', significance(5, 10, 0.01, k=-1), significance(5, 10, 0.01), significance(5, 10, 0.01, k=0.1))
"""
