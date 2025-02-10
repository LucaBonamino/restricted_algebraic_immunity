import os
import logging
from pathlib import Path

root_dir = os.path.dirname(os.path.abspath(__file__))
root_path = f"{root_dir}"

factory_results_dir_name = "factory-results"
distributions_dir_name = f"{factory_results_dir_name}/AIk_distributions"
algs_comparison_dir_name = f"{factory_results_dir_name}/algs_comparison"

log_level = logging.INFO

logging.basicConfig(level=log_level)