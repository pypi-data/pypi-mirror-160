"""
    Func cache module
"""


class FuncCache:

    _instance = None
    _store = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
            class_._store = {}
        return class_._instance

    def add_func(self, function_name, return_value):
        """
            Function should add func to cache
        """
        self._store.update({function_name: return_value})
        return self

    def get_func_result(self, key):
        """
            Function should get func result
        """
        return self._store.get(key)

store = FuncCache()