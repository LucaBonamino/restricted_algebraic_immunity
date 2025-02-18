from copy import copy
import random
import algebraic_immunity_utils


def get_pivot(row):
    for idx, v in enumerate(row):
        if v == 1:
            return idx




def verify_ech(m):
    p_old = 0
    flags = []
    for r in range(len(m)):
        p = get_pivot(m[r])
        if p is not None and p_old is not None:
            assert p_old <= p
            p_old = p
        else:
            if p_old is not None and p is None:
                flags.append(True)
            flags.append(False)
            p_old = p
    print(flags)
    # assert len([item for item in flags if item is False]) in [0,1]


n = 2**9
x = 2
l = [i*[0]+[1]+[ random.randint(0,1) for _ in range(n - 1-i)] for i in range(n)]

idx  = random.randint(0,1)
if idx == 0:
    for i in range(x, n):
        l[i] = [0 for _ in range(n)]

print(l)

verify_ech(algebraic_immunity_utils.Matrix(l).to_list())

l.append([random.randint(0,1) for _ in range(n)])

for i in range(len(l)):
    l[i] = l[i] + [random.randint(0,1)]

mat = algebraic_immunity_utils.Matrix(l)

print(mat)
ec = mat.echelon_form_last_row()[0]
verify_ech(ec.to_list())


# l = Matrix(GF(2), [[1, 1, 1, 1], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]])

# echf_1(l)
# print(ec)


ec_list = ec.to_list()
for idx, row in enumerate(ec_list):
    if row == [0 for _ in range(len(row))]:
        print(idx)
