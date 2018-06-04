import numpy as np
from .base_ops import Op


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