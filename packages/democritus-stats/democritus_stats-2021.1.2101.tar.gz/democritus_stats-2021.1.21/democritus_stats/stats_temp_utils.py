import functools


def string_to_decimal_first_arg(func):
    """Convert the first argument to a number (either integer or float)."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from democritus_strings import string_to_number

        first_arg = args[0]
        other_args = args[1:]

        first_arg = list(map(string_to_number, first_arg))

        return func(first_arg, *other_args, **kwargs)

    return wrapper
