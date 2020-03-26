import functools
from typing import List

from pkg_resources import parse_version


def compare_versions(version_a: str, version_b: str) -> int:
    """Compare versions as defined by PEP 440.

    https://www.python.org/dev/peps/pep-0440/
    Args:
        version_a (str): version to be compared
        version_b (str): version to be compared
    Returns:
        0: if versions are the same
        1: if version_a > version_b
        -1: if version_a < version_b
    """
    v_a = parse_version(version_a)
    v_b = parse_version(version_b)
    if v_a == v_b:
        return 0
    elif v_a > v_b:
        return 1
    else:
        return -1


def sort_list_by_version(l: List[str], reverse: bool = False) -> List[str]:
    """Sort a list of versions as defined by PEP 440.

    Args:
        l (List[str]): List of strings (versions) to be parsed
        reverse (bool): Whether or not to sort in reverse order.
    Returns:
        Sorted list `l`.
    """
    return sorted(l, key=functools.cmp_to_key(compare_versions), reverse=reverse)
