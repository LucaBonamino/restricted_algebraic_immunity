import math
import time

from WPB_constructor import WAPBFamily
from restricted_algebraic_immunity.inductive_reed_muller.IV import IVRestrictedAI

times = {}
for n in range(1, 10):
    times[n] = 0
    k = math.ceil(n / 2)
    wapb_family = WAPBFamily(n=n)
    slice_ = wapb_family.slices[k]
    if n <= 6:
        vectors = slice_.generate_wapb_vectors()
        t_n = []
        for vector in vectors:
            t = time.time()
            IVRestrictedAI.algebraic_immunity_dist(s_image=vector, s=slice_.domain, n_vars=n)
            dt = time.time() - t
            t_n.append(dt)
        times[n] = sum(t_n) / len(vectors)


print(times)