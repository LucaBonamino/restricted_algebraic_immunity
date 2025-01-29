from sage.all import *
from sage.crypto.boolean_function import BooleanFunction

from restricted_algebraic_immunity.boolean_functions.boolean_function import CustomBooleanFunction


class ZS23(CustomBooleanFunction):

    def __init__(self, n):
        slices = Slices(n_variables=n)
        super().__init__(slices)

    @classmethod
    def evaluate(cls, x, n, m):
        if m == 1:
            return x[0]
        f_m = SubZS23.evaluate(x, m)
        p = prod([(x[i] + x[2 ** (m - 1) + i] + 1) % 2 for i in range(2 ** (m - 1))])
        x = x[:2 ** (m - 1) + 1]
        return (f_m + cls.evaluate(x, n, m - 1) * p) % 2

    @classmethod
    def construct_truth_table(cls, n: Integer, m: Integer):
        tt = []
        for i in range(2 ** n):
            b_item = bin(i)[2:].zfill(n)[::-1]
            v = vector(GF(2), [Integer(item) for item in b_item])
            tt.append(cls.evaluate(v, n, m))
        return tt

    @classmethod
    def boolean_function(cls, n: Integer, m: Integer):
        tt = cls.construct_truth_table(n=n, m=m)
        return BooleanFunction(tt)


class SubZS23(CustomBooleanFunction):

    @staticmethod
    def evaluate(x: vector, m: Integer):
        if m == 1:
            return x[0]
        mon_1 = 2 ** (m - 1)
        mon_2 = 2 ** (m - 2)
        p_1 = sum(x[:mon_1])
        p_2 = vector(GF(2), [x[i] * x[i + mon_2] for i in range(mon_1)])
        return p_1 + sum(p_2)

    @classmethod
    def construct_truth_table(cls, n: Integer, m: Integer):
        tt = []
        for i in range(2 ** n):
            b_item = bin(i)[2:].zfill(n)[::-1]
            v = vector(GF(2), [Integer(item) for item in b_item])
            tt.append(cls.evaluate(v, m))
        return tt

    @classmethod
    def boolean_function(cls, n: Integer, m: Integer):
        tt = cls.construct_truth_table(n=n, m=m)
        return BooleanFunction(tt)
