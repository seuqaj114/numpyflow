import numpy as np

class Graph:
    # Represents a computational graph 

    def __init__(self):
        # Construct Graph
        self.operations = []
        self.placeholders = []
        self.variables = []
        self.constants = []

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
        self.validate_inputs()
        self.execute_specific()

    def execute_specific(self):
        # To be implemented by each specific operation
        raise NotImplementedError

    def reset_value(self):
        self.value = None

    def validate_inputs(self):
        for inp in self.inputs:
            if inp.value is None:
                raise Exception("A value for %s was not provided." % inp)

    def __add__(self, obj):
        return AddOp(self, obj)


class AddOp(Op):

    def __init__(self, *args):

        assert len(args) == 2
        super(AddOp, self).__init__(*args)
        # Get shape by running dummy operation with shape of inputs
        # This also allows validation of input shapes
        self.shape = (np.zeros(args[0].shape) + np.zeros(args[1].shape)).shape

    def execute_specific(self):
        self.value = self.inputs[0].value + self.inputs[1].value


class matmul(Op):

    def __init__(self, *args):

        assert len(args) == 2
        super(matmul, self).__init__(*args)
        self.shape = np.dot(np.zeros(args[0].shape),np.zeros(args[1].shape)).shape

    def execute_specific(self):
        self.value = np.dot(self.inputs[0].value, self.inputs[1].value)


class transpose(Op):

    def __init__(self, *args):

        assert len(args) == 1
        super(transpose, self).__init__(*args)
        self.shape = np.transpose(args[0]).shape

    def execute_specific(self): 
        self.value = np.transpose(self.inputs[0].value)


class Variable:
    # Variable class - we try to copy numpy's operations
    def __init__(self, name, shape, value=0.0):
        assert isinstance(shape, list) or isinstance(shape, tuple)

        self.value = value*np.ones(shape)
        self.shape = shape
        self.name = name

        _default_graph.variables.append(self)

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

        _default_graph.variables.append(self)

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

x = Placeholder("x", shape=(2,3))
a = Variable("a", (2,3), 1.0)
b = Variable("b", (2,3), 2.0)

c = a + b + Constant(1)
d = c + b + x
e = matmul(a, transpose(x))

print(_default_graph.operations)
print(_default_graph.variables)
sess = Session()

# Fetch result of c
print(sess.run(c))
print(sess.run(d, {x: np.array([[1,2,3],[4,5,6]])}))
print(sess.run(e, {x: np.array([[1,2,3],[4,5,6]])}))