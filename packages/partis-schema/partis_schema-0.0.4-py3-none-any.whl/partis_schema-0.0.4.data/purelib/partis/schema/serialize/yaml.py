# -*- coding: UTF-8 -*-
from collections import OrderedDict as odict
from copy import copy
from abc import ABCMeta
import itertools
import re
import uuid

from abc import ABCMeta

import logging
log = logging.getLogger(__name__)

import ruamel.yaml

from ruamel.yaml.comments import (
  CommentedMap,
  CommentedOrderedMap,
  CommentedKeySeq,
  CommentedSeq )

from ruamel.yaml.scalarstring import LiteralScalarString

from partis.schema_meta.base import (
  Loc,
  SchemaHint,
  SchemaError,
  SchemaParseError,
  SchemaDetectionError,
  is_valued_type,
  is_evaluated,
  is_string,
  is_mapping,
  is_sequence )

from partis.schema.plugin import (
  schema_plugins )

from .utils import (
  as_load,
  as_dump )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dump_prep( val ):
  """Prepares value to be dumped, converting to ruamel datastructures
  """

  if is_valued_type( val ) or is_evaluated( val ):
    val = val._encode

  if is_mapping( val ):
    _val = CommentedMap()

    for k, v in val.items():
      _val[k] = dump_prep( v )

  elif is_sequence( val ):
    _val = CommentedSeq()

    for v in val:
      _val.append( dump_prep( v ) )

  elif is_string( val ) and len(val.splitlines()) > 1:
    _val = LiteralScalarString(val)

  else:
    _val = val

  return _val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def loads(
  src,
  schema = None,
  loc = None,
  detect_schema = False ):
  """
  Parse the first YAML source in a stream
  and produce the corresponding Python object.

  Parameters
  ----------
  src : str
  schema : :class:`Schema <partis.schema.struct.SchemaStruct>` | :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>`
  loc : None | :class:`Loc <partis.schema_meta.base.Loc>`
    Location information of source data (E.G. file, line/column number)
  detect_schema : bool
    If true, attempts to find the schema to use from available plugins by the
    `schema_hash` stored in a top-level ``__schema_hash__`` key.
    If the top level source is not a mapping, or if ``__schema_hash__`` is not
    present, or if the has is not discovered, and ``schema`` (the default)
    is not given, this will raise an error.

  Returns
  -------
  val : object | :class:`Schema <partis.schema.valued.Valued>`
  """

  if loc is None:
    loc = Loc()

  if isinstance( loc, str ):
    loc = Loc( filename = loc )

  try:
    val = ruamel.yaml.round_trip_load( src )

  except BaseException as e:
    raise SchemaParseError(
      f"source failed parsing",
      loc = loc,
      hints = SchemaHint.cast( e ) ) from e

  schema_hash = ''

  if is_mapping( val ) and '__schema_hash__' in val:
    schema_hash = val.pop('__schema_hash__')

  if detect_schema:

    if schema_hash:
      _schemas = schema_plugins.get_by_hash( schema_hash )

      if len(_schemas) > 0:
        schema = _schemas[0]

    if schema is None:
      raise SchemaDetectionError(
        f'Schema could not be detected' )

  if schema is None:
    return val

  loc = loc(val)

  return schema.schema.decode(
    val = val,
    loc = loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dumps(
  val,
  add_hash = False ):
  """Serializes a suitable Python object into a YAML source string

  Parameters
  ----------
  val : object | :class:`Schema <partis.schema.valued.Valued>`

  Returns
  -------
  src : str
  """

  schema = None

  if hasattr( val, '_schema'):
    schema = val._schema

  val = dump_prep( val )

  if add_hash and schema and is_mapping( val ):
    val['__schema_hash__'] = schema.schema_hash

  return ruamel.yaml.round_trip_dump( val,
    # default_style = "|",
    default_flow_style = False,
    allow_unicode = True )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
load = as_load( loads )
dump = as_dump( dumps )
