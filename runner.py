import numpy as np

class Graph:
    # Represents a computational graph 

    def __init__(self):
        # Construct Graph
        self.operations = []
        self.placeholders = []
        self.variables = []

    def as_default(self):
        global _default_graph
        _default_graph = self


class Session:

    def __init__(self):
        self.operations = []

    def run(self, fetch, feed_dict=None):

        if feed_dict == None:
            feed_dict = {}

        # Give values to placeholders
        for ph, value in feed_dict.items():
            ph.set_value(value)

        # Go through the operations backwards and collect all nodes that need
        # to be computed, in the correct order. Then perform the operations forward
        self.recurse(fetch)
        self.operations.append(fetch)

        for op in self.operations:
            op.execute()

        returns = fetch.value

        # Clear placeholders
        for ph in feed_dict.keys():
            ph.reset_value()

        # Clear graph
        for op in self.operations:
            op.reset_value()

        self.operations = []

        return returns

    def recurse(self, node):
        for inp in node.inputs:
            if isinstance(inp, Op):
                self.recurse(inp)
                self.operations.append(inp)


class Op:

    def __init__(self, *args):
        self.inputs = args
        self.value = None
        _default_graph.operations.append(self)

    def execute(self):
        pass

    def reset_value(self):
        self.value = None

    def validate_inputs(self):
        for inp in self.inputs:
            if inp.value is None:
                raise Exception("A value for %s was not provided." % inp)

    def __add__(self, obj):
        return AddOp(self, obj)


class AddOp(Op):

    def execute(self):
        self.validate_inputs()
        self.value = sum(inp.value for inp in self.inputs)


class Variable:
    # Variable class - we try to copy numpy's operations
    def __init__(self, name, shape, initial_value=0.0):
        assert isinstance(shape, list) or isinstance(shape, tuple)

        self.value = initial_value*np.ones(shape)
        self.shape = shape
        self.name = name

        _default_graph.variables.append(self)

    def __add__(self, obj):
        return AddOp(self, obj)

    def __str__(self):
        return "<Variable '%s', shape %s, at %s>" % (self.name, self.shape, hex(id(self)))

    def __repr__(self):
        return self.__str__()


class Placeholder():

    def __init__(self, name, shape):
        self.shape = shape
        self.name = name
        self.value = None

        _default_graph.placeholders.append(self)

    def set_value(self, value):
        assert value.shape == self.shape
        self.value = value

    def reset_value(self):
        self.value = None

    def __str__(self):
        return "<Placeholder '%s', shape %s, at %s>" % (self.name, self.shape, hex(id(self)))

    def __repr__(self):
        return self.__str__()


# Test run 

Graph().as_default()

x = Placeholder("x", (2,3))
a = Variable("a", (2,3), 1.0)
b = Variable("b", (2,3), 2.0)

c = a + b
d = c + b + x

print(_default_graph.operations)
print(_default_graph.variables)
sess = Session()

# Fetch result of c
print(sess.run(c))
print(sess.run(d, {x: np.array([[1,2,3],[4,5,6]])}))