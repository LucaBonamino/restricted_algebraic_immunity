import unittest

from algebraic_immunity_utils import Matrix as GF2Matrix


class TestEchelonForm(unittest.TestCase):

    def test_echelon_form_last_row_simple(self):
        m = GF2Matrix([[1, 1], [1, 0]])
        m, ops = m.reduced_echelon_form_last_row()
        self.assertEqual(m.to_list(), [[1, 0], [0, 1]])
        self.assertEqual(ops, [(1, 0), (0, 1)])

    def test_2(self):
        m = [
            [1, 1, 1],
            [0, 0, 1],
            [1, 0, 1]
        ]
        m, ops = GF2Matrix(m).reduced_echelon_form_last_row()
        a = 1

    def test_3(self):
        m = [[1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0], [1, 1, 1, 0]]
        m, ops = GF2Matrix(m).reduced_echelon_form_last_row()
        a = 1

    def test_echelon_form_last_row_no_change(self):
        m = GF2Matrix([[1, 1], [0, 1]])
        m, ops = m.echelon_form_last_row()
        self.assertEqual(m.to_list(), [[1, 1], [0, 1]])
        self.assertEqual(ops, [])

        m = GF2Matrix([[1, 0], [0, 0]])
        m, ops = m.echelon_form_last_row()
        self.assertEqual(m.to_list(), [[1, 0], [0, 0]])
        self.assertEqual(ops, [])

    def test_reduced_echelon_form_full_matrix(self):
        m_l = [
            [1, 0, 0, 1],
            [0, 1, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
        ]

        m = GF2Matrix(m_l)
        m, ops = m.row_echelon_full_matrix()
        m2 = GF2Matrix(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
        )
        self.assertEqual(m.to_list(), m2.to_list())
