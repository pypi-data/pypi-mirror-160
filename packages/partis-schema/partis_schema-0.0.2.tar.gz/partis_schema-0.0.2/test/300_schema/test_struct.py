import pytest

from pprint import pprint

import itertools

from partis.schema import (
  required,
  optional,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  StructValued,
  PJCEvaluated,
  SchemaError,
  is_bool,
  is_numeric,
  is_string,
  is_sequence,
  is_mapping,
  is_schema_prim,
  is_schema_struct,
  is_schema,
  is_schema_struct_valued,
  any_schema,
  SchemaDefinitionError )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_schema():

  # test using metaclass arguments
  class MyType1( StructValued,
    tag = 'my_type',
    struct = [
      ( 'a', BoolPrim() ),
      ( 'b', IntPrim() ),
      ( 'c', FloatPrim() ),
      ( 'd', StrPrim() ),
      ( 'e', SeqPrim(
        item = StrPrim() ) ),
      ( 'f', MapPrim(
        item = StrPrim() ) )  ] ):
    pass

  # test using class namespace arguments
  class MyType2( StructValued ):
    schema = dict(
      tag = 'my_type' )

    a = BoolPrim()
    b = IntPrim()
    c = FloatPrim()
    d = StrPrim()
    e =  SeqPrim(
      item = StrPrim() )

    f = MapPrim(
      item = StrPrim() )

  doc_yaml = """{ type: my_type, a: True, b: 1, c: 1.0, d: "one", e: ["x", "y", "z"], f: { q: q, r: r} }"""

  for cls in [ MyType1, MyType2 ]:
    obj = loads( doc_yaml, cls )

    assert isinstance( obj, cls )
    assert obj._schema is cls.schema
    assert obj._schema.tag == 'my_type'
    assert obj.a == True
    assert obj.b == 1
    assert obj.c == 1.0
    assert obj.d == "one"
    assert obj.e == ["x", "y", "z"]
    assert obj.f == { "q": "q", "r": "r"}

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_struct_proxy():

  # test using metaclass arguments
  class MyType1( StructValued,
    tag = 'my_type',
    struct_proxy = 'a',
    struct = [
      ( 'a', BoolPrim() ),
      ( 'b', IntPrim( default_val = 1 ) ) ] ):
    pass

  x = MyType1( True )

  assert x.a == True
  assert x.b == 1

  with pytest.raises( SchemaDefinitionError ):
    # should raise error because struct_proxy conflicts with union
    u = UnionPrim(
      cases = [
        MyType1,
        BoolPrim() ] )
