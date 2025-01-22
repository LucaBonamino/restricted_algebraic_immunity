import argparse
import os


from restricted_algebraic_immunity.factory.time_comparison import TimeMeasurement
from restricted_algebraic_immunity.inductive_reed_muller.IV import IVRestrictedAI
from restricted_algebraic_immunity.utils.logging import get_logger

_log = get_logger(__name__)



class IVTimeMeasurement(TimeMeasurement):

    @classmethod
    def measure_time_for_ai_e_n_half(cls, max_n: int = 17, sample_size: int = 1000, parallel=False):
        return cls.measure_time_for_ai_e_n_half_by_alg(alg=IVRestrictedAI, max_n=max_n, sample_size=sample_size, parallel=parallel)


def main(max_n, sample_size):
    times, aik_s = IVTimeMeasurement.measure_time_for_ai_e_n_half(max_n=max_n, sample_size=sample_size,
                                                                  parallel=False)
    print(times)
    print()
    print(aik_s)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, f"results/IV/times_{max_n}_{sample_size}.csv")
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



    #file_path = os.path.join(script_dir, f"results/IV/ai_ks_{args.sample_size}.csv")
    #aik_s.to_csv(file_path, index=False)


