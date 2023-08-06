"""Filters"""
#  Copyright (c) 2022. Asger Jon Vistisen All Rights Reserved.

from torchcuts import *
import torch


class Filter:
  """Instances of Filter are created on the basis of a given filter base.
  Calling an instance on a tensor"""

  eps = 1e-08

  @staticmethod
  def ensureTensor(X: Tensor | list) -> Tensor:
    """This static method returns a tensor, if X is a list. Otherwise,
    it simply returns X back."""
    return X if isinstance(X, Tensor) else torch.tensor(X).to(Float32)

  def __init__(self, X0: Tensor | list, ) -> NoReturn:
    self._X0, _ = torch.sort(self.ensureTensor(X0).view(-1))

  def __call__(self, X: Tensor | list) -> Tensor:
    """Calling an instance returns a one-hot tensor."""
    X = self.ensureTensor(X)
    outShape = [self.N0, *[i for i in X.shape]]
    X = X.view(1, -1)
    XE = J(self.N0, 1) @ X
    X0E, N = self.X0 @ J(X.shape), X.view(-1).shape[0]
    linds = Lin(0, N - 1, N).view(-1).to(torch.long)
    inds = torch.argmin(torch.cosh(XE - X0E), dim=0).view(-1).to(torch.long)
    out = Oh(self.N0, N)
    out[inds, linds] = 1
    return out.view(outShape)

    # return torch.argmin(torch.cosh(XE - X0E), dim=0)
    #
    # E0 = J([1, ] + [i for i in self.X0.shape])
    # E = J([self.N0, ] + [1 for _ in self.X0.shape])
    # X0E = self.X0 @ E0
    # XE = E @ torch.transpose(X, 0, 1)
    # top = self.max0 + Filter.eps
    # bottom = self.min0 - Filter.eps
    # xLow = torch.roll(X0E, 1, 0)  # smaller
    # xHigh = torch.roll(X0E, -1, 0)  # larger
    # xLow[0] = bottom
    # xLow[-1] = top
    # xHigh[0] = bottom
    # xHigh[-1] = top
    # out = ((xHigh - XE) > 0).to(Float32) - ((xLow - XE) > 0).to(Float32)
    # torch.argmin(torch.cosh(X - self.X0), 0, )

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
