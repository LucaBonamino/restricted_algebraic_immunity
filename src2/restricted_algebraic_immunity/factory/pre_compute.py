import argparse

import pandas as pd

from restricted_algebraic_immunity.full_reed_muller.pre_compute import pre_compute_all_separated, pre_compute_by_n_vars


def dummy():
    dtm, dt_d = [], []
    for n in range(1, 13):
        m, d = pre_compute_all_separated(n_vars=n)
        dtm.append(m)
        dt_d.append(d)

    df = pd.DataFrame({
        'G': dtm,
        'D': dt_d,
        'max_n': range(1, 13)
    })

    print(df.to_latex(index=False))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', '--max_n', help='Number of variables.', type=int)
    args = parser.parse_args()

    pre_compute_by_n_vars(n=args.max_n)

# print(pre_compute_all(10))