import argparse
import os

from restricted_algebraic_immunity.full_reed_muller.FRM import FRMRestrictedAI
from restricted_algebraic_immunity.utils.logging import get_logger
from restricted_algebraic_immunity.factory.time_comparison import TimeMeasurement

_log = get_logger(__name__)


class FMRTimeMeasurement(TimeMeasurement):

    @classmethod
    def measure_time_for_ai_e_n_half(cls, max_n: int = 17, sample_size: int = 1000):
        im = FRMRestrictedAI()
        return cls.measure_time_for_ai_e_n_half_by_alg(im, max_n, sample_size)


def main(max_n, sample_size):
    # t = pre_compute_all(n_vars=args.max_n)
    t = 276.2263057231903

    times, aik_s = FMRTimeMeasurement.measure_time_for_ai_e_n_half(max_n=max_n, sample_size=sample_size)
    print(times)
    print()
    print(aik_s)
    times['pre_computation_time'] = t
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, f"results/FRM/times_{sample_size}_unique.csv")
    times.to_csv(file_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Time Calculator',
        description='Calculates the average AIk execution time for k = ceil(n/2) for different values of n',
    )
    parser.add_argument('-N', '--max_n', help='maximum value of n', type=int, default=5)
    parser.add_argument('-O', '--sample_size', help='sample_size', type=int, default=10000)
    args = parser.parse_args()

    main(max_n=args.max_n, sample_size=args.sample_size)
    # times, aik_s = FMRTimeMeasurement.measure_time_for_ai_e_n_half(max_n=args.max_n, sample_size=args.sample_size)
    # print(times)
    # print()
    # print(aik_s)
    # times['pre_computation_time'] = t
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(script_dir, f"results/FRM/times_{args.sample_size}_unique.csv")
    # times.to_csv(file_path, index=False)

    # file_path = os.path.join(script_dir, f"results/FRM/ai_ks_{args.sample_size}_unique.csv")
    # aik_s.to_csv(file_path, index=False)
