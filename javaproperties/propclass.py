import collections
from   six      import text_type  ### `string_types` instead?
from   .reading import read_properties

# https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html

class Properties(collections.MutableMapping):
    def __init__(self, defaults=None):
        ### Add arguments for constructing from/like a `dict`?
        self.data = {}
        self.defaults = defaults

    def __getitem__(self, key):
        if not isinstance(key, text_type):
            raise TypeError  ####
        try:
            return self.data[key]
        except KeyError:
            if self.defaults is not None:
                return self.defaults[key]
            else:
                raise

    def __setitem__(self, key, value):
        if not isinstance(key, text_type) or not isinstance(value, text_type):
            raise TypeError  ####
        self.data[key] = value

    def __delitem__(self, key):
        if not isinstance(key, text_type):
            raise TypeError  ####
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        ???

    def __eq__(self, other):
        return type(self) == type(other) and \
                self.data == other.data and \
                self.defaults == other.defaults

    def __ne__(self, other):
        return not (self == other)

    def getProperty(self, key, defaultValue=None)
        try:
            return self[key]
        except KeyError:
            return defaultValue

    def load(self, fp):
        self.data.update(read_properties(fp))

    def propertyNames(self):
        for k in self.data:
            yield k
        if self.defaults is not None:
            for k in self.defaults.propertyNames():
                if k is not in self.data:
                    yield k

    def setProperty(self, key, value):
        self[key] = value

    def store(self, out, comments=None):
        ???

    def stringPropertyNames(self):
        names = set(self.data)
        if self.defaults is not None:
            names.update(self.defaults.stringPropertyNames())
        return names

    def loadFromXML(self, fp):
        ???

    def storeToXML(self, out, comment=None, encoding=None):
        ???

    def list(self, out):
        ???
