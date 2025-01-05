import math

from restricted_algebraic_immunity.boolean_functions.known_boolean_functions.DM24 import SubDM24, DM24
from restricted_algebraic_immunity.boolean_functions.known_boolean_functions.ZS23 import ZS23
from restricted_algebraic_immunity.entities.enums import ReturnType


def dm_24(n: int = 16):
    u = SubDM24.boolean_function(n // 2)
    v = u
    dm = DM24(n=n, u=u, v=v)
    bf = dm.boolean_function()
    df = dm.immunity_f_k(n=n, f=bf, return_type=ReturnType.DATA_FRAME, _verbose=False,
                             _hide=True)
    return df

def zn_23(n:int = 16):
    m = int(math.log(n, 2))
    bf = ZS23.boolean_function(n=n, m=m)
    # df = ZS23.immunity_f_k(f=bf, n=n, return_type=ReturnType.DATA_FRAME, _verbose=verbose, _hide=hide)
    df = ZS23.immunity_k(tt=bf.truth_table(), n=n, return_type=ReturnType.DATA_FRAME, _verbose=False, _hide=True)
    return df

if __name__ == '__main__':
    # print("DM24 8")
    # print(dm_24(8))
    # print()
    print("ZN23 8")
    print(zn_23(8))
    print(dm_24(8))