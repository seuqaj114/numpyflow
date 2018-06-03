import numpy as np
from numpyflow.ops import matmul, transpose, Variable, Constant, Placeholder
from numpyflow.graph import Graph

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