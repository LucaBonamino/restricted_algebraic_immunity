import unittest

from sage.all import *
from sage.rings.integer import Integer

from sage.crypto.boolean_function import BooleanFunction
import random

from restricted_algebraic_immunity.full_reed_muller.FRM import FRMRestrictedAI
from restricted_algebraic_immunity.inductive_reed_muller.IV import IVRestrictedAI

from WAPB.parsed_AIk import AIk


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
        immunity_obj = FRMRestrictedAI()

        max_n = 10
        for _ in range(1000):
            n_var = random.choice(range(1, max_n))
            p = partition(n=Integer(n_var))
            v = [Integer(random.randint(0, 1)) for _ in range(2 ** Integer(n_var))]
            f = BooleanFunction(v)
            for k in p:
                ai_k_n = immunity_obj.algebraic_immunity(f=f, s=p[k])
                s_image = [v[i] for i in p[k]]
                r = IVRestrictedAI.algebraic_immunity_dist(s_image=s_image, s=p[k], n_vars=n_var)
                if ai_k_n != r:
                    print(ai_k_n, r)
                    print(f.truth_table())
                    print(p[k])
                    print(k)
                self.assertEqual(ai_k_n, r)

    def test_full_random_v_dist_alg_1(self):
        immunity_obj = FRMRestrictedAI()

        max_n = 10
        for _ in range(1000):
            n_var = random.choice(range(1, max_n))
            p = partition(n=Integer(n_var))
            v = [Integer(random.randint(0, 1)) for _ in range(2 ** Integer(n_var))]
            f = BooleanFunction(v)
            for k in p:
                s_image = [v[i] for i in p[k]]
                ai_k_n = immunity_obj.algebraic_immunity_dist(s_image=s_image, s=p[k], n_vars=n_var)
                r = IVRestrictedAI.algebraic_immunity_dist(s_image=s_image, s=p[k], n_vars=n_var)
                if ai_k_n != r:
                    print(ai_k_n, r)
                    print(f.truth_table())
                    print(p[k])
                    print(k)
                self.assertEqual(ai_k_n, r)

    def test_full_random_unbalanced(self):
        immunity_obj = FRMRestrictedAI()

        max_n = 10
        for _ in range(1000):
            n_var = random.choice(range(1, max_n))
            p = partition(n=Integer(n_var))
            f = BooleanFunction([Integer(random.randint(0, 1)) for _ in range(2 ** Integer(n_var))])
            for k in p:
                ai_k = AIk(k=k, f=f)
                try:
                    ai_k_n = immunity_obj.algebraic_immunity(f=f, s=p[k])
                    r = IVRestrictedAI.algebraic_immunity(f, p[k], balance_ratio=1)
                except:
                    print(f.truth_table())
                    print(p[k])
                    raise Exception
                if ai_k_n != r:
                    print(ai_k_n, r)
                    print(f.truth_table())
                    print(p[k])
                    print(k)
                self.assertEqual(ai_k_n, r)
                self.assertEqual(ai_k, ai_k_n)

    def test_failing_unbalanced(self):
        tb = (True, False, False, True, True, False, True, True, True, False, False, False, False, False, True, True, True, True, False, True, True, False, True, False, True, True, False, True, False, False, True, False, False, False, False, False, True, False, True, False, False, False, False, True, False, False, False, True, True, True, True, False, False, True, True, True, False, False, True, True, True, True, False, False, True, True, False, False, True, False, True, False, False, False, False, True, False, True, True, True, False, True, False, True, False, False, False, False, False, True, True, False, True, False, True, True, True, False, True, True, False, False, False, True, False, True, True, True, True, True, False, False, True, False, False, False, True, False, True, True, True, False, True, True, False, True, True, True, True, False, True, True, False, False, True, False, True, True, False, True, True, False, True, True, True, True, True, False, False, False, False, False, True, True, False, True, True, False, False, True, True, False, False, False, True, False, False, False, True, True, True, False, False, False, True, False, True, False, False, False, False, True, True, False, False, True, False, False, True, True, False, False, True, False, True, True, False, False, True, True, True, False, True, True, True, False, True, False, False, True, True, True, True, False, True, True, True, True, False, False, True, True, True, True, False, True, True, False, True, True, False, False, True, True, False, True, False, False, False, True, False, False, True, True, False, False, True, False, False, True, False, True, False, False, True, False, True, True, False, True, False, True, True, True, True, False, True, False, False, False, True, True, True, True, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True, True, False, True, True, True, True, False, False, True, False, True, True, False, True, True, True, True, False, False, False, True, False, False, True, False, True, False, False, True, False, True, False, False, False, False, False, True, True, False, True, False, True, False, False, True, True, True, False, False, True, False, True, False, False, True, False, True, True, False, True, False, False, False, True, True, True, True, True, False, False, False, True, True, False, True, False, True, True, True, True, True, True, True, False, False, True, True, True, True, False, False, True, False, False, False, False, False, False, False, False, False, True, True, False, True, True, True, False, True, True, False, True, False, False, True, False, True, True, True, False, False, False, False, True, True, True, False, True, False, False, True, False, False, True, False, False, False, True, False, True, False, True, True, False, False, True, False, True, False, False, False, False, False, True, True, False, True, False, True, False, True, True, True, True, True, True, False, False, True, False, True, False, True, False, False, True, False, True, False, True, False, False, False, False, False, True, False, False, True, True, False, True, False, True, False, True, True, True, True, True, False, False, False, True, False, False, False, True, True, True, True, False, True, True, False, True, True, True, False, False, True, True, True)
        s = [3, 5, 6, 9, 10, 12, 17, 18, 20, 24, 33, 34, 36, 40, 48, 65, 66, 68, 72, 80, 96, 129, 130, 132, 136, 144, 160, 192, 257, 258, 260, 264, 272, 288, 320, 384]
        r = IVRestrictedAI.algebraic_immunity(BooleanFunction([int(item) for item in tb]), s, balance_ratio=1)

    def test_failing_unbalanced_2(self):
        tb = (False, True, False, True, False, False, True, False, False, False, False, False, True, True, False, False, False, False, False, False, False, True, False, True, True, False, False, False, True, True, False, True, False, False, False, False, True, True, True, False, False, True, True, True, False, False, False, False, False, True, False, False, True, True, True, True, False, True, True, True, True, False, False, False, True, False, True, False, True, False, False, False, True, True, True, False, True, False, True, False, True, False, False, False, True, False, True, False, False, True, False, False, True, False, True, True, False, True, False, False, True, False, False, True, True, True, True, False, False, False, False, True, False, True, False, True, True, False, True, False, True, False, True, True, False, False, False, True, False, True, True, True, True, True, False, True, False, False, True, False, False, True, False, True, False, False, True, False, False, False, True, False, True, True, False, True, True, True, True, True, True, True, False, True, True, True, False, False, False, True, False, True, True, False, True, False, False, False, False, True, True, True, True, True, False, True, True, False, True, True, True, True, True, False, True, False, True, True, True, True, True, False, False, True, False, False, True, True, False, False, False, False, False, True, False, True, False, False, True, True, False, False, True, True, True, False, True, True, False, False, True, True, True, True, True, True, False, False, False, True, True, False, True, True, True, True, False, False, False, True, False, True, True, True, True, True)
        s = [63, 95, 111, 119, 123, 125, 126, 159, 175, 183, 187, 189, 190, 207, 215, 219, 221, 222, 231, 235, 237, 238, 243, 245, 246, 249, 250, 252]

        n = log(len(tb), 2)
        p = partition(n=Integer(n))
        ou = 0
        for k in p:
            if p[k] == s:
                ou = k

        f = BooleanFunction([int(item) for item in tb])
        r = IVRestrictedAI.algebraic_immunity(f, s, balance_ratio=1)
        immunity_obj = FRMRestrictedAI()
        ai_k_n = immunity_obj.algebraic_immunity(f=f, s=s)
        print(r)
        self.assertEqual(ai_k_n, r)

    def test_failing_unbalanced_3(self):
        tb = (False, True, False, False, True, True, True, True, False, False, True, False, True, False, False, True, True, True, True, False, False, True, False, False, True, False, True, False, True, False, True, True, True, False, False, True, True, False, False, False, True, False, True, True, False, True, False, False, False, False, False, False, False, False, False, True, True, False, True, True, False, True, True, True, False, True, True, False, False, True, True, True, False, False, True, False, True, True, False, False, True, True, True, True, False, True, True, False, False, False, True, True, False, False, True, True, True, False, True, False, False, True, True, False, True, False, False, False, False, True, True, False, False, False, True, True, True, False, False, False, False, False, True, True, True, True, True, True, True, True, False, True, False, True, True, True, False, False, True, True, True, True, True, False, True, True, False, True, False, False, True, True, True, False, False, True, True, True, True, True, True, False, False, True, False, True, True, True, False, True, False, True, False, True, False, False, False, False, False, True, False, True, False, False, True, True, True, False, False, True, True, True, False, True, True, True, False, True, True, False, True, False, False, True, False, True, False, True, False, True, True, True, False, False, False, False, True, False, False, False, False, True, False, True, True, False, False, True, False, True, False, False, True, False, False, False, False, True, True, True, False, False, True, True, True, True, True, True, False, True, False, True, True, False, False, False)
        s = [63, 95, 111, 119, 123, 125, 126, 159, 175, 183, 187, 189, 190, 207, 215, 219, 221, 222, 231, 235, 237, 238, 243, 245, 246, 249, 250, 252]

        f = BooleanFunction([int(item) for item in tb])
        r = IVRestrictedAI.algebraic_immunity(f, s, balance_ratio=1)
        immunity_obj = FRMRestrictedAI()
        ai_k_n = immunity_obj.algebraic_immunity(f=f, s=s)
        print(r)
        self.assertEqual(ai_k_n, r)

    def test_failing_unbalanced_4(self):
        tb = (True, False, True, False, False, True, False, True, True, False, False, False, False, False, True, False, False, False, True, False, False, True, True, True, False, True, True, False, False, True, True, False, True, False, True, False, True, False, True, False, True, True, True, False, True, True, False, False, False, True, False, False, False, True, False, True, False, False, False, False, False, True, True, False, True, True, True, False, True, True, False, True, True, True, False, False, False, True, True, True, True, True, False, True, False, True, False, False, True, False, True, True, False, False, False, False, False, True, True, False, False, False, True, True, False, False, True, True, True, False, False, True, True, False, False, False, True, False, True, True, False, False, True, False, False, False, False, False, False, True, True, True, True, True, False, True, True, True, False, True, False, False, False, False, False, True, True, False, False, False, True, True, True, False, True, False, False, True, True, False, False, False, True, True, False, True, True, True, False, True, True, True, True, False, False, True, True, True, True, True, False, True, False, False, False, False, True, False, False, True, False, False, False, True, True, True, False, True, True, True, False, True, False, False, False, True, True, True, True, True, True, False, True, False, True, False, False, False, False, True, True, True, True, True, True, False, True, True, False, False, True, False, True, False, False, False, False, False, False, True, True, False, True, False, True, False, True, False, False, True, False, False, True, True, True, False)
        s = [15, 23, 27, 29, 30, 39, 43, 45, 46, 51, 53, 54, 57, 58, 60, 71, 75, 77, 78, 83, 85, 86, 89, 90, 92, 99, 101, 102, 105, 106, 108, 113, 114, 116, 120, 135, 139, 141, 142, 147, 149, 150, 153, 154, 156, 163, 165, 166, 169, 170, 172, 177, 178, 180, 184, 195, 197, 198, 201, 202, 204, 209, 210, 212, 216, 225, 226, 228, 232, 240]
        f = BooleanFunction([int(item) for item in tb])
        r = IVRestrictedAI.algebraic_immunity(f, s, balance_ratio=1)
        immunity_obj = FRMRestrictedAI()
        ai_k_n = immunity_obj.algebraic_immunity(f=f, s=s)
        print(r)
        self.assertEqual(ai_k_n, r)

    def test_failing_unbalanced_5(self):
        tb = (True, True, True, False, False, True, True, True, True, True, False, True, False, False, True, True, True, False, True, True, True, False, False, True, False, True, True, True, False, False, True, False, True, True, True, True, False, False, False, True, False, False, True, True, True, False, False, True, False, True, True, False, True, True, True, True, True, False, True, True, True, True, False, True, True, False, True, False, False, True, True, False, True, True, True, False, False, True, False, False, False, False, True, True, True, False, False, True, False, False, False, False, False, True, True, True, True, True, True, True, False, False, False, True, True, False, True, False, True, False, False, True, True, True, False, False, True, True, True, True, False, True, True, True, True, False, True, False, True, False, True, True, True, False, False, False, True, True, False, True, True, False, False, True, False, False, False, True, True, False, False, True, False, True, True, False, False, False, True, False, False, False, False, True, False, False, False, True, True, False, True, False, False, False, True, False, True, False, True, True, True, True, False, True, False, True, True, True, False, True, True, False, True, False, True, True, False, False, True, True, False, False, True, False, False, True, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, True, False, False, False, True, True, True, False, True, False, True, True, True, True, True, True, True, True, False, False, True, True, True, True, False, True, False, True, False, True, True, True, False, False, True, False, False, False, False, True, False, True, False, False, True, False, False, False, False, False, True, False, True, True, True, True, False, True, True, True, True, True, True, True, True, False, False, True, False, False, False, True, True, True, False, False, False, True, True, False, True, True, True, False, False, True, False, True, False, False, False, False, True, True, True, False, False, False, False, True, True, True, False, True, True, False, True, True, False, False, True, False, False, False, False, False, True, True, False, False, False, False, False, True, True, False, True, True, True, False, True, False, False, False, False, True, True, True, True, False, True, False, False, False, True, False, False, False, False, True, False, False, True, True, False, False, False, True, False, False, True, True, True, True, False, True, False, True, True, True, False, True, False, True, False, False, True, True, False, False, False, True, True, True, False, False, False, True, False, True, True, True, False, False, False, False, False, False, True, True, True, True, True, True, False, True, False, True, True, True, False, True, False, True, True, False, True, False, False, False, False, False, True, True, False, True, False, False, True, True, True, False, True, False, False, True, True, True, True, True, False, False, False, True, False, False, True, True, False, True, False, False, False, True, True, True, True, False, True, False, True, False, True, False, False, True, True, True, True, True, False, False, False, False, False, True, True, False, True, True, False, True, True, True, False, True, False, True, False, True)
        s = [63, 95, 111, 119, 123, 125, 126, 159, 175, 183, 187, 189, 190, 207, 215, 219, 221, 222, 231, 235, 237, 238, 243, 245, 246, 249, 250, 252, 287, 303, 311, 315, 317, 318, 335, 343, 347, 349, 350, 359, 363, 365, 366, 371, 373, 374, 377, 378, 380, 399, 407, 411, 413, 414, 423, 427, 429, 430, 435, 437, 438, 441, 442, 444, 455, 459, 461, 462, 467, 469, 470, 473, 474, 476, 483, 485, 486, 489, 490, 492, 497, 498, 500, 504]
        f = BooleanFunction([int(item) for item in tb])
        # r = IVRestrictedAI.algebraic_immunity(f, s, balance_ratio=1)
        immunity_obj = FRMRestrictedAI()
        ai_k_n = immunity_obj.algebraic_immunity(f=f, s=s)
        r = IVRestrictedAI.algebraic_immunity(f, s, balance_ratio=0.0000001)
        # n = log(len(tb), 2)
        #
        # p = partition(n=Integer(n))
        # ou = 0
        # for k in p:
        #     if p[k] == s:
        #         ou = k
        # r1 = AIk(ou,f)
        self.assertEqual(ai_k_n, r)

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

    def test_cmr(self):
        tb = (True, False, False, True, True, False, False, False, False, True, True, False, False, True, True, True, True, False, False, True, True, False, False, False, False, True, True, False, True, False, False, False, False, True, True, False, False, True, True, True, True, False, False, True, True, False, False, False, False, True, True, False, False, True, True, True, True, False, False, True, False, True, True, True, True, False, False, True, True, False, False, False, False, True, True, False, False, True, True, True, True, False, False, True, True, False, False, False, False, True, True, False, True, False, False, False, False, True, True, False, False, True, True, True, True, False, False, True, True, False, False, False, False, True, True, False, False, True, True, True, True, False, False, True, False, True, True, True, True, False, False, True, True, False, False, False, False, True, True, False, False, True, True, True, True, False, False, True, True, False, False, False, False, True, True, False, True, False, False, False, False, True, True, False, False, True, True, True, True, False, False, True, True, False, False, False, False, True, True, False, False, True, True, True, True, False, False, True, False, True, True, True, True, False, False, True, True, False, False, False, False, True, True, False, False, True, True, True, True, False, False, True, True, False, False, False, False, True, True, False, True, False, False, False, False, True, True, False, False, True, True, True, True, False, False, True, True, False, False, False, False, True, True, False, False, True, True, True, True, False, False, True, False, True, True, True)
        n = 8
        p = partition(n=Integer(n))

        for k in range(n+1):
            s = p[k]
            f = BooleanFunction([int(item) for item in tb])
            r = IVRestrictedAI.algebraic_immunity(f, s)
            immunity_obj = FRMRestrictedAI()
            ai_k_n = immunity_obj.algebraic_immunity(f=f, s=s)
            ai_k_n_n = AIk(k, f)

            print(r)
            self.assertEqual(ai_k_n, r)
            self.assertEqual(ai_k_n, ai_k_n_n)

    def test_get_combinations(self):
        kl = [[1,0,0,0], [0,1,0,0]]
        # com = IVRestrictedAI.GF2_span([1,0,0,0], [0,1,0,0,0])
        com = list(IVRestrictedAI.linear_combinations(kl))
        self.assertEqual(com, [[0, 1, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0]])

        kl = [[1,0,0], [0,1,0], [0,0,1]]
        com = list(IVRestrictedAI.linear_combinations(kl))
        self.assertEqual(com, [[0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])


