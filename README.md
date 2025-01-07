# restricted_algebraic_immunity
This repository contains two algorithms to compute the restricted algebraic immunity of Boolean function.</br>
<ul>
    <li>Using punctured RM generator matrices - Algorithm 1</li>
    <li>Constructing Vandermonde matrix iteratively - Algorithm 3</li>
</ul>

In addition, the repository also contains the applications of the algorithms to WAPB and WPB functions. In particular: 
<ol>
    <li>Experimentally comparison between the two algorithms on WAPB functions.</li>
    <li>The applications on WPB functions:
        <ol>
            <li>AIk probability distribution of WPB_2,WPB_3 and WPB_4 functions.</li>
            <li>Computation of the AIk of two published WPB functions on 8 and 16 variables.</li>
        </ol>
    </li>
</ol>

To use Algorithm 3 and run Application 2.ii, any Python interpreter between 3.8 and 3.11 may be used while to use Algorithm 1 and to run Application 1. and 2.ii, the Python interpreter must have the SageMath library installed.

