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

### gf2_linear_algebra_utils
The project depends on the <code>gf2_linear_algebra_utils</code> python package implemented in Rust. The package is located in the <i>gf2_linear_algebra_utils</i> and its installable from wheels or from by creating a build from your system using <i>maturin</i>.


### SageMath
Installing on the SageMath python environment</br>
```sage -pip install .```</br>
Installing on a general Python environment</br>
```pip install .```

Installing the package will also create an entry point command <code>restrictedAI</code> to use CLI tool. However, this command will only work if the package has been installed in an environment with the SageMath library.