from dictanykey.default_mixin import DefaultMixin
from dictanykey.unhashmap import UnHashMap


class DefaultUnHashMap(DefaultMixin, UnHashMap):
    """A dictionary that takes any key while also behaving like collections.defaultdict
       
       The default factory is called without arguments to produce
       a new value when a key is not present, in __getitem__ only.
       A defaultdict compares equal to a dict with the same items.
       All remaining arguments are treated the same as if they were
       passed to the dict constructor, including keyword arguments.
    """
    ...
