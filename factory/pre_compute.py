from restricted_algebraic_immunity.full_reed_muller.pre_compute import pre_compute_all

for n in range(1,11):
    print(pre_compute_all(n_vars=12))

# print(pre_compute_all(10))