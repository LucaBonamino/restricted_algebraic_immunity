
def get_pivot(row):
    for idx, val in enumerate(row):
        if val != 0:
            return idx
    return None


def copy(matrix):
    return [row[:] for row in matrix]


def generalized_echelon_form_GF2(matrix):
    m_copy = copy(matrix)
    rows = len(m_copy)
    cols = len(m_copy[0])
    operations = []
    lead = 0

    for r in range(rows):
        if lead >= cols:
            break
        i = r
        while m_copy[i][lead] == 0:
            i += 1
            if i == rows:
                i = r
                lead += 1
                if lead == cols:
                    return m_copy, operations
        m_copy[r], m_copy[i] = m_copy[i], m_copy[r]
        if r != i:
            operations.append((r, i))
            operations.append((i, r))
            operations.append((r, i))
        for i in range(rows):
            if i != r and m_copy[i][lead] == 1:
                m_copy[i] = [(x + y) % 2 for x, y in zip(m_copy[i], m_copy[r])]
                operations.append((i, r))
        lead += 1

    return m_copy, operations



m_l = [
            [1,0,0,1],
            [0,1,0,1],
            [0,0,0,1],
            [0,0,0,1],
        ]

generalized_echelon_form_GF2(m_l)



def echf_3(m):
    m_copy = copy(m)  # Assuming m is an object that has a `copy()` method
    last_row_index = m.nrows() - 1
    last_row = m_copy[-1]
    operations = []

    # Check for pivots and perform operations on the last row
    for col_index in range(m_copy.ncols()):
        p_index = get_pivot(last_row)  # This should find the pivot in the last row

        if p_index is None:
            print(m_copy)
            for row_index in range(1, m_copy.nrows() - 1)[::-1]:
                if m_copy[row_index].is_zero():
                    continue
                curr_pivot = get_pivot(m_copy[row_index])
                if curr_pivot == row_index:
                    break
                prev_pivot = get_pivot(m_copy[row_index - 1])
                # print(curr_pivot, prev_pivot)
                print()
                if prev_pivot is None or (prev_pivot is not None and curr_pivot < prev_pivot):
                    m_copy[row_index], m_copy[row_index - 1] = m_copy[row_index - 1], m_copy[row_index]
                    operations.append((row_index, row_index + 1))
                    operations.append((row_index + 1, row_index))
                    operations.append((row_index, row_index + 1))
                elif prev_pivot is not None and prev_pivot == curr_pivot == m_copy.ncols() - 1:
                    print(curr_pivot, prev_pivot)
                    m_copy[row_index] = m_copy[row_index] + m_copy[row_index - 1]
                    operations.append((row_index, row_index - 1))
            print("HERE Just")
            break
        else:
            p_row = None
            j_index = None

            # Look for a row above that has the pivot at p_index
            d_base = m_copy.nrows() - 1
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
                    print("HERE")
                    break

            if p_row is None:  # No row found with a pivot at p_index
                m_copy[-1], m_copy[closest] = m_copy[closest], m_copy[-1]
                last_row = m_copy[-1]  # Update the last row after the swap
                operations.append((closest, last_row_index))
                operations.append((last_row_index, closest))
                operations.append((closest, last_row_index))

            elif p_row[p_index] == 1:
                m_copy[-1] = m_copy[-1] + p_row
                last_row = m_copy[-1]
                operations.append((last_row_index, j_index))
                new_pivot = get_pivot(last_row)
                if new_pivot is not None:
                    for r in range(m_copy.nrows()):
                        if m_copy[r][new_pivot] == 1:
                            m_copy[r] = m_copy[r] + m_copy[last_row]

    return m_copy, operations


m_l = [
            [1,0,0,1],
            [0,1,0,1],
            [0,0,0,1],
            [0,0,0,1],
        ]

M = Matrix(GF(2), m_l)

echf_3(M)