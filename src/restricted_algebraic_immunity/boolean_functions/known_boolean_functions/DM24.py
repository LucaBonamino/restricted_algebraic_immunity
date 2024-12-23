import pandas as pd
from sage.all import *
from sage.crypto.boolean_function import BooleanFunction
from typing import List
import random

from sage.rings.finite_rings.all import GF

from restricted_algebraic_immunity.boolean_functions.boolean_function import CustomBooleanFunction
from restricted_algebraic_immunity.boolean_functions.boolean_hypercube import Slices
from restricted_algebraic_immunity.entities.enums import ReturnType


class DM24(CustomBooleanFunction):

    def __init__(self, u, v, n):
        self.u = u
        self.v = v
        self.n = n
        slices = Slices(n_variables=n)
        super().__init__(slices)

    @staticmethod
    def sample_random_subset(number_or_variables, sample_size):
        for _ in range(sample_size):
            yield [random.randint(0, 1) for _ in range(2 ** number_or_variables)]

    @staticmethod
    def process_dataframe(df, counts, total_counts):
        for _, row in df.iterrows():
            k = row['k']
            AI_k = row['AIk']
            counts[k][AI_k] += 1
            total_counts[k] += 1
        return counts, total_counts

    @classmethod
    def aik_by_sample(cls, sample_size: int, n_vars: int):
        df = pd.DataFrame
        r = n_vars // 2
        # for sub_fb in DM24.sample_random_subset(number_or_variables=n//2, sample_size=sample_size):

        probs = {k: {aik: 0 for aik in range(n_vars // 2 + 1)} for k in range(n_vars + 1)}

        for _ in range(sample_size):
            u = [random.randint(0, 1) for _ in range(2 ** r)]
            v = [random.randint(0, 1) for _ in range(2 ** r)]
            sub_boolean_u = BooleanFunction(u)
            sub_boolean_v = BooleanFunction(v)
            dm24 = DM24(u=sub_boolean_u, v=sub_boolean_v, n=n_vars)
            bf = dm24.boolean_function()
            result_df = dm24.immunity_k(n=n_vars, tt=bf.truth_table(), return_type=ReturnType.DATA_FRAME)
            for _, row in result_df.iterrows():
                k = row['k']
                ai = row['AIk']
                probs[k][ai] += 1 / sample_size

            if df.empty:
                df = result_df
            else:
                df += result_df

        if df.empty:
            raise Exception("The DataFrame is empty. No data was processed.")

        macrostate_df = df / sample_size
        macrostate_df['k'] = macrostate_df['k'].astype(int)
        return macrostate_df, probs

    def boolean_function(self):
        tt = self.construct_truth_table()
        return BooleanFunction(tt)

    def tt_by_slices(self, tt):
        return {sl.k: [v for idx,v in enumerate(tt) if idx in sl.domain] for sl in self.slices.slices}


    def evaluate_wrapper(self, v):
        if v == 0:
            return 0
        elif v == 2 ** self.n - 1:
            return 1
        else:
            b_item = bin(v)[2:].zfill(self.n)[::-1]
            x = vector(GF(2), [Integer(item) for item in b_item])
            return DM24.evaluate(n=self.n, u=self.u, v=self.v, n_max=self.n // 2, x=x)

    def construct_truth_table(self):
        return [self.evaluate_wrapper(v=v) for v in range(2 ** self.n)]

    @staticmethod
    def extend_input(v: vector, n_max: Integer) -> List[Integer]:
        zeros_needed = n_max - len(v)
        return list(v) + list(vector(zeros_needed * [0]))

    @classmethod
    def evaluate2(cls, n: int, x: vector, u: BooleanFunction, v: BooleanFunction, n_max: int):
        if n % 2 != 0:
            if x[-1] == 0:
                return cls.evaluate(n=n - 1, x=x[:-1], u=u, v=v, n_max=n_max)
            else:
                return (cls.evaluate(n=n - 1, x=x[:-1], u=u, v=v, n_max=n_max) + 1) % 2
        else:
            x1 = x[:n // 2]
            x2 = x[n // 2:]
            k1 = sum(x1)
            k2 = sum(x2)

            if sum(x) % 2 != 0:
                if k1 % 2 != 0:
                    extended_v = cls.extend_input(n_max=n_max, v=x2)
                    return int(u(extended_v))
                else:
                    extended_v = cls.extend_input(n_max=n_max, v=x1)
                    return (1 + int(v(extended_v))) % 2
            else:
                if x1 == x2:
                    return cls.evaluate(n=n // 2, x=x1, u=u, v=v, n_max=n_max) \
                        if k1 % 2 == 0 else (1 + cls.evaluate(n=n // 2, x=x1, u=u, v=v, n_max=n_max)) % 2
                else:
                    i = 0
                    while i < len(x1) and x1[i] == x2[i]:
                        i += 1
                    if i == len(x1):
                        return 0
                    if k1 % 2 == 0:
                        if x1[i] > x2[i]:
                            extended_v = cls.extend_input(n_max=n_max, v=x2)
                            return int(v(extended_v))
                        else:
                            extended_v = cls.extend_input(n_max=n_max, v=x1)
                            return int(v(extended_v))
                    else:
                        return 1 if x1[i] > x2[i] else 0

    @classmethod
    def evaluate(cls, n: int, x: vector, u: BooleanFunction, v: BooleanFunction, n_max: int):
        if n % 2 != 0:
            if x[-1] == 0:
                return cls.evaluate(n=n - 1, x=x[:-1], u=u, v=v, n_max=n_max)
            else:
                return (cls.evaluate(n=n - 1, x=x[:-1], u=u, v=v, n_max=n_max) + 1) % 2
        else:
            x1 = x[:n // 2]
            x2 = x[n // 2:]
            k1 = sum(x1)
            k2 = sum(x2)
            if sum(x) % 2 != 0:
                if k1 % 2 != 0:
                    extended_v = cls.extend_input(n_max=n_max, v=x2)
                    return Integer(u(extended_v))
                else:
                    extended_v = cls.extend_input(n_max=n_max, v=x1)
                    return (1 + Integer(v(extended_v))) % 2
            else:
                if x1 == x2:
                    return cls.evaluate(n=n // 2, x=x1, u=u, v=v, n_max=n_max) \
                        if k1 % 2 == 0 else (1 + cls.evaluate(n=n // 2, x=x1, u=u, v=v, n_max=n_max)) % 2
                else:
                    i = 0
                    while i < len(x1) and x[i] == x[i + n // 2]:
                        i += 1
                    if i == len(x1):  # Prevents index out of range
                        return 0
                    if k1 % 2 == 0:
                        if x[i] > x[n // 2 + i]:
                            extended_v = cls.extend_input(n_max=n_max, v=x2)
                            return v(extended_v)
                        else:
                            extended_v = cls.extend_input(n_max=n_max, v=x1)
                            v(extended_v)
                    else:
                        return 1 if x[i] > x[n // 2 + i] else 0

    #
    # @staticmethod
    # def save_latex_table(dataframe, n):
    #     plotter = PublishedFunctionsPlotter(function_family=FunctionFamilyType.DM24)
    #     file_name = f"table_n_{n}"
    #     m = log(n, 2)
    #     caption = fr"$AI_k$ of {FunctionFamilyType.DM24.value.label} for $m={m}$ $n=2^{{m}}={n}$"
    #     plotter.save_table_to_file(save_filename=file_name, dataframe=dataframe, caption=caption)
    #
    # @staticmethod
    # def save_latex_table_random(dataframe, n, sample_size):
    #     plotter = PublishedFunctionsPlotter(function_family=FunctionFamilyType.DM24)
    #     file_name = f"table_random_n_{n}_sample_size_{sample_size}"
    #     m = log(n, 2)
    #     caption = fr"$AI_k$ of {FunctionFamilyType.DM24.value.label} for $m={m}$ $n=2^{{m}}={n}$ and $\mbox{{sample\_size}} = {sample_size}$"
    #     plotter.save_table_to_file(save_filename=file_name, dataframe=dataframe, caption=caption)


class SubDM24(CustomBooleanFunction):

    @staticmethod
    def evaluate(x: vector, n: int) -> int:
        if n % 2 == 0:
            return (sum(x[i] * x[i + 1] for i in range(len(x) - 1))) % 2
        else:
            s = sum(x[i] * x[i + 1] for i in range(len(x) - 2))
            return (s + x[-1]) % 2

    @classmethod
    def construct_truth_table(cls, n: int) -> List:
        return [cls.evaluate(x=convert_number_to_bin_vector(v=idx, n=n), n=n) for idx in
                range(2 ** n)]

    @classmethod
    def boolean_function(cls, n: int) -> BooleanFunction:
        tt = cls.construct_truth_table(n=n)
        return BooleanFunction(tt)


def convert_number_to_bin_vector(v: int, n: int) -> vector:
    bin_v = bin(v)[2:].zfill(n)[::-1]
    return vector(GF(2), [Integer(item) for item in bin_v])
