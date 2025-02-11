import unittest
from typing import List, Tuple, Union

from algebraic_immunity_utils import Matrix as GF2Matrix
from algebraic_immunity_utils import verify


class TestBasicMethods(unittest.TestCase):

    def test_to_list(self):
        m = GF2Matrix([[1, 1], [1, 0]])
        self.assertEqual(m.to_list(), [[1, 1], [1, 0]])

    def test_add_rows(self):
        m = GF2Matrix([[1, 1], [1, 0]])
        m.append_row([1, 0])

        m_res = GF2Matrix([[1, 1], [1, 0], [1, 0]])
        self.assertEqual(m, m_res)

    def test_compute_next(self):
        m = GF2Matrix([[1, 1], [1, 0]])
        support_slice = ['00', '01', '10']
        monom_slice = ['00', '01', '10']
        idx = 2
        operations = []
        n = m.compute_next(monom_slice, support_slice, idx, operations)
        self.assertEqual(n.to_list(), [[1, 1, 0], [1, 0, 0], [1, 0, 1]])

        m = GF2Matrix([[1, 1], [0, 1]])
        support_slice = ['000', '010', '100']
        monom_slice = ['000', '001', '010']
        idx = 2
        operations = [(0, 1)]
        n_m = m.compute_next(monom_slice, support_slice, idx, operations)
        self.assertEqual(n_m.to_list(), [[1, 1, 1], [0, 1, 1], [1, 0, 0]])
        self.assertEqual(m.to_list(), [[1, 1], [0, 1]])

    def construct_and_add_column(self):
        m = GF2Matrix([[1, 1], [1, 0]])
        support_slice = ['00', '01', '10']
        monom_slice = ['00', '01', '10']
        idx = 2
        operations = []
        n = m.compute_next(monom_slice, support_slice, idx, operations)
        self.assertEqual(n.to_list(), [[1, 1, 0], [1, 0, 0], [1, 0, 1]])

    def test_verify(self):
        resp = verify(['001'], [0, 0, 1], ['000', '001', '010', '011'])
        self.assertEqual(resp, (True, None))

        resp = verify(['001', '000'], [0, 0, 1], ['000', '001', '010', '011'])
        self.assertEqual(resp, (True, None))

        resp = verify(['001', '000', '100'], [0, 0, 1, 1], ['000', '001', '010', '100', '011'])
        self.assertEqual(resp, (False, (2, '100')))

        resp = verify(['000', '011'], [0, 0, 1, 0, 1], ['000', '001', '010', '100', '011'])
        self.assertEqual(resp, (True, None))

        resp = verify(['000', '010', '011'], [0, 0, 1, 0, 1], ['000', '001', '010', '100', '011'])
        self.assertEqual(resp, (False, (1, '010')))


def is_submonomial(sub_monom: str, monom: str) -> bool:
    assert len(sub_monom) == len(monom)
    for char1, char2 in zip(sub_monom, monom):
        if char1 > char2:
            return False
    return True


def verify_p(z: List[str], g: List[int], mapping: List[str]) -> Tuple[bool, Union[None, Tuple[int, str]]]:
    for idx, item in enumerate(z):
        anf = [g[i] for i in range(len(g)) if is_submonomial(sub_monom=mapping[i], monom=item) is True]
        if sum(anf) % 2 == 1:
            return False, (idx, item)
    return True, None
