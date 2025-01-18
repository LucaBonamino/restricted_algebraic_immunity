import argparse
import enum
import math

from restricted_algebraic_immunity.boolean_functions.boolean_function import CustomBooleanFunction
from restricted_algebraic_immunity.boolean_functions.known_boolean_functions.CMR import CMR
from restricted_algebraic_immunity.boolean_functions.known_boolean_functions.DM24 import SubDM24, DM24
from restricted_algebraic_immunity.boolean_functions.known_boolean_functions.TL import LT_WPB_rand
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


def tl(n: int, check: bool = False):
    bf = LT_WPB_rand(n)
    print(bf)
    if check is True:
        assert is_WPB(bf)
    immu = CustomBooleanFunction.immunity_f_k(f=bf, n=n, return_type=ReturnType.DATA_FRAME)
    print(immu)
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
    ZS23 = "ZS23"
    TL19 = "TL29"
    CMR = "CMR"

class FunctionsEnum(enum.Enum):
    DM24 = ('DM24', dm_24)
    ZS23 = ("ZS23", zn_23)
    TL19 = ("TL29", tl)
    CMR = ("CMR", cmr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--function', type=lambda p: FunctionsInputEnum(p),
                        help="Function family of the function of which to calculate the AIk", required=True)
    parser.add_argument('-n', '--n_vars', type=int, help='Number of variables of the function', required=True)
    parser.add_argument('-c', '--check', action='store_false', help="Check if the function is WPB.")
    args = parser.parse_args()
    print(FunctionsEnum[args.function.name].value[1](n=args.n_vars))
