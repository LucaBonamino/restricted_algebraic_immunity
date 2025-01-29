import algebraic_immunity_utils



m = algebraic_immunity_utils.Matrix([[1,1], [1,0]])

m.append_row([1,0])
print(m)

m.append_column([1,0,1])

print(m)

m = algebraic_immunity_utils.Matrix([[1,1], [0,0]])
print(m.kernel())

m = algebraic_immunity_utils.Matrix([[1,0], [0,0]])
print(m.kernel())

print()
m = algebraic_immunity_utils.Matrix([[1,1,0], [0,1,1]])
print(m.kernel())

m = algebraic_immunity_utils.Matrix([[1,1,0], [1,0,1], [1,1,1]])
print(m.row_echelon_full_matrix())
print(m)

print(m.to_list())


m = algebraic_immunity_utils.Matrix([[1,1,0,1], [0,0,1,0], [0,0,0,0]])
print(m.rank())

m = algebraic_immunity_utils.Matrix([
                                        [1, 1, 1, 1, 1],
                                        [0, 1, 0, 0, 0],
                                        [0, 0, 0, 0, 1],
                                        [0, 0, 0, 1, 0],
                                        [0, 0, 0, 0, 0]
                                    ])
ec = m.echelon_form_last_row()
print(ec[0])
print(ec[1])



m = algebraic_immunity_utils.Matrix([[1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0], [1, 1, 1, 0]])
ec = m.echelon_form_last_row()
print(ec[0])
print(ec[1])

m = algebraic_immunity_utils.Matrix([[1, 1, 1, 1], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 1]])
ec = m.echelon_form_last_row()
print(ec[0])
print(ec[1])

l = [[1, 1, 1, 1, 1], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [1, 0, 1, 1, 1]]

m = algebraic_immunity_utils.Matrix(l)
ec = m.echelon_form_last_row()
print(ec[0])
print(ec[1])


l = [[1, 1, 1, 1, 1], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [1, 0, 1, 1, 1]]

m = algebraic_immunity_utils.Matrix(l)
ec = m.echelon_form_last_row()
print(ec[0])
print(ec[1])


l = [[1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
     [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],
     [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0],
     [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
     [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1],
     [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]]

m = algebraic_immunity_utils.Matrix(l)
ec = m.echelon_form_last_row()
print(ec[0])
print(ec[1])

l = [[1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
         [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0],
         [0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1],
         [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
         [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
         [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1],
         [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0]]

m = algebraic_immunity_utils.Matrix(l)
ec = m.echelon_form_last_row()
print(ec[0])
print(ec[1])


l = [[1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
 [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1], [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))


import random

n = 4
M = [[random.randint(0,1) for _ in range(n)] for _ in range(n)]
print_matrix(M)
mr = algebraic_immunity_utils.Matrix(M)
print()
esc, ops = mr.row_echelon_full_matrix()
print_matrix(esc.to_list())
print(ops)


print(mr.get_sub_matrix(0,2).to_list())


