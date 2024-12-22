import argparse
import os
import textwrap

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt



def main(df_iv, df_rmf, sample_size):
    max_n = max(df_iv['n'].values)
    pre_computation_time = df_rmf['pre_computation_time'][0]

    print(df_iv)
    # Plot the data
    plt.plot(df_iv['n'], df_iv['$T(AI_{n/2})$'], marker='x', label="Algorithm 3")
    plt.plot(df_rmf['n'], df_rmf['$T(AI_{n/2})$'], marker='o', label="Algorithm 1")
    plt.xticks(range(int(min(df_iv['n'])), int(max(df_iv['n'])) + 1))
    plt.xlabel(r'$n$')
    plt.ylabel(r'$\mathbb{E}\left[T\left(AI_{\lceil{n/2}\rceil}\right)\right]$', rotation=90)
    # plt.title(rf'Average execution time of Algorithm 1 and 2 on $S = E_{{n,\lceil{{n/2}}\rceil}}$ for $n$ from $0$ to ${max_n}$ with $|\Omega| = {sample_size}$\nPrecomputation of $D$ for Algorithm 1: {pre_computation_time}')

    title = (
        f"Average execution time of Algorithm 1 and 3 on $S = E_{{n,\\lceil{{n/2}}\\rceil}}$"
        f"with $|\\Omega| = {sample_size}$\n$T(D^{{\leq n_{max}}} )$ for Algorithm 1: {round(pre_computation_time,4)}"
    )

    # Wrap title
    # wrapped_title = "\n".join(textwrap.wrap(title, width=80))
    # Increase width and height
    plt.title(title, fontsize=10)

    plt.legend(loc="upper right")
    plt.grid()
    plt.show()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, f"results/plot_{sample_size}.png")
    plt.savefig(filename)


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