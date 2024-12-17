import os
import logging

root_dir = os.path.dirname(os.path.abspath(__file__))
root_path = f"{root_dir}"

log_level = logging.INFO

logging.basicConfig(level=log_level)