from pkg_resources import parse_version
import functools
from typing import List

def compare_versions(version_a: str, version_b: str):
    v_a = parse_version(version_a)
    v_b = parse_version(version_b)
    if v_a == v_b:
        return 0
    elif v_a > v_b:
        return 1
    else:
        return -1


def sort_list_by_version(d: List[str], reverse: bool = False):
    return sorted(d, key=functools.cmp_to_key(compare_versions), reverse=reverse)
