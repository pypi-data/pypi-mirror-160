import functools


def arguments_as_decimals(func):
    """Convert all arguments to numbers (either integers or floats)."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from democritus_strings import string_to_number
        from .maths import is_integer_tuple, integer_tuple_to_decimal

        new_args = []
        for arg in args:
            if isinstance(arg, str):
                new_args.append(string_to_number(arg))
            elif is_integer_tuple(arg):
                decimal_arg = integer_tuple_to_decimal(arg)
                new_args.append(decimal_arg)
            else:
                new_args.append(arg)
        return func(*new_args, **kwargs)

    return wrapper
