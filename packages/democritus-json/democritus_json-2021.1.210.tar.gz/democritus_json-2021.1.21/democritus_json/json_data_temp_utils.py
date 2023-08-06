import functools


def json_read_first_arg_string(func):
    """Load the first argument as JSON (if it is a string)."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from .json_data import json_read

        first_arg = args[0]
        other_args = args[1:]

        if isinstance(first_arg, str):
            first_arg_json = json_read(first_arg)
            return func(first_arg_json, *other_args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper
