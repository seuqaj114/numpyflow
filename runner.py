import numpy as np
import numpyflow as nf

# Test run 
nf.Graph().as_default()

x = nf.Placeholder("x", shape=(2,3))
a = nf.Variable("a", (2,3), 1.0)
b = nf.Variable("b", (2,3), 2.0)

c = a + b + nf.Constant(1)
d = c + b + x
e = nf.matmul(a, nf.transpose(x))

print(nf.graph._default_graph.operations)
print(nf.graph._default_graph.variables)
sess = nf.Session()

# Fetch result of c
print(sess.run(c))
print(sess.run(d, {x: np.array([[1,2,3],[4,5,6]])}))
print(sess.run(e, {x: np.array([[1,2,3],[4,5,6]])}))