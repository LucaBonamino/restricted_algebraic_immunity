from sage.all import *

def partition(n):
    """
    Compute the partition of range(2^n) in slices of integers according to their hamming weight.

    For instance,
      > partition(4)
      {0: [0], 1: [1, 2, 4, 8], 2: [3, 5, 6, 9, 10, 12], 3: [7, 11, 13, 14], 4: [15]}


    Args:
        n (int): number of variables

    Returns:
        dict: dictionary P such that P[k] is the set of numbers x in range(2^n) such that hw(x)=k
    """
    P = {}
    for i in range(n + 1): P[i] = []
    for d in range(2 ** n): P[bin(d).count("1")].append(d)
    return P


def is_WPB(f,verbose=False):
  """ Checks if a function is WAPB. The verification done via supports computation.
  Args:
      f (BooleanFunction)

  Returns:
      bool: True iff f is WPB
      (bool,int): (False, k) k is a slice cause failure
  """
  n=f.nvariables()
  assert n%2==0 and n.is_prime_power(), "number of variables not a power of 2!"
  fT=f.truth_table(format='int')
  if fT[0] or not fT[-1]: return False,(0,n)
  for k in range(1,n):
    if verbose: print(k)
    b=binomial(n,k)
    if size_suppk(f,k)!=b/2: return False,k
  return True,True

def Ekn(k,n):
  """Retuns integers between 0 and 2^n whose binary rapresentation has hamming weight k.

  Args:
      k (int): Hamming weight
      n (int): bitsize

  Returns:
      list : integers between 0 and 2^n with Hw k.
  """
  return list(filter(lambda d : (hw(bin(d)[2:])==k), range(2^n)))


def suppk(f, k, iter=False):
    """Computes the support of the Boolean function f restricted to the slice Ekn
    Args:
        f (Boolean function): _description_
        k (_type_): _description_
        iter (bool, optional): returns an iterator if True. Defaults to False.

    Returns:
        list or iter : support of the Boolean function f restricted to the slice Ekn
    """
    n = f.nvariables()
    # E=Ekn(k,n)
    fT = f.truth_table(format='int')
    if iter: return filter(lambda x: (fT[x] == 1), Ekn(k, n))
    return list(filter(lambda x: (fT[x] == 1), Ekn(k, n)))


def size_suppk(f, k):
    """Returns cardinality of the support of the Boolean function f restricted to the slice Ekn """
    return len(suppk(f, k))


def hw(x):
   """Compute the hamming weight of a vector x"""
   x=vector(ZZ,x)
   w=vector(ones_matrix(ZZ,1,len(x)))
   return w*x