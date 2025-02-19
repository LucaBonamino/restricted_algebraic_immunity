import argparse
import enum
import math
from restricted_algebraic_immunity.boolean_functions.boolean_function import CustomBooleanFunction
from restricted_algebraic_immunity.boolean_functions.known_boolean_functions.CMR import CMR
from restricted_algebraic_immunity.boolean_functions.known_boolean_functions.DM24 import SubDM24, DM24
from restricted_algebraic_immunity.boolean_functions.known_boolean_functions.TL import LT_WPB_rand, tl_truth_table
from restricted_algebraic_immunity.boolean_functions.known_boolean_functions.ZS23 import ZS23
from restricted_algebraic_immunity.entities.enums import ReturnType
from restricted_algebraic_immunity.utils.utils import is_WPB


def dm_24(n: int = 16, check: bool = False):
    u = SubDM24.evaluate
    v = u
    dm = DM24(n=n, u=u, v=v)
    bf = dm.boolean_function()
    if check is True:
        assert is_WPB(bf)
        assert DM24.is_wpb(bf.truth_table(), n) is True
    print('OK')
    df = dm.immunity_f_k(n=n, f=bf, return_type=ReturnType.DATA_FRAME, _verbose=False,
                         _hide=True)
    return df


def zn_23(n: int = 16, check: bool = False):
    m = int(math.log(n, 2))
    bf = ZS23.boolean_function(n=n, m=m)
    if check is True:
        assert is_WPB(bf)
        # assert ZS23.is_wpb(bf.truth_table(), n) is True
    # df = ZS23.immunity_f_k(f=bf, n=n, return_type=ReturnType.DATA_FRAME, _verbose=verbose, _hide=hide)
    df = ZS23.immunity_k(tt=bf.truth_table(), n=n, return_type=ReturnType.DATA_FRAME, _verbose=False, _hide=True)
    return df


def tl(n: int, random: bool = False, check: bool = False):
    # if random is True:
    if True:
        bf = LT_WPB_rand(n)
    else:
        bf = tl_truth_table[n]
    print(bf)
    if check is True:
        assert is_WPB(bf)
    immu = CustomBooleanFunction.immunity_f_k(f=bf, n=n, return_type=ReturnType.DATA_FRAME)
    print(immu)
    print(bf.truth_table(format='int'))
    return immu


def cmr(n: int, check: bool = False):
    bf = CMR(n)
    if check is True:
        assert is_WPB(bf)
        print(CustomBooleanFunction.is_wpb(bf.truth_table(), n)[1])
    print(bf.truth_table())
    immu = CustomBooleanFunction.immunity_f_k(f=bf, n=n, return_type=ReturnType.DATA_FRAME)
    print(immu)
    return immu


class FunctionsInputEnum(enum.Enum):
    DM24 = "DM24"
    ZJZQ23 = "ZJZQ23"
    TL19 = "TL29"
    CMR17 = "CMR17"


class FunctionsEnum(enum.Enum):
    DM24 = ('DM24', dm_24)
    ZJZQ23 = ("ZJZQ23", zn_23)
    TL19 = ("TL29", tl)
    CMR17 = ("CMR17", cmr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--function', type=lambda p: FunctionsInputEnum(p),
                        help="Function family of the function of which to calculate the AIk", required=True)
    parser.add_argument('-n', '--n_vars', type=int, help='Number of variables of the function', required=True)
    parser.add_argument('-c', '--check', action='store_false', help="Check if the function is WPB.")
    parser.add_argument('-r', '--random', action='store_false',
                        help="Take a random function from the family - only usable with LT19")
    args = parser.parse_args()
    if args.random is True and args.function != FunctionsInputEnum.TL19:
        print(f"invalid --random argument for function {args.function.value}, ignoring the -r argument")
    print(FunctionsEnum[args.function.name].value[1](n=args.n_vars))
