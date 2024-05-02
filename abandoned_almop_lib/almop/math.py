"""
This library is a collection of functions for compute-unit-agnostic functions that perform mathematical operations. The standard assumed here is that `xp` is the name representing the mathematical library alias. It stands for `np` (`numpy`, CPU-based calculations) or `cp` (`cupy`, GPU-based calculations).
"""

import cupy as cp 
from cupyx.scipy import stats
from scipy import stats 

def zscore(a):
    xp = cp.get_array_module(a)
    return stats.zscore(a)