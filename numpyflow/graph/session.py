import numpy as np
from ..ops.base_ops import Op


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