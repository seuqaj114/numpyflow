import numpy as np
from ..graph import graph


class Op:

    def __init__(self, *args):
        self.inputs = args
        self.value = None
        graph._default_graph.operations.append(self)

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
