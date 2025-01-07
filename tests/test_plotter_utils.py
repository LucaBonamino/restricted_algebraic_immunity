import unittest
from pathlib import Path

import pandas as pd

from restricted_algebraic_immunity.factory.plotter_utils import from_dataframe_to_dict_of_dataframes, \
    from_latex_to_dataframe


class TestPlotterUtils(unittest.TestCase):

    def test_from_dataframe_to_dict_of_dataframes(self):
        k = [0, 0, 0, 0, 1, 1, 1, 1]
        v1 = [1, 2, 3, 4, 5, 6, 7, 8]
        v2 = [8, 7, 6, 5, 4, 3, 2, 1]

        df = pd.DataFrame({
            'k': k,
            'v1': v1,
            'v2': v2}
        )

        resp = from_dataframe_to_dict_of_dataframes(data_frame=df, other_labels=['v1', 'v2'], key_label='k')


    def test_from_latex_to_dataframe(self):
        f_name = Path(
            '../src/restricted_algebraic_immunity/factory/results/IV/AIk_distributions/n_16/distribution_n_16_sample_16_a_0_4.txt')
        resp = from_latex_to_dataframe(filename=f_name)
        k = list(resp['k'])

