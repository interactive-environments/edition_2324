class SimpleNamespace:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        items = ("{}={!r}".format(key, getattr(self, key)) for key in self.__dict__)
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __eq__(self, other):
        if not isinstance(other, SimpleNamespace):
            return False
        for key in self.__dict__:
            if getattr(self, key) != getattr(other, key, None):
                return False
        return True
