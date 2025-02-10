from pathlib import Path
import re

import pandas as pd
from typing import List, Dict

def from_dataframe_to_dict_of_dataframes(data_frame: pd.DataFrame, key_label: str, other_labels: List[str]) -> Dict[int, pd.DataFrame]:
    print(data_frame.columns)
    labels = data_frame[key_label].unique()
    new_dict = {k: {kl: [] for kl in other_labels} for k in labels}
    for index, row in data_frame.iterrows():
        for kl in other_labels:
            new_dict[row[key_label]][kl].append(row[kl])
    ret_dist = {k: pd.DataFrame(v) for k,v in new_dict.items()}
    return ret_dist

def from_latex_to_dataframe(filename: Path) -> pd.DataFrame:
    with filename.open("r") as file:
        lines = file.readlines()

    headers = []
    data_lines = []
    header_found = False

    for line in lines:
        line = line.strip()

        # Ignore LaTeX formatting lines
        if line.startswith(("\\", "%")) or "toprule" in line or "midrule" in line or "bottomrule" in line:
            continue

        # Step 1: Extract headers
        if not header_found:
            headers = [
                re.sub(r"[\$\{\}\\]", "", col).strip().replace(" ", "")  # Remove LaTeX syntax & spaces
                for col in line.split(" & ")
            ]
            header_found = True
        else:
            # Step 2: Clean data rows
            clean_line = re.sub(r"\\$", "", line).strip()  # Remove trailing '\\' if present
            clean_line = clean_line.replace("\\", "")  # Remove any remaining '\' symbols
            data_lines.append(re.sub(r"\s+", " ", clean_line).split(" & "))

    # Step 3: Convert to DataFrame
    df = pd.DataFrame(data_lines, columns=headers)

    # Step 4: Convert columns to numeric where possible
    df = df.apply(pd.to_numeric, errors="ignore")

    return df