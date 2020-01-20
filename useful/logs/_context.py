import threading


class _Context(threading.local):
    """
    threading.local with additional methods for saving and restoring state.
    Main purpose is to allow copying data between threads. For example, we want
    to be able to copy the context to threads we create. We do this only when
    we can be sure that the data won't be changed afterwards, ie. to forward
    some already created information to child threads.
    """
    def save_state_to_dict(self):
        """
        Make a copy of self.__dict__ containing all the data we need.
        """
        return self.__dict__.copy()

    def load_state_from_dict(self, dictionary):
        """
        Basically set self.__dict__ = dictionary.
        """
        # Work only with empty _Context objects
        assert not self.__dict__
        for key, value in dictionary.items():
            self.__setattr__(key, value)

    def cleanup(self):
        """
        Remove all data stored in _Context.
        """
        for key in list(self.__dict__.keys()):
            delattr(self, key)


context = _Context()
