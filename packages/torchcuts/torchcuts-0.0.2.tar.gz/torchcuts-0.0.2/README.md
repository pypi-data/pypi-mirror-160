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
