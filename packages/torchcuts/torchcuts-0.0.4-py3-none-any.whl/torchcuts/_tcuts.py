"""Use TorchCuts to have quick and easy access to central content from
several relevant namespaces!"""

#  Copyright (c) 2022. Asger Jon Vistisen, All Rights Reserved.
from __future__ import annotations

from typing import NoReturn

import numpy
import torch


class TorchCuts:
  """Create an instance of this class with a convenient name. Then the
  instance will have access to the shortcuts as properties. For example:
  from torchcuts import Torchcuts

  tc = TorchCuts()

  N = 7
  X = torch.linspace(0, N-1, N)
  Now, TorchCuts alternatively provides:
  X = tc.Lin(0, N-1, N)
  Conveniently, TorchCuts include shortcuts pointing to other namespaces not
  included in PyTorch, but frequently used with PyTorch. For example, much
  content from numpy is provided for as well. In this case, the content from
  PyTorch has the beginning letter capitalized, whereas numpy content is all
  in lower case. For instance, tc.Oh(7, 7) creates a torch tensor with shape
  (7, 7), whereas tc.oh(7, 7) creates a numpy array filled with zeros. """

  Func = type(torch.zeros)

  def __init__(self) -> NoReturn:
    self._id = 'Thank you for using TorchCuts'

  def _bad(self, *_) -> NoReturn:
    """Raises type error when trying to delete/overwrite readonly
    variables"""
    raise TypeError('Tried to delete/overwrite readonly variable!')

  def _rand(self) -> Func:
    """Getter-function to rand"""
    return torch.rand

  def _roll(self) -> Func:
    """Getter-function to roll"""
    return torch.roll

  def _relu(self) -> Func:
    """Getter-function to relu"""
    return torch.nn.functional.relu

  def _heaviside(self) -> Func:
    """Getter-function to _heaviside"""
    return torch.heaviside

  def _new(self) -> Func:
    """Getter-function to tensor"""
    return torch.tensor

  def _cat(self) -> Func:
    """Getter-function to concatenate"""
    return torch.cat

  def _transpose(self) -> Func:
    """Getter-function to transpose"""
    return torch.transpose

  def _eye(self) -> Func:
    """Getter-function to eye"""
    return torch.eye

  def _ones(self) -> Func:
    """Getter-function to ones"""
    return torch.ones

  def _linspace(self) -> Func:
    """Getter-function to linspace"""
    return torch.linspace

  def _zeros(self) -> Func:
    """Getter-function to zeros"""
    return torch.zeros

  def _squeeze(self) -> Func:
    """Getter-function to squeeze"""
    return torch.squeeze

  def _unsqueeze(self) -> Func:
    """Getter-function to unsqueeze"""
    return torch.unsqueeze

  def _tile(self) -> Func:
    """Getter-function to tile"""
    return torch.tile

  def _bernoulli(self) -> Func:
    """Getter-function to bernoulli"""
    return torch.bernoulli

  def _abs(self) -> Func:
    """Getter-function to abs"""
    return torch.abs

  def _erf(self) -> Func:
    """Getter-function to erf"""
    return torch.erf

  def _exp(self) -> Func:
    """Getter-function to exp"""
    return torch.exp

  def _log(self) -> Func:
    """Getter-function to log"""
    return torch.log

  def _vdot(self) -> Func:
    """Getter-function to vdot"""
    return torch.vdot

  def _triu(self) -> Func:
    """Getter-function to triu"""
    return torch.triu

  def _tril(self) -> Func:
    """Getter-function to tril"""
    return torch.tril

  def _trace(self) -> Func:
    """Getter-function to trace"""
    return torch.trace

  def _flatten(self) -> Func:
    """Getter-function to flatten"""
    return torch.flatten

  def _sort(self) -> Func:
    """Getter-function to sort"""
    return torch.sort

  def _cos(self) -> Func:
    """Getter-function to cos"""
    return torch.cos

  def _sin(self) -> Func:
    """Getter-function to sin"""
    return torch.sin

  def _tan(self) -> Func:
    """Getter-function to tan"""
    return torch.tan

  def _cosh(self) -> Func:
    """Getter-function to cosh"""
    return torch.cosh

  def _sinh(self) -> Func:
    """Getter-function to sinh"""
    return torch.sinh

  def _tanh(self) -> Func:
    """Getter-function to tanh"""
    return torch.tanh

  def _acosh(self) -> Func:
    """Getter-function to acosh"""
    return torch.acosh

  def _asinh(self) -> Func:
    """Getter-function to asinh"""
    return torch.asinh

  def _atanh(self) -> Func:
    """Getter-function to atanh"""
    return torch.atanh

  def _acos(self) -> Func:
    """Getter-function to acos"""
    return torch.acos

  def _asin(self) -> Func:
    """Getter-function to asin"""
    return torch.asin

  def _atan(self) -> Func:
    """Getter-function to atan"""
    return torch.atan

  def _float32(self) -> Func:
    """Getter-function to float32"""
    return torch.float32

  def _float64(self) -> Func:
    """Getter-function to float64"""
    return torch.float64

  def _complex32(self) -> Func:
    """Getter-function to complex32"""
    return torch.complex32

  def _complex64(self) -> Func:
    """Getter-function to complex64"""
    return torch.complex64

  def _complex128(self) -> Func:
    """Getter-function to complex128"""
    return torch.complex128

  def _uint8(self) -> Func:
    """Getter-function to uint8"""
    return torch.uint8

  def _int8(self) -> Func:
    """Getter-function to int8"""
    return torch.int8

  def _int16(self) -> Func:
    """Getter-function to int16"""
    return torch.int16

  def _int32(self) -> Func:
    """Getter-function to int32"""
    return torch.int32

  def _long(self) -> Func:
    """Getter-function to long"""
    return torch.long

  def _bool(self) -> Func:
    """Getter-function to bool"""
    return torch.bool

  def _atan2(self) -> Func:
    """Getter-function for atan2"""
    return torch.atan2

  def _npeye(self) -> Func:
    """Getter-function to eye"""
    return numpy.eye

  def _npzeros(self) -> Func:
    """Getter-function to zeros"""
    return numpy.zeros

  def _npones(self) -> Func:
    """Getter-function to ones"""
    return numpy.ones

  def _npint8(self) -> Func:
    """Getter-function to int8"""
    return numpy.int8

  def _npint16(self) -> Func:
    """Getter-function to int16"""
    return numpy.int16

  def _npint32(self) -> Func:
    """Getter-function to int32"""
    return numpy.int32

  def _npint64(self) -> Func:
    """Getter-function to int64"""
    return numpy.int64

  def _npuint8(self) -> Func:
    """Getter-function to uint8"""
    return numpy.uint8

  def _npuint16(self) -> Func:
    """Getter-function to uint16"""
    return numpy.uint16

  def _npuint32(self) -> Func:
    """Getter-function to uint32"""
    return numpy.uint32

  def _npuint64(self) -> Func:
    """Getter-function to uint64"""
    return numpy.uint64

  def _npfloat16(self) -> Func:
    """Getter-function to float16"""
    return numpy.float16

  def _npfloat32(self) -> Func:
    """Getter-function to float32"""
    return numpy.float32

  def _npfloat64(self) -> Func:
    """Getter-function to float64"""
    return numpy.float64

  def _npcomplex64(self) -> Func:
    """Getter-function to complex64"""
    return numpy.complex64

  def _npcomplex128(self) -> Func:
    """Getter-function to complex128"""
    return numpy.complex128

  def _nparcsin(self) -> Func:
    """Getter-function to arcsin"""
    return numpy.arcsin

  def _nparccos(self) -> Func:
    """Getter-function to arccos"""
    return numpy.arccos

  def _nparctan(self) -> Func:
    """Getter-function to arctan"""
    return numpy.arctan

  def _nparctan2(self) -> Func:
    """Getter-function to arctan2"""
    return numpy.arctan2

  def _npsin(self) -> Func:
    """Getter-function to sin"""
    return numpy.sin

  def _npcos(self) -> Func:
    """Getter-function to cos"""
    return numpy.cos

  def _nptan(self) -> Func:
    """Getter-function to tan"""
    return numpy.tan

  def _npsinh(self) -> Func:
    """Getter-function to sinh"""
    return numpy.sinh

  def _npcosh(self) -> Func:
    """Getter-function to cosh"""
    return numpy.cosh

  def _nptanh(self) -> Func:
    """Getter-function to tanh"""
    return numpy.tanh

  def _nparcsinh(self) -> Func:
    """Getter-function to arcsinh"""
    return numpy.arcsinh

  def _nparccosh(self) -> Func:
    """Getter-function to arccosh"""
    return numpy.arccosh

  def _nparctanh(self) -> Func:
    """Getter-function to arctanh"""
    return numpy.arctanh

  i = property(_npeye, _bad, _bad)
  oh = property(_npzeros, _bad, _bad)
  j = property(_npones, _bad, _bad)
  i8 = property(_npint8, _bad, _bad)
  i16 = property(_npint16, _bad, _bad)
  i32 = property(_npint32, _bad, _bad)
  i64 = property(_npint64, _bad, _bad)
  ui8 = property(_npuint8, _bad, _bad)
  ui16 = property(_npuint16, _bad, _bad)
  ui32 = property(_npuint32, _bad, _bad)
  ui64 = property(_npuint64, _bad, _bad)
  f16 = property(_npfloat16, _bad, _bad)
  f32 = property(_npfloat32, _bad, _bad)
  f64 = property(_npfloat64, _bad, _bad)
  c64 = property(_npcomplex64, _bad, _bad)
  c128 = property(_npcomplex128, _bad, _bad)
  asin = property(_nparcsin, _bad, _bad)
  acos = property(_nparccos, _bad, _bad)
  atan = property(_nparctan, _bad, _bad)
  atan2 = property(_nparctan2, _bad, _bad)
  sin = property(_npsin, _bad, _bad)
  cos = property(_npcos, _bad, _bad)
  tan = property(_nptan, _bad, _bad)
  sinh = property(_npsinh, _bad, _bad)
  cosh = property(_npcosh, _bad, _bad)
  tanh = property(_nptanh, _bad, _bad)
  asinh = property(_nparcsinh, _bad, _bad)
  acosh = property(_nparccosh, _bad, _bad)
  atanh = property(_nparctanh, _bad, _bad)
  Dot = property(_vdot, _bad, _bad)
  Triu = property(_triu, _bad, _bad)
  Tril = property(_tril, _bad, _bad)
  Tr = property(_trace, _bad, _bad)
  Flat = property(_flatten, _bad, _bad)
  Sort = property(_sort, _bad, _bad)
  Cos = property(_cos, _bad, _bad)
  Sin = property(_sin, _bad, _bad)
  Tan = property(_tan, _bad, _bad)
  Cosh = property(_cosh, _bad, _bad)
  Sinh = property(_sinh, _bad, _bad)
  Tanh = property(_tanh, _bad, _bad)
  Acosh = property(_acosh, _bad, _bad)
  Asinh = property(_asinh, _bad, _bad)
  Atanh = property(_atanh, _bad, _bad)
  Acos = property(_acos, _bad, _bad)
  Asin = property(_asin, _bad, _bad)
  Atan = property(_atan, _bad, _bad)
  Atan2 = property(_atan2, _bad, _bad)
  F32 = property(_float32, _bad, _bad)
  F64 = property(_float64, _bad, _bad)
  C32 = property(_complex32, _bad, _bad)
  C64 = property(_complex64, _bad, _bad)
  C128 = property(_complex128, _bad, _bad)
  Ui8 = property(_uint8, _bad, _bad)
  I8 = property(_int8, _bad, _bad)
  I16 = property(_int16, _bad, _bad)
  I32 = property(_int32, _bad, _bad)
  I64 = property(_long, _bad, _bad)
  Bool = property(_bool, _bad, _bad)
  Log = property(_log, _bad, _bad)
  Exp = property(_exp, _bad, _bad)
  Erf = property(_erf, _bad, _bad)
  Abs = property(_abs, _bad, _bad)
  Coin = property(_bernoulli, _bad, _bad)
  Tile = property(_tile, _bad, _bad)
  Sq = property(_squeeze, _bad, _bad)
  Un = property(_unsqueeze, _bad, _bad)
  Rand = property(_rand, _bad, _bad)
  Roll = property(_roll, _bad, _bad)
  Relu = property(_relu, _bad, _bad)
  H = property(_heaviside, _bad, _bad)
  New = property(_new, _bad, _bad)
  Cat = property(_cat, _bad, _bad)
  T = property(_transpose, _bad, _bad)
  I = property(_eye, _bad, _bad)
  J = property(_ones, _bad, _bad)
  Lin = property(_linspace, _bad, _bad)
  Oh = property(_zeros, _bad, _bad)
