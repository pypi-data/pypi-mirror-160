"""Utility functions temporarily provided until the rest of the democritus functions get uploaded."""

import functools
from typing import Iterable, Any, List


def map_first_arg(func):
    """If the first argument is a list or tuple, iterate through each item in the list and send it to the function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        iterable_arg = args[0]
        other_args = args[1:]

        # TODO: define these types elsewhere
        if isinstance(iterable_arg, (list, set, tuple)):
            results = []
            # iterate through the list argument sending each item into the function (along with the other arguments/kwargs)
            for item in iterable_arg:
                results.append(func(item, *other_args, **kwargs))
            return results
        else:
            return func(*args, **kwargs)

    return wrapper


def sort_by_length(list_arg: List[Any], **kwargs) -> List[Any]:
    """."""
    sorted_list = sorted(list_arg, key=lambda x: len(x), **kwargs)
    return sorted_list


def longest(iterable: Iterable) -> Any:
    """."""
    longest_item = sort_by_length(iterable, reverse=True)[0]
    return longest_item


def deduplicate(iterable: Iterable) -> list:
    """Deduplicate the iterable."""
    # TODO: will this work for every type except for dicts???
    deduplicated_list = list(set(iterable))
    return deduplicated_list
