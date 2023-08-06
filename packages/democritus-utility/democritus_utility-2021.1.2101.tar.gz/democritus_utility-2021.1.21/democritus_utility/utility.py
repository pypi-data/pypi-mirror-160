"""This is a collection of functions that really don't belong anywhere else."""

from typing import Any, Iterable, List, Dict

from .utility_temp_utils import listify_first_arg, copy_first_arg


def has_more_than_one_item(thing: Any) -> bool:
    """Return whether or not the given thing has a length of at least one."""
    return thing and len(thing) > 1


def has_one_or_more_items(thing: Any) -> bool:
    """Return whether or not the given thing has a length of at least one."""
    return thing and len(thing) >= 1


def has_one_item(thing: Any) -> bool:
    """Return whether or not the given thing has a length of at least one."""
    return thing and len(thing) == 1


# TODO: there should be a decorator around this function (or maybe it should be converted entirely to a decorator)
def request_or_read(path):
    """If the given path is a URL, request the URL and return the content; if the path exists read the file; otherwise, just return the string and assume it is the input itself."""
    from democritus_urls import is_url
    from democritus_networking import get
    from democritus_file_system import file_exists, file_read

    # TODO: improve the code below; it is all wrapped in a try-except block primarily due to ValueErrors when trying to check if the file exists
    try:
        if is_url(path):
            return get(path, process_response=True)
        # TODO: do more here to make sure the path looks like a file path
        elif file_exists(path):
            return file_read(path)
        else:
            return path
    except:
        return path


@listify_first_arg
def is_sorted(iterable, *, descending: bool = False) -> bool:
    """Return whether or not the iterable is sorted."""
    return sorted(iterable, reverse=descending) == iterable


@listify_first_arg
def first_unsorted_value(iterable, *, descending: bool = False) -> Any:
    """Return the first unsorted value in the iterable."""
    sorted_items = sorted(iterable, reverse=descending)
    for original_item, sorted_item in zip(iterable, sorted_items):
        if original_item != sorted_item:
            return original_item


@listify_first_arg
@copy_first_arg
def last_unsorted_value(iterable, *, descending: bool = False) -> Any:
    """Return the last unsorted value in the iterable."""
    # we reverse everything so we can iterate through the iterable and return the first item that is not sorted
    iterable.reverse()
    descending = not descending

    sorted_items = sorted(iterable, reverse=descending)
    for original_item, sorted_item in zip(iterable, sorted_items):
        if original_item != sorted_item:
            return original_item


@listify_first_arg
def unsorted_values(iterable, *, descending: bool = False) -> Iterable[Any]:
    """."""
    sorted_items = sorted(iterable, reverse=descending)
    for original_item, sorted_item in zip(iterable, sorted_items):
        if original_item != sorted_item:
            yield original_item


@listify_first_arg
def sorted_values(iterable, *, descending: bool = False) -> Iterable[Any]:
    """."""
    sorted_items = sorted(iterable, reverse=descending)
    for original_item, sorted_item in zip(iterable, sorted_items):
        if original_item == sorted_item:
            yield original_item


def ignore_errors(function, *args, **kwargs):
    """."""
    result = None
    try:
        result = function(*args, **kwargs)
    except:
        pass

    return result


def zip_padded(*iterables, fillvalue: Any = None):
    """Zip through the longest iterable using the fillvalue to replace any items in an iterable once it has no more items."""
    import itertools

    for i in itertools.zip_longest(*iterables, fillvalue=fillvalue):
        yield i


def zip_if_same_length(*iterables, debug_failure: bool = False):
    """Zip the given iterables if they are the same length. If they are not the same length, raise an assertion error."""
    from lists import lists_are_same_length

    assert lists_are_same_length(*iterables, debug_failure=debug_failure)

    for i in zip(*iterables):
        yield i


def unique_items(iterable_a: Any, iterable_b: Any) -> Dict[str, set]:
    """Find the values unique to iterable_a and iterable_b (relative to one another)."""
    unique_items_list = {'a': [], 'b': []}

    set_a = set(iterable_a)
    set_b = set(iterable_b)
    unique_items_list['a'] = set_a.difference(set_b)
    unique_items_list['b'] = set_b.difference(set_a)

    return unique_items_list


def prettify(thing: Any, *args):
    """."""
    import pprint

    p = pprint.PrettyPrinter(*args)
    return p.pformat(thing)


def pretty_print(thing: Any, *args):
    """."""
    print(prettify(thing, *args))
