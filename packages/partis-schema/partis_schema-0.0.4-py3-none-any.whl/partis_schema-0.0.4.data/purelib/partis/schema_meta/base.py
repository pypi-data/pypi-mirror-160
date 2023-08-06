import re
import logging
log = logging.getLogger(__name__)

from collections.abc import (
  Mapping,
  Sequence )

from numbers import (
  Number,
  Complex,
  Real,
  Integral )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from partis.utils.special import (
  SpecialType,
  RequiredType,
  OptionalType,
  DerivedType,
  NotSetType )

from partis.utils import (
  Loc,
  ModelHint,
  ModelError )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import partis


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
name_re = r"^[a-zA-Z\_][a-zA-Z\_0-9]*$"
name_cre = re.compile( name_re )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaError( ModelError ):
  """Base of all schema related errors
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaNameError( SchemaError ):
  """Raised when a name error occurs
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaParseError( SchemaError ):
  """Raised when a schema cannot be detected
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaDetectionError( SchemaError ):
  """Raised when a schema cannot be detected
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaDeclaredError( SchemaError ):
  """Raised when a schema's declared is used before the schema has been defined
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaDefinitionError( SchemaError ):
  """Raised when a schema's definition is not correctly specified
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaValidationError( SchemaError ):
  """Raised when data could not be validated (encoded/decoded) using schema definition
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaEvaluationError( SchemaError ):
  """Raised when evaluated expression failed to result in a decoded value
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaHint( ModelHint ):
  """Base of all schema hints
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def assert_valid_name( name ):
  if not isinstance( name, str ):
    raise SchemaNameError(
      f"Name must be a string: {name}")

  match = name_cre.fullmatch(name)

  if match is None:
    raise SchemaNameError(
      f"Name must be only alpha-numeric or underscrores, and not start with a number: {name}")


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def assert_valid_path( path ):

  if isinstance( path, str ):
    if path == '':
      # empty path is valid
      return

    path = path.split('.')

  if not isinstance( path, list ) and all( isinstance(p, str) for p in path ):
    raise SchemaNameError(
      f"Name path must be a string or list of strings: {path}")

  for i, name in enumerate(path):
    try:

      assert_valid_name( name )

    except SchemaNameError as e:
      raise SchemaNameError(
        f"Path name segment {i} not valid: {path}",
        hints = SchemaHint.cast( e ) ) from e


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_special( val ):
  return isinstance( val, SpecialType )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_required( val ):
  """
  Returns
  -------
  bool
    True if the value corresponds to being required, likely resulting in
    an error if no value is supplied.
  """

  return isinstance( val, RequiredType )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_optional( val ):
  """
  Returns
  -------
  bool
    True if the value corresponds to being optional, resulting in a default of None
  """
  return val is None or isinstance( val, OptionalType )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_derived( val ):
  """
  Returns
  -------
  bool
    True if the value is to be derived from some other value(s)
  """
  return isinstance( val, DerivedType )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_notset( val ):
  """
  Returns
  -------
  bool
    True if the value corresponds to being not set, or otherwise undefined,
    including not even ``None``.
  """

  return isinstance( val, NotSetType )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_bool( obj ):
  """Is a boolean value
  """

  if isinstance( obj, type ):
    return issubclass( obj, bool ) or issubclass( obj, partis.schema.valued.BoolValued )

  return isinstance( obj, bool ) or isinstance( obj, partis.schema.valued.BoolValued )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_numeric( obj ):
  """Is a numeric value
  """

  if isinstance( obj, type ):
    return issubclass( obj, Number ) and not is_bool( obj )

  return isinstance( obj, Number ) and not is_bool( obj )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_string( obj ):
  """Is a string value
  """

  if isinstance( obj, type ):
    return issubclass( obj, str )

  return isinstance( obj, str )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_sequence( obj ):
  """Is a sequence value, but not a string
  """
  if isinstance( obj, type ):
    return issubclass( obj, Sequence ) and not is_string( obj )

  return isinstance( obj, Sequence ) and not is_string( obj )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_mapping( obj ):
  """Is a mapping value
  """
  if isinstance( obj, type ):
    return issubclass( obj, Mapping )

  return isinstance( obj, Mapping )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
type_tests = [
  is_required,
  is_derived,
  is_optional,
  is_bool,
  is_numeric,
  is_string,
  is_sequence,
  is_mapping ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_similar_value_type( a, b ):
  """
  Returns
  -------
  is_similar_value_type : bool
    True if all `type_tests` return the same for both values
  """
  return all( f(a) == f(b) for f in type_tests )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_schema( obj ):
  """Is a schema class or schema declared
  """
  return issubclass( type(obj), partis.schema_meta.schema.SchemaRef )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_schema_prim( obj ):
  """Is a schema primitive type
  """
  return issubclass( type(type(obj)), partis.schema_meta.prim.SchemaPrimMeta )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_schema_declared( obj ):
  """Is a schema class or schema declared type
  """
  return issubclass( type(obj), partis.schema_meta.schema.SchemaDeclared )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_schema_struct( obj ):
  """Is a schema class or schema declared type
  """
  return (
    issubclass( type(obj), partis.schema_meta.struct.SchemaStruct )
    or issubclass( type(obj), partis.schema_meta.struct.SchemaStructDeclared )
    or issubclass( type(obj), partis.schema_meta.struct.SchemaStructProxy ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_schema_struct_valued( obj ):
  """Is an instance value of a schema class type
  """
  return (
    is_valued_type( obj )
    and is_schema_struct(obj._schema) )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_evaluated_class( val ):
  """Is an evaluated class type
  """
  return ( issubclass( type(val), partis.schema_meta.eval.EvaluatedMeta ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_provider( val ):
  """Is an evaluated type
  """
  return issubclass( type(type(val)), partis.schema_meta.eval.ProviderMeta )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_evaluated( val ):
  """Is an evaluated type
  """
  return issubclass( type(type(val)), partis.schema_meta.eval.EvaluatedMeta )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_valued_type( val ):
  """
  Returns
  -------
  is_valued_type : bool
    True if is an instance value of any schema type
  """
  return issubclass( type(type(val)), partis.schema_meta.valued.ValuedMeta )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def any_schema( val, schemas ):
  """Is the schema any of the list schemas

  Parameters
  ----------
  schema : object
    Schema to test
  schema : list[object]
    Schemas to compare to
  """
  if is_valued_type( val ):
    return any( val._schema is s.schema for s in schemas )

  elif is_schema( val ):
    return any( val.schema is s.schema for s in schemas )

  return False


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_valued( val ):
  """
  Returns
  -------
  is_valued : bool
    True if value is completely evaluated
  """

  if is_evaluated(val):
    return False

  if is_valued_type( val ):
    return val._valued

  if is_sequence( val ):
    return all( is_valued(v) for v in val )

  if is_mapping( val ):
    return all( is_valued(v) for v in val.values() )

  return True
