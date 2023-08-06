from typing import Iterator, TypeVar

from cognite.seismic.data_classes.errors import NotFoundError

T = TypeVar("T")


# This is moved out of utility.py to prevent circular import of NotFoundError
def get_single_item(iterator: Iterator[T], not_found_str: str) -> T:
    try:
        ret = next(iterator)
    except StopIteration:
        raise NotFoundError(not_found_str)
    try:
        next(iterator)
        raise Exception("Internal error: Found too many results. Please contact support.")
    except StopIteration:
        pass
    return ret
