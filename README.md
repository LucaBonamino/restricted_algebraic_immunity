# restricted_algebraic_immunity
This repository contains two algorithms to compute the restricted algebraic immunity of Boolean function.</br>
<ul>
    <li>Using punctured RM generator matrices - Algorithm 1.</li>
    <li>Constructing Vandermonde matrices iteratively - Algorithm 3.</li>
</ul>

In addition, the repository also contains the applications of the algorithms to WAPB and WPB functions. In particular: 
<ol>
    <li>Experimental comparison between the two algorithms on WAPB functions.</li>
    <li>AIk probability distribution of WPB_2,WPB_3 and WPB_4 functions.</li>
    <li>Computation of the AIk of two published WPB functions on 8 and 16 variables.</li>
</ol>

To use Algorithm 3 and run Application 2, any Python interpreter between 3.8 and 3.11 may be used without any additional requirements not listed in the requirement.txt file. However, to use Algorithm 1 and to run Application 1. and 3, the Python interpreter must have the SageMath library installed.

## Installation

To use the full functionality of the repository, install and use the package in a python interpreter having the <i>SageMath</i> library installed.</br>
In particular, to use Algorithm 3, the <i>SageMath</i> library is not needed, but to use the command line interface getting installed with the package, it is needed even if you only intend to run Algorithm 3.</br>
Installing the package will also create an entry point command <code>restrictedAI</code> to use CLI tool. However, this command will only work if the package has been installed in an environment with the SageMath library.

### The algebraic_immunity_utils package as dependency
The project depends on the <code>algebraic_immunity_utils</code> python package which is implemented in Rust. To ensure ananymity in the submission, such package has not been published to <b>PyPI</b>, but it is located in the <i>algebraic_immunity_utils</i>. Therefore, its installations may be done by creating a build locally using <i>maturin</i> or getting the wheels corresponding to your system from the GitHub release of the package.


### SageMath
Installing on the SageMath python environment</br>
```sage -pip install .```</br>
Installing on a general Python environment</br>
```pip install .```

