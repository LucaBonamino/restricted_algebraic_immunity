from abc import ABC, abstractmethod

import pandas as pd

from sage.all import *

from restricted_algebraic_immunity.boolean_functions.boolean_hypercube import Slices
from restricted_algebraic_immunity.entities.enums import ReturnType
from restricted_algebraic_immunity.utils.utils_no_sage import partition


class CustomBooleanFunction(ABC):

    def __init__(self, slices):
        self.slices = slices

    def tt_by_slices(self, tt):
        return {sl.k: [v for idx, v in enumerate(tt) if idx in sl.domain] for sl in self.slices.slices}

    @abstractmethod
    def evaluate(*args, **kwargs):
        pass

    @abstractmethod
    def construct_truth_table(*args, **kwargs):
        pass

    @abstractmethod
    def boolean_function(*args, **kwargs):
        pass

    @staticmethod
    def compute_ai(r_slice, truth_table, _verbose: bool = False, _hide: bool = True):
        s_image = r_slice.get_s_image(truth_table)
        return r_slice.immunity_k(s_image, _verbose=_verbose, _hide=_hide)

    @classmethod
    def immunity_k(cls, n, tt, return_type: ReturnType = None, _verbose: bool = False, _hide: bool = True):
        sls = Slices(n_variables=n)
        ai_ks, dts = zip(
            *[cls.compute_ai(r_slice=sl, truth_table=tt, _verbose=_verbose, _hide=_hide) for sl in sls.slices])
        if return_type == ReturnType.DATA_FRAME:
            return cls.convert_to_df(partition=sls.partition, immunity_list=ai_ks, dts=dts)
        else:
            return ai_ks

    @staticmethod
    def convert_to_df(partition, immunity_list, dts):
        return pd.DataFrame({
            "k": partition.keys(),
            "AIk": immunity_list,
            r"T(AIk))": dts
        })

    @classmethod
    def immunity_f_k(cls, f, n, return_type: ReturnType = None, _verbose: bool = False, _hide: bool = True):
        sls = Slices(n_variables=n)
        aik_s, dts = zip(*[sl.immunity_f_k(f=f, _verbose=_verbose, _hide=_hide) for sl in sls.slices])
        if return_type == ReturnType.DATA_FRAME:
            return cls.convert_to_df(partition=sls.partition, immunity_list=aik_s, dts=dts)
        else:
            return aik_s


    @staticmethod
    def is_wpb(t_table, n_vars):
        p = partition(n_vars)
        if t_table[0] == 1 or t_table[-1] == 0:
            return False, None
        sls = Slices(n_vars)
        for sl in sls.slices:
            if sl.k == 0 or sl.k == n_vars:
                continue
            print(n_vars, sl.k)
            b = binomial(n_vars, sl.k)
            it = len([t_table[item] for item in p[sl.k] if t_table[item] == 1])
            if it != b//2:
                return False, [t_table[item] for item in p[sl.k]]
        return True, None


