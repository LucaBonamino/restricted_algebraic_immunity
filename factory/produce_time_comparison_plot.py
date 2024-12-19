import argparse
import os

import pandas as pd
import matplotlib.pyplot as plt

def main(df_iv, df_rmf, sample_size):
    max_n = max(df_iv['n'].values)

    print(df_iv)
    # Plot the data
    plt.plot(df_iv['n'], df_iv['$T(AI_{n/2})$'], marker='x', label="Algorithm 1")
    plt.plot(df_rmf['n'], df_rmf['$T(AI_{n/2})$'], marker='o', label="Algorithm 2")
    plt.xlabel(r'$n$')
    plt.ylabel(r'$\mathbb{E}\left[T\left(AI_{\lceil{n/2}\rceil}\right)\right]$', rotation=90)
    plt.title(rf'Average execution time of Algorithm 1 and 2 on $S = E_{{n,\lceil{{n/2}}\rceil}}$ for $n$ from $0$ to ${max_n}$ with $|\Omega| = {sample_size}$')
    plt.legend(loc="upper right")
    plt.grid()
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Time Plotter',
        description='Plot the average AIk execution time for k = ceil(n/2) for different values of n',
    )
    parser.add_argument('-N', '--max_n', help='maximum value of n', type=int)
    parser.add_argument('-O', '--sample_size', help='sample_size', type=int)
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_1 = os.path.join(script_dir, f"results/IV/times_{args.sample_size}.csv")
    file_path_2 = os.path.join(script_dir, f"results/FRM/times_{args.sample_size}.csv")

    df_1 = pd.read_csv(f'{file_path_1}')
    df_2 = pd.read_csv(f'{file_path_2}')

    main(df_1, df_2, args.sample_size)