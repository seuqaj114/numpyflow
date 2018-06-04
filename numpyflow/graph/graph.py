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

