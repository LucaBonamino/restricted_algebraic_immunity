from sage.all import *
from copy import copy
import random

def get_pivot(row):
    for idx, v in enumerate(row):
        if v == 1:
            return idx

def echf_1(m):
    m_copy = copy(m)  # Assuming m is an object that has a `copy()` method
    last_row_index = m.nrows() - 1
    last_row = m_copy[-1]
    operations = []

    # Check for pivots and perform operations on the last row
    for col_index in range(m_copy.ncols()):
        p_index = get_pivot(last_row)  # This should find the pivot in the last row

        if p_index is None:
            for row_index in range(1, m_copy.nrows() - 1)[::-1]:
                if m_copy[row_index].is_zero():
                    continue
                #print(row_index)
                curr_pivot = get_pivot(m_copy[row_index])
                if curr_pivot == row_index:
                    break
                prev_pivot = get_pivot(m_copy[row_index - 1])
                #print(curr_pivot, prev_pivot)
                #print()
                if prev_pivot is None or (prev_pivot is not None and curr_pivot < prev_pivot):
                    m_copy[row_index], m_copy[row_index - 1] = m_copy[row_index - 1], m_copy[row_index]
                    operations.append((row_index, row_index + 1))
                    operations.append((row_index + 1, row_index))
                    operations.append((row_index, row_index + 1))


            break
            # swap_row_index = None
            # for row_index in range(m_copy.nrows() - 1)[::-1]:
            #     if m_copy[row_index][row_index] == 0 and any(
            #             m_copy[row_index][k] == 1 for k in range(row_index + 1, m_copy.nrows())):
            #         swap_row_index = row_index
            # if swap_row_index is not None and not m_copy[swap_row_index+1].is_zero() :
            #     m_copy[swap_row_index], m_copy[swap_row_index + 1] = m_copy[swap_row_index + 1], m_copy[swap_row_index]
            #     operations.append((swap_row_index, swap_row_index + 1))
            #     operations.append((swap_row_index + 1, swap_row_index))
            #     operations.append((swap_row_index, swap_row_index + 1))
            # else:
            #     break

        else:
            p_row = None
            j_index = None

            # Look for a row above that has the pivot at p_index
            d_base = m_copy.nrows()-1
            closest = None
            for j in range(m_copy.nrows() - 1):  # Go up to the second-to-last row
                piv = get_pivot(m_copy[j])
                if piv is not None:
                    if piv == p_index:
                        p_row = m_copy[j]
                        j_index = j
                        break
                    else:
                        d = piv - p_index
                        if 0 < d < d_base:
                            closest = j
                            d_base = d
                else:
                    if closest is None:
                        closest = j
                    break
                # if m_copy[j][p_index] == 1 and not any(m_copy[j][k] == 1 for k in range(p_index)):
                #    p_row = m_copy[j]
                #    j_index = j
                #    break

            if p_row is None:  # No row found with a pivot at p_index
                if p_index == last_row_index:
                    swap_index_row = None
                    for r in range(m_copy.nrows() - 1):
                        if m_copy[r].is_zero():  # Check if row is zero
                            swap_index_row = r
                            break
                    if swap_index_row is not None:
                        m_copy[-1], m_copy[swap_index_row] = m_copy[swap_index_row], m_copy[-1]
                        operations.append((swap_index_row, last_row_index))
                        operations.append((last_row_index, swap_index_row))
                        operations.append((swap_index_row, last_row_index))
                    break  # Exit if we can't find a valid pivot
                # Swap rows to bring the pivot to the last row

                m_copy[-1], m_copy[closest] = m_copy[closest], m_copy[-1]
                last_row = m_copy[-1]  # Update the last row after the swap
                operations.append((closest, last_row_index))
                operations.append((last_row_index, closest))
                operations.append((closest, last_row_index))

            elif p_row[p_index] == 1:
                m_copy[-1] = m_copy[-1] + p_row
                last_row = m_copy[-1]
                operations.append((last_row_index, j_index))

    return m_copy, operations



n = 8
x = 2
l = [i*[0]+[1]+[ random.randint(0,1) for _ in range(n - 1-i)] for i in range(n)]

idx  = random.randint(0,1)
if idx == 0:
    used = []
    for i in range(x, n)[::-1]:
        to_add = [0 for _ in range(n)]
        if to_add not in used:
            l[i] = to_add


def verify_ech(m):
    p_old = 0
    flags = []
    for r in range(m.nrows()):
        p = get_pivot(m[r])
        if p is not None:
            assert p_old <= p
            p_old = p
        else:
            if p_old is not None and p is None:
                flags.append(True)
            flags.append(False)
            p_old = p
    assert len([item for item in flags if item is True]) in [0,1]


print(l)

verify_ech(Matrix(GF(2), l))

l.append([random.randint(0,1) for _ in range(n)])

for i in range(len(l)):
    l[i] = l[i] + [random.randint(0,1)]

mat = Matrix(GF(2), l)

print("mat")
print(mat)
ec = echf_1(mat)[0]
print()
print(ec)
verify_ech(ec)


# l = Matrix(GF(2), [[1, 1, 1, 1], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]])

# echf_1(l)



for idx, row in enumerate(ec):
    if row == [0 for _ in range(len(row))]:
        print(idx)
