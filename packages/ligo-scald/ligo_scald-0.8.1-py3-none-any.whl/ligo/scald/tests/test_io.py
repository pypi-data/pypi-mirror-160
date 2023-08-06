#!/usr/bin/env python

__author__ = "Patrick Godwin (patrick.godwin@ligo.org)"
__description__ = "a module that tests core I/O utilities"

#-------------------------------------------------
### imports

import sys
import pytest

import numpy

from ligo.scald.io import core


#-------------------------------------------------
### tests

class TestIOCore(object):
    """
    Tests several aspects of mock.py to check basic functionality.
    """
    def test_median(self):
        arr1 = numpy.arange(0, 100)
        median1 = core.median(arr1)
        assert median1 == 50, 'expected median: {}, got: {}'.format(50, median1)

        arr2 = numpy.arange(0, 101)
        median1 = core.median(arr2)
        assert median1 == 50, 'expected median: {}, got: {}'.format(50, median1)


    @pytest.mark.parametrize("agg, func", [('min', min), ('median', core.median), ('max', max)])
    def test_aggregate_to_func(self, agg, func):
        expected = core.aggregate_to_func(agg)
        assert expected == func


    @pytest.mark.parametrize("func, idx", [(min, 0), (core.median, 5), (max, 9)])
    def test_reduce_data(self, func, idx):
        xarr = numpy.arange(10)
        yarr = numpy.arange(10)
        reduced_idx, reduced_x, reduced_y = core.reduce_data(xarr, yarr, func, dt=10)
        reduced_idx = reduced_idx[0] # checking only single idx
        assert len(reduced_x) == 1, 'expected x length: {}, got: {}'.format(1, len(reduced_x))
        assert len(reduced_y) == 1, 'expected y length: {}, got: {}'.format(1, len(reduced_y))
        assert yarr[reduced_idx] == idx, 'expected aggregate: {}, got: {}'.format(idx, yarr[reduced_idx])
        assert reduced_idx == idx, 'expected aggregate idx: {}, got: {}'.format(idx, reduced_idx)
