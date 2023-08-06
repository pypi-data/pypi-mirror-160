# torchcuts - Convenient shortcuts to different namespaces

PyTorch contains a vast namespace which frequently overlaps with numpy.
Simplify with torchcuts! First, import the TorchCuts class and create an
instance:

~~~
from torchcuts import TorchCuts
tc = TorchCuts()
~~~

You now have access to common functions from both PyTorch and numpy.
Shortcuts to the PyTorch namespace begin with a capital letter, whereas
shortcuts to the numpy namespace are all lower case. For example:

~~~
N = 7
X = torch.linspace(0, N-1, N)
# Try with the torchcuts instance create previously:
X = tc.Lin(0, N-1, N)
~~~

Additionally, torchcuts also comes with a filter class. Instantiate this
class on an input tensor. You can then call then the instance on another
tensor, to find the elements in the original tensor that are nearest to
the elements in the argument tensor. The result is return in one-hot format.

~~~
from torchcuts import Filter
f = Filter([0, 1, 2])
f([0.25, 0.5, 0.75])
>>> torch.tensor([[1, 0, 0,], [0, 1, 0], [0, 1, 0]])
~~~

This filter class finds use for piecewise defined function on some
interval, such as for splines. 