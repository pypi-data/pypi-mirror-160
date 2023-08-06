"""This is a collection of functions that really don't belong anywhere else."""

import functools
from typing import Any, Iterable, List, Dict, Union

from .utility_temp_utils import listify_first_arg, copy_first_arg

StrOrNumberType = Union[str, int, float]


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
    from democritus_lists import lists_are_same_length

    print('here')
    print(iterables)
    print(lists_are_same_length(*iterables, debug_failure=debug_failure))

    if not lists_are_same_length(*iterables, debug_failure=debug_failure):
        message = 'The given iterables are not the same length.'
        raise ValueError(message)

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


def subprocess_run(command, input_=None):
    """Run the given command as if it were run in a command line."""
    import shlex
    import subprocess

    if isinstance(command, str):
        command_list = shlex.split(command)
    else:
        command_list = command

    process = subprocess.run(command_list, input=input_, text=True, capture_output=True)
    result = (process.stdout, process.stderr)
    return result


def stringify_first_arg(func):
    """Decorator to convert the first argument to a string."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg_string = str(args[0])
        other_args = args[1:]
        return func(first_arg_string, *other_args, **kwargs)

    return wrapper


def retry_if_no_result(wait_seconds=10):
    """Decorator to call the given function and recall it if it returns nothing."""

    def retry_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time

            return_value = func(*args, **kwargs)

            if return_value:
                return return_value
            else:
                time.sleep(wait_seconds)
                return func(*args, **kwargs)

        return wrapper

    return retry_decorator


def copy_first_arg(func):
    """Decorator to make a copy of the first argument and pass into the func."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import copy

        first_arg = args[0]
        other_args = args[1:]
        try:
            first_arg_copy = copy.deepcopy(first_arg)
        # a RecursionError can occur when trying to do a deep copy on objects of certain classes (e.g. beautifulsoup objects) - see: https://github.com/biopython/biopython/issues/787, https://bugs.python.org/issue5508, and https://github.com/cloudtools/troposphere/issues/648
        except RecursionError as e:
            message = 'Performing a deep copy on the first arg failed; I\'ll just perform a shallow copy.'
            print(message)
            first_arg_copy = copy.copy(first_arg)
        return func(first_arg_copy, *other_args, **kwargs)

    return wrapper


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


def repeat_concurrently(n: int = 10):
    """Repeat the decorated function concurrently n times."""

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import concurrent.futures

            results = []

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for i in range(n):
                    function_submission = executor.submit(func, *args, **kwargs)
                    yield function_submission.result()

            return results

        return wrapper

    return actual_decorator


# TODO: there may be a cleaner way to create a decorator that takes arguments, but this works for now (see: https://stackoverflow.com/questions/10176226/how-do-i-pass-extra-arguments-to-a-python-decorator)
def validate_keyword_arg_value(keyword: str, valid_keyword_values: List[str], fail_if_keyword_not_found: bool = False):
    """Validate that the value for the given keyword is in the list of valid_keyword_values."""

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            keyword_value = kwargs.get(keyword)
            if not keyword_value:
                if fail_if_keyword_not_found:
                    message = f'The keyword "{keyword}" was not given.'
                    raise RuntimeError(message)
            else:
                if keyword_value not in valid_keyword_values:
                    message = f'The value of the "{keyword}" keyword argument is not valid (valid values are: {valid_keyword_values}).'
                    raise RuntimeError(message)

            return func(*args, **kwargs)

        return wrapper

    return actual_decorator


def validate_arg_value(arg_index: StrOrNumberType, valid_values: List[str]):
    """Validate that the value of the argument at the given arg_index is in the list of valid_values."""

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            arg_index_int = int(arg_index)
            arg_value = args[arg_index_int]

            if arg_value not in valid_values:
                message = f'The value of the argument at index {arg_index} (whose value is "{arg_value}") is not valid (valid values are: {valid_values}).'
                raise RuntimeError(message)

            return func(*args, **kwargs)

        return wrapper

    return actual_decorator


def wait_and_retry_on_failure(wait_seconds=10):
    """Try to call the given function. If there is an exception thrown by the function, wait for 10 seconds and try again."""

    def retry_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time

            try:
                return func(*args, **kwargs)
            except:
                time.sleep(wait_seconds)
                return func(*args, **kwargs)

        return wrapper

    return retry_decorator
