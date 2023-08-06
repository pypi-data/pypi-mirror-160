"""Filters"""
#  Copyright (c) 2022. Asger Jon Vistisen All Rights Reserved.
from typing import NoReturn

import torch
from torch import Tensor

from torchcuts import TorchCuts


class Filter:
  """Instances of Filter are created on the basis of a given filter base.
  Calling an instance on a tensor"""

  eps = 1e-08
  tc = TorchCuts()

  @staticmethod
  def ensureTensor(X: Tensor | list) -> Tensor:
    """This static method returns a tensor, if X is a list. Otherwise,
    it simply returns X back."""
    tc = TorchCuts()
    return X if isinstance(X, Tensor) else torch.tensor(X).to(tc.F32)

  def __init__(self, X0: Tensor | list, ) -> NoReturn:
    self._X0, _ = torch.sort(self.ensureTensor(X0).view(-1))

  def __call__(self, X: Tensor | list) -> Tensor:
    """Calling an instance returns a one-hot tensor."""
    tc = TorchCuts()
    X = self.ensureTensor(X)
    outShape = [self.N0, *[i for i in X.shape]]
    X = X.view(1, -1)
    XE = tc.J(self.N0, 1) @ X
    X0E, N = self.X0 @ tc.J(X.shape), X.view(-1).shape[0]
    linds = tc.Lin(0, N - 1, N).view(-1).to(torch.long)
    inds = torch.argmin(torch.cosh(XE - X0E), dim=0).view(-1).to(torch.long)
    out = tc.Oh(self.N0, N)
    out[inds, linds] = 1
    return out.view(outShape)
  
  def getLimits(self) -> list[float]:
    """Returns a list of the limits used at creation time"""
    return self.X0.tolist()

  def getN0(self) -> int:
    """Getter-function for number of entries in limits"""
    return self.X0.shape[0]

  def getMin(self) -> float:
    """Getter-function for smallest value in X0"""
    return self.X0[0]

  def getMax(self) -> float:
    """Getter-function for largest value in X0"""
    return self.X0[-1]

  def getX0(self) -> Tensor:
    """Getter function for filter values"""
    return self._X0.view(-1, 1)

  def getXH(self) -> Tensor:
    """Getter-function for filter values with index offset"""

  def _bad(self, *_) -> NoReturn:
    """Bad setter/deleter"""
    raise TypeError('Tried setting or deleting readonly variable')

  X0 = property(getX0, _bad, _bad)
  N0 = property(getN0, _bad, _bad)
  min0 = property(getMin, _bad, _bad)
  max0 = property(getMax, _bad, _bad)
  limits = property(getLimits, _bad, _bad)
