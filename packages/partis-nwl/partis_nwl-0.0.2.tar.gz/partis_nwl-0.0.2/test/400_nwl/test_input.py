import pytest

from pprint import pprint

from partis.nwl import (
  AnyInput,
  BaseInput,
  BoolInput,
  IntInput,
  FloatInput,
  StrInput,
  ListInput,
  StructInput,
  UnionInput,
  WorkFileInput,
  RunFileInput,
  WorkDirInput,
  RunDirInput )

from partis.schema import (
  SchemaError )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_int():
  d1 = IntInput(
    label = 'my_int',
    min = 0,
    max = 10,
    default_val = 2 )

  print(str(d1))
  print(d1.__dict__)
  # print(dir(d1))

  assert 'label' in d1
  assert d1.label == 'my_int'
  assert 'min' in d1
  assert d1.min == 0
  assert 'max' in d1
  assert d1.max == 10
  assert 'default_val' in d1
  assert d1.default_val == 2
  assert 'enabled' in d1
  assert 'visible' in d1

  doc = dumps(d1)

  print(doc)

  d2 = loads(doc, IntInput )

  print(str(d2))

  assert 'label' in d2
  assert 'min' in d2
  assert 'max' in d2
  assert 'default_val' in d2

  assert d2.label == d2['label'] and d2.label == d1.label
  assert d2.min == d2['min'] and d2.min == d1.min
  assert d2.max == d2['max'] and d2.max == d1.max
  assert d2.default_val == d2['default_val'] and d2.default_val == d1.default_val

  s2 = d2.value_schema( name = 'test' )

  print(str(s2))

  assert s2.min == d1.min
  assert s2.max == d1.max
  assert s2.default_val == d1.default_val

  assert s2.decode(None) == d1.default_val

  with pytest.raises(SchemaError):
    s2.decode(-1)

  with pytest.raises(SchemaError):
    s2.decode(11)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_float():
  d1 = FloatInput(
    label = 'my_float',
    min = 0.0,
    max = 10.0,
    default_val = 5.0 )

  assert 'label' in d1
  assert 'min' in d1
  assert 'max' in d1
  assert 'enabled' in d1
  assert 'visible' in d1
  assert 'default_val' in d1

  doc = dumps(d1)

  print(doc)

  d2 = loads(doc, FloatInput )

  assert 'label' in d2
  assert 'min' in d2
  assert 'max' in d2
  assert 'enabled' in d2
  assert 'visible' in d2
  assert 'default_val' in d2

  assert d2.label == d2['label'] and d2.label == d1.label
  assert d2.min == d2['min'] and d2.min == d1.min
  assert d2.max == d2['max'] and d2.max == d1.max
  assert d2.default_val == d2['default_val'] and d2.default_val == d1.default_val

  s2 = d2.value_schema( name = 'test' )

  assert s2.min == d1.min
  assert s2.max == d1.max
  assert s2.default_val == d1.default_val

  assert s2.decode(None) == d1.default_val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_struct():

  a1 = IntInput(
    label = 'my_int',
    min = 0,
    max = 10,
    default_val = 2 )

  b1 = FloatInput(
    label = 'my_float',
    min = 0.0,
    max = 10.0,
    default_val = 5.0 )

  d1 = StructInput(
    label = 'my_struct',
    struct = dict(
      a = a1,
      b = b1 ) )

  c1 = d1.value_schema( name = 'test' )

  doc = "a: 3"

  f = loads(doc, c1 )

  assert f.a == 3
  assert f.b == 5.0
