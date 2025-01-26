import pandas as pd

from restricted_algebraic_immunity.full_reed_muller.pre_compute import pre_compute_all, pre_compute_all_separated

# dtm, dt_d = [], []
# for n in range(1,13):
#     m, d = pre_compute_all_separated(n_vars=n)
#     dtm.append(m)
#     dt_d.append(d)
#
# df = pd.DataFrame({
#     'G': dtm,
#     'D': dt_d,
#     'max_n': range(1,13)
# })
#
# print(df.to_latex(index=False))


print(pre_compute_all(10))