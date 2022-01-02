from typing import Dict, List


def from_dictval_to_list(dict: Dict):
    data = []
    for val in dict.values():
        data.append(val)
    return data
