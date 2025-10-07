# restricted_algebraic_immunity
This repository contains two algorithms to compute the restricted algebraic immunity of Boolean function.</br>
<ul>
    <li>Using punctured RM generator matrices - Algorithm 3.</li>
    <li>Constructing Vandermonde matrices iteratively - Algorithm 2.</li>
</ul>

In addition, the repository also contains the applications of the algorithms to WAPB and WPB functions. In particular: 
<ol>
    <li>Experimental comparison between the two algorithms on WAPB functions.</li>
    <li>AIk probability distribution of WPB_2,WPB_3 and WPB_4 functions.</li>
    <li>Computation of the AIk of four published WPB functions on 8 and 16 variables.
        <ul>
            <li><a href="https://www.researchgate.net/publication/368950658_A_New_Construction_of_Weightwise_Perfectly_Balanced_Functions_with_High_Weightwise_Nonlinearity">ZJZQ23</a></li>
            <li><a href="https://eprint.iacr.org/2024/422.pdf">DM24</a></li>
            <li><a href="https://www.researchgate.net/publication/333468298_A_family_of_weightwise_almost_perfectly_balanced_boolean_functions_with_optimal_algebraic_immunity">TL19</a></li>
            <li><a href="https://tosc.iacr.org/index.php/ToSC/article/view/771">CMR17</a></li>
        </ul>
    </li>
</ol>

To use Algorithm 2 and run Application 2, any Python interpreter between 3.8 and 3.11 may be used without any additional requirements not listed in the requirement.txt file. However, to use Algorithm 3 and to run Application 1. and 3, the Python interpreter must have the <i>SageMath</i> library installed.

<b>If you use this work, please cite:</b></br>
*"Computing the Restricted Algebraic Immunity, and Application to WPB Functions"*  
Luca Bonamino and Pierrick Méaux. [IACR ePrint 2025/1779](https://eprint.iacr.org/2025/1779).

While all the above-mentioned applications use Algorithm 2, only the AIk distribution relies on a full Rust implementation of it. This allows for a larger sample size in the AIk distribution compared to the one presented in the current version of the preprint.

## Installation

To use the full functionality of the repository, install and use the package in a python interpreter having the <i>SageMath</i> library installed.</br>
In particular, to use Algorithm 2, the <i>SageMath</i> library is not needed, but it is required if you want to use the command line interface getting installed with the package.</br>
Installing the package will also create an entry point command <code>restrictedAI</code> to use CLI tool. However, this command will only work if the package has been installed in an environment with the SageMath library.

### The algebraic_immunity_utils package as dependency
The project depends on the <code>algebraic_immunity_utils</code> python package which is implemented in Rust. To ensure anonymity of the corresponding paper the submission, such package has not been published to <b>PyPI</b>, but it's source code is located in the <i>algebraic_immunity_utils</i> directory. Therefore, its installations may be done by creating a build locally using <i>maturin</i> or by getting the wheels corresponding to your system from the GitHub release of this repository.

#### Local build
To build the <code>algebraic_immunity_utils</code> package locally, <b>Cargo</b> and the <b>maturin>=1.7</b> package are required.</br>
When these are installed, enter the <i>algebraic_immunity_utils</i> directory and run<br/> 
```maturin build --release```</br>
Then copy and paste the output in a pip install command:</br>
<ul>
    <li>On the SageMath python interpreter</br>
        <code>sage -pip install path_to_build</code>
    </li>
    <li>Installing on a general Python environment</br>
        <code>sage -pip install path_to_build</code>
    </li>
</ul>


#### Install via the wheels
The links of the wheels are present in the <i>requirements.txt</i> file. To see which of the provided wheels is the one corresponding to your system, run 
```bash
python construct_wheel_url -v 0.2.0
````

and uncomment the line in the <i>requirements.txt</i> file corresponding to the output.

##### Install via the wheels from Zenodo
The installation files are also hosted on Zenodo:  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15042593.svg)](https://doi.org/10.5281/zenodo.15042593)
 
To determine the correct wheel for your system, run the following command:
```bash
python construct_wheel_url -l zenodo -v 0.2.0
```


#### Install full project
Once you have either installed the <i>algebraic_immunity_utils</i> package from a local build or you have uncommented the correct line in the <i>requirements.txt</i> file corresponding to your system, you can install the full project.</br>
Installing on the SageMath python environment</br>
```sage -pip install .```</br>
Installing on a general Python environment</br>
```pip install .```

## Usage

### From Typer CLI
After installation, enter the sage environment shell by <code>sage -sh</code>, then run</br>
<code>restrictedAI --help</code></br>
to see the available commands

Note that if you have <i>SageMath</i> installed in your default python interpreter, you do not have to enter the sage shell, and can directly run <code>restrictedAI --help</code> from the current terminal.

The following commands are available:

#### AIk distributions
<code>restrictedAI distributions --help</code>

<ul>
    <li>AIk-distribution: <code>restrictedAI distributions AIk-distribution --help</code> 
    <ul>
        <li><code>--n</code>: number of variables.</li>
        <li><code>--sample-size</code>.</li>
        <li><code>--k-min</code>: minimum value of k.</li>
        <li><code>--k-max</code>: maximum value of k.</li>
        <li><code>--parallelize-by</code>: Type or parallelization: sequencial (no parallelization), by slice k or by sample.</li>
        <li><code>--algorithm</code>: algorithm to use: 2 or 3.</li>
    </ul>
        If k-min and k-max are not provided, the distribution and the averages will be calculated for all ks.</br>
        This will generate e files
        <ul>
            <li><i>factory-results/AIk_distributions/n_{n}/distribution_n_{n}_sample_{sample-size}_{parallelize-by}_{k-min}_{k_max}.txt</i></li>
            <li><i>factory-results/AIk_distributions/n_{n}/distribution_n_{n}_sample_{sample-size}_{parallelize-by}_{k-min}_{k_max}_averages.txt</i></li>
            <li><i>factory-results/AIk_distributions/n_{n}/times_{n}_sample_{sample-size}_{parallelize-by}_{k-min}_{k_max}.txt</i></li>
        </ul>
        In the case in which k-min and -k-max are not provided they will not appear in the filename:
        <ul>
            <li><i>factory-results/AIk_distributions/n_{n}/distribution_n_{n}_sample_{sample-size}_{parallelize-by}.txt</i></li>
            <li><i>factory-results/AIk_distributions/n_{n}/distribution_n_{n}_sample_{sample-size}_{parallelize-by}_averages.txt</i></li>
            <li><i>factory-results/AIk_distributions/n_{n}/times_{n}_sample_{sample-size}_{parallelize-by}.txt</i></li>
        </ul>
    </li>
    <li>Compute exact distribution for n=4 <code>restrictedAI distributions exact-distribution --n 4</code></li></br>
    The following files will be craated
    <ul>
        <li><i>factory-results/AIk_distributions/n_{n}/distribution_n_{n}_sample.txt</i></li>
        <li><i>factory-results/AIk_distributions/n_{n}/distribution_n_{n}_sample_averages.txt</i></li>
        <li><i>factory-results/AIk_distributions/n_{n}/times_n_{n}_sample.txt</i></li>
    </ul>
    </li>
    <li>plot-distribution: <code>restrictedAI distributions plot-distribution --help</code>
        <ul>
            <li><code>dist_filename</code>: filename of the text file where the AIk distribution is stored.</li>
            <li><code>average_filename</code>: filename of the text file where the AIk averages per k are stored.</li>
            <li><code>--parallelize-by</code>: parallelization type.</li>
            <li><code>--sample-size</code>: sample size.</li>
            <li><code>--n</code>: number of variables.</li>
        </ul>
        This will only run if the data for all ks are present. Meaning that the following files must exist:
        <ul>
            <li><i>factory-results/AIk_distributions/n_{n}/distribution_n_{n}_sample_{sample-size}_{parallelize-by}.txt</i></li>
            <li><i>factory-results/AIk_distributions/n_{n}/distribution_n_{n}_sample_{sample-size}_{parallelize-by}_averages.txt</i></li>
        </ul>
    </li>
</ul>

#### AIk of Published Functions
<code>restrictedAI functions --help</code>
<ul>
    <li>ZJZQ23
        <ul>
            <li><code>--n</code>: number of variables. For WPB, n must be a power of 2.</li>
            <li><code>--check</code>: validate that the function is WPB.</li>
        </ul>
    </li>
    <li>DM24
        <ul>
            <li><code>--n</code>: number of variables. For WPB, n must be a power of 2.</li>
            <li><code>--check</code>: validate that the function is WPB.</li>
        </ul>
    </li>
    <li>TL19</li>
        <ul>
            <li><code>--n</code>: number of variables. For WPB, n must be a power of 2.</li>
            <li><code>--check</code>: validate that the function is WPB.</li>
            <li><code>--random</code>: take a random function from the family.</li>
        </ul>
    <li>CMR17
        <ul>
            <li><code>--n</code>: number of variables. For WPB, n must be a power of 2.</li>
            <li><code>--check</code>: validate that the function is WPB.</li>
        </ul>
    </li>
</ul>

#### Algorithms comparison
<code>restrictedAI algs-comparison --help</code>

<ul>
    <li>Measure time execution of algorithm 1 <code>restrictedAI algs-comparison FMR-time-measurements --help</code>.</li>
    <li>Measure time execution of algorithm 3 <code>restrictedAI algs-comparison IV-time-measurements --help</code>.</li>
    <li>Produce comparison plot <code>restrictedAI algs-comparison comparison-plot --help</code>.</li>
</ul>

#### Pre-compute RM generator matrices for Algorithm 3
Pre compute $D^n$</br>
<code>restrictedAI pre-compute by-n --help</code></br>
Pre compute $D^{\leq n}$</br>
<code>restrictedAI pre-compute by-n-max --help</code>

### Without the Typer CLI
Without Typer CLI, the python scripts have to be executed individually.

#### AIk distributions
<code>python src/restricted_algebraic_immunity/factory/AIk_distribution.py --help</code>

#### AIk of Published Functions
<code>python src/restricted_algebraic_immunity/factory/AIk_of_published_functions.py --help</code>

#### Algorithms comparison
<code>python src/restricted_algebraic_immunity/factory/FMR_time_measurement.py --help</code></br>
<code>python src/restricted_algebraic_immunity/factory/IV_time_measurement.py --help</code></br>
<code>python src/restricted_algebraic_immunity/factory/produce_time_comparison_plot.py --help</code>

#### Pre-compute RM generator matrices for Algorithm 3
<code>python src/restricted_algebraic_immunity/factory/pre_compute.py --help</code>
