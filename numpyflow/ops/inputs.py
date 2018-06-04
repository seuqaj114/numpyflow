import numpy as np
from ..graph import graph
from .base_ops import AddOp

class Variable:
    # Variable class - we try to copy numpy's operations
    def __init__(self, name, shape, value=0.0):
        assert isinstance(shape, list) or isinstance(shape, tuple)

        self.value = value*np.ones(shape)
        self.shape = shape
        self.name = name

        graph._default_graph.variables.append(self)

    def __add__(self, obj):
        return AddOp(self, obj)

    def __str__(self):
        return "<Variable '%s', shape %s, at %s>" % (self.name, self.shape, hex(id(self)))

    def __repr__(self):
        return self.__str__()


class Constant:

    def __init__(self, value):
        assert type(value) in [int, float, np.ndarray], "%s" % type(value)

        self.value = np.array(value)
        self.shape = np.shape(value)

        graph._default_graph.variables.append(self)

    def __add__(self, obj):
        return AddOp(self, obj)

    def __str__(self):
        return "<Constant %s, shape %s, at %s>" % (self.value, self.shape, hex(id(self)))

    def __repr__(self):
        return self.__str__()


class Placeholder:

    def __init__(self, name, shape):
        self.shape = shape
        self.name = name
        self.value = None

        graph._default_graph.placeholders.append(self)

    def set_value(self, value):
        assert value.shape == self.shape
        self.value = value

    def reset_value(self):
        self.value = None

    def __str__(self):
        return "<Placeholder '%s', shape %s, at %s>" % (self.name, self.shape, hex(id(self)))

    def __repr__(self):
        return self.__str__()
