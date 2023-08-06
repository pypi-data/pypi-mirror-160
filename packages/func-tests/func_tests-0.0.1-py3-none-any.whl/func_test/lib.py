from .cache import store


def func_test(func):
    """x
        Function should check func
    """
    def _executor(*args, **kwargs):
        """
            Function executor
        """
        name = func.__name__
        result = func(*args, **kwargs)
        store.add_func(name, result)
        return result

    return _executor


def assert_func(func_name, value, raise_=True):
    """
        Assert function
    """
    result = store.get_func_result(func_name)
    if raise_:
        assert result == value

    return result
