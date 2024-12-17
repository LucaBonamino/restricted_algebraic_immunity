import unittest

from sage.all import *
from sage.rings.integer import Integer

from sage.crypto.boolean_function import BooleanFunction
import random

from restricted_algebraic_immunity.full_reed_muller.FRM import FRMRestrictedAI
from restricted_algebraic_immunity.inductive_reed_muller.IV import IVRestrictedAI


def partition(n):
    """
    Compute the partition of range(2^n) in slices of integers according to their hamming weight.

    For instance,
      > partition(4)
      {0: [0], 1: [1, 2, 4, 8], 2: [3, 5, 6, 9, 10, 12], 3: [7, 11, 13, 14], 4: [15]}


    Args:
        n (int): number of variables

    Returns:
        dict: dictionary P such that P[k] is the set of numbers x in range(2^n) such that hw(x)=k
    """
    P = {}
    for i in range(n + Integer(1)): P[i] = []
    for d in range(Integer(2) ** n): P[bin(d).count("1")].append(d)
    return P


class TestRestrictedEfficientImmunityExtensive(unittest.TestCase):

    def test_restricted_with_pre_computation(self):
        v = [Integer(0), Integer(1), Integer(0), Integer(0)]
        f = BooleanFunction(v)
        s = [Integer(0), Integer(2)]

        immunity_obj = FRMRestrictedAI()
        res = immunity_obj.algebraic_immunity(f=f, s=s)
        self.assertEqual(res, 0)
        r = IVRestrictedAI.algebraic_immunity(f, s)
        self.assertEqual(res, r)

    def test_full_random(self):
        immunity_obj = FRMRestrictedAI()

        max_n = 10
        for _ in range(1000):
            n_var = random.choice(range(1, max_n))
            p = partition(n=Integer(n_var))
            v = [Integer(random.randint(0, 1)) for _ in range(2 ** Integer(n_var))]
            f = BooleanFunction(v)
            for k in p:
                ai_k_n = immunity_obj.algebraic_immunity(f=f, s=p[k])
                r = IVRestrictedAI.algebraic_immunity(v, p[k])
                if ai_k_n != r:
                    print(ai_k_n, r)
                    print(f.truth_table())
                    print(p[k])
                    print(k)
                self.assertEqual(ai_k_n, r)

    def test_full_random_v_dist(self):
        immunity_obj = AlgebraicImmunityRestrictedSet()

        max_n = 10
        for _ in range(1000):
            n_var = random.choice(range(1, max_n))
            p = partition(n=Integer(n_var))
            v = [Integer(random.randint(0, 1)) for _ in range(2 ** Integer(n_var))]
            f = BooleanFunction(v)
            for k in p:
                ai_k = AIk(k=k, f=f)
                ai_k_n = immunity_obj.find_immunity_full_precomputation(f=f, s=p[k])
                s_image = [v[i] for i in p[k]]
                r = EfficientAIRestrictedSet.algebraic_immunity_dist(s_image=s_image, s=p[k], n_var=n_var)
                if ai_k_n != r:
                    print(ai_k_n, r)
                    print(f.truth_table())
                    print(p[k])
                    print(k)
                self.assertEqual(ai_k_n, r)
                self.assertEqual(ai_k, ai_k_n)

    def test_full_random_unbalanced(self):
        immunity_obj = AlgebraicImmunityRestrictedSet()

        max_n = 10
        for _ in range(1000):
            n_var = random.choice(range(1, max_n))
            p = partition(n=Integer(n_var))
            f = BooleanFunction([Integer(random.randint(0, 1)) for _ in range(2 ** Integer(n_var))])
            for k in p:
                ai_k = AIk(k=k, f=f)
                ai_k_n = immunity_obj.algebraic_immunity(f=f, s=p[k])
                r = EfficientAIRestrictedSet.algebraic_immunity(f, p[k], balance_ratio=1)
                if ai_k_n != r:
                    print(ai_k_n, r)
                    print(f.truth_table())
                    print(p[k])
                    print(k)
                self.assertEqual(ai_k_n, r)
                self.assertEqual(ai_k, ai_k_n)

    def test_full_random_less_n(self):
        immunity_obj = FRMRestrictedAI()

        max_n = 4
        for _ in range(1000):
            n_var = random.choice(range(1, max_n))
            p = partition(n=Integer(n_var))
            f = BooleanFunction([Integer(random.randint(0, 1)) for _ in range(2 ** Integer(n_var))])
            for k in p:
                ai_k_n = immunity_obj.find_immunity_full_precomputation(f=f, s=p[k])
                r = IVRestrictedAI.algebraic_immunity(f, p[k])
                self.assertEqual(ai_k_n, r)


    def test_failing_7(self):
        tb = (True, False, True, True, True, False, True, True, False, False, False, True, True, True, False, True, True, False, False, False, False, True, False, True, False, False, True, True, False, True, True, True, True, False, True, False, True, False, False, True, False, True, True, False, False, True, False, True, False, False, True, False, False, False, True, False, False, True, True, False, False, False, True, True, False, False, True, False, False, True, True, False, False, True, False, True, False, True, True, True, False, True, True, False, True, False, False, True, True, True, False, True, True, False, False, False, True, False, False, False, True, False, False, True, False, True, True, True, False, True, False, True, True, True, False, False, True, True, True, False, False, True, False, False, False, False, False, True, True, False, False, True, True, False, True, False, False, True, True, False, True, False, False, True, True, True, True, True, True, False, True, False, True, True, True, True, True, False, True, True, True, False, False, False, True, False, False, False, True, True, True, True, False, False, False, True, True, True, True, True, False, True, False, True, True, True, False, True, False, True, False, True, True, False, False, False, True, False, True, False, False, False, False, False, False, False, True, False, True, False, True, False, False, False, True, False, False, False, True, False, True, False, True, False, True, False, True, False, False, True, False, True, True, False, False, True, False, True, True, True, False, True, True, False, False, True, False, True, False, True, False, True, False, False, True, False)
        s = [7, 11, 13, 14, 19, 21, 22, 25, 26, 28, 35, 37, 38, 41, 42, 44, 49, 50, 52, 56, 67, 69, 70, 73, 74, 76, 81, 82, 84, 88, 97, 98, 100, 104, 112, 131, 133, 134, 137, 138, 140, 145, 146, 148, 152, 161, 162, 164, 168, 176, 193, 194, 196, 200, 208, 224]
        n = log(len(tb), 2)
        p = partition(n=Integer(n))
        ou = 0
        for k in p:
            if p[k] == s:
                ou = k

        f = BooleanFunction([int(item) for item in tb])
        r = IVRestrictedAI.algebraic_immunity(f, s)
        immunity_obj = FRMRestrictedAI()
        ai_k_n = immunity_obj.algebraic_immunity(f=f, s=s)
        print(r)
        self.assertEqual(ai_k_n, r)
