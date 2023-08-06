
from copy import copy

from collections.abc import (
  Mapping )

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  adict,
  odict )

from partis.schema_meta.base import (
  SchemaError,
  SchemaNameError,
  SchemaDeclaredError,
  SchemaDefinitionError,
  SchemaValidationError,
  SchemaHint,
  Loc,
  assert_valid_name,
  is_notset,
  is_valued,
  is_evaluated,
  is_mapping,
  is_derived,
  is_optional,
  is_required,
  is_valued_type,
  is_schema_declared,
  is_schema_struct )

from partis.schema_meta.struct import (
  SchemaStructProxy )

from partis.schema_meta.valued import (
  ValuedMeta )

from partis.schema import (
  EvaluatedContext )

from .valued import (
  Valued,
  get_schema_loc,
  get_init_val,
  get_src_val )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StructValuedMeta( ValuedMeta, SchemaStructProxy ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def extract_val_loc( args, kwargs ):

  if len(args) == 0:
    val = None
    loc = None
  else:
    if len(args) == 1:
      val = args[0]
      loc = None
    elif len(args) == 2:
      val, loc = args
    else:
      raise ValueError(
        f"positional arguments must be at most `(val, loc)`."
        " All keyword arguments are interpreted as items of `val`")

  if kwargs:
    if val:
      val = {**val, **kwargs}
    else:
      val = kwargs

  return val, loc

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class StructValued( Valued, Mapping, metaclass = StructValuedMeta ):
  """Container for fully or partially evaluated fixed mapping data.

  .. note::

    The terminology of 'struct' is used to indicate that the allowed key-value
    pairs of the value are fixed, such that keys may not be added or removed
    dynamically.
    However, key-values may be heterogenous, with a unique schema defined for
    each key, unlike the generic MapValue that specifies the same schema for
    all keys.

  Parameters
  ----------
  val : NoneType | object
    Source data used to initialize values
  loc : NoneType | :class:`Loc <partis.schema_meta.base.Loc>`
    Location information of source data (E.G. file, line/column number)

  Raises
  ------
  SchemaValidationError
    If the value is not valid
  """

  #-----------------------------------------------------------------------------
  def __new__( cls,
    *args, **kwargs ):

    val, loc = extract_val_loc( args, kwargs )

    if is_valued_type( val ) or is_evaluated( val ):
      if loc is None:
        loc = val._loc

      # NOTE: must still validate value since there are no gaurantees about
      # the original schema
      val = val._encode

    if loc is None:
      loc = Loc()

    if not isinstance( loc, Loc ):
      raise SchemaValidationError(
        f"`loc` must be instance of `Loc`: {type(loc)}")

    if is_optional(val):
      val = cls.schema.default_val

      if is_required( val ):
        raise SchemaValidationError(
          f"Value is required",
          loc = loc,
          hints = cls.schema.hints )

      elif is_optional( val ):
        return None

    valued = True

    if cls.schema.evaluated.check( val ):
      valued = False

      val = cls.schema.evaluated(
        schema = cls.schema,
        src = val,
        loc = loc )

    self = super().__new__( cls )

    self._p_dict = odict()
    self._p_loc = loc
    self._p_valued = valued
    self._p_src = val

    return self

  #-----------------------------------------------------------------------------
  def __init__( self,
    *args, **kwargs ):

    val, loc = extract_val_loc( args, kwargs )

    # these are set by the __new__ method
    if not self._valued:
      return

    val = self._src
    loc = self._loc

    tag_key = self._schema.tag_key
    tag = self._schema.tag

    self._p_dict[tag_key] = tag

    loc = self._loc

    if not is_mapping( val ):
      if self._schema.struct_proxy:
        # uses source data for primary struct key value with remaining defaults

        _val = dict()
        _val[ self._schema.struct_proxy ] = val
        val = _val

      else:
        raise SchemaValidationError(
          f"`val` must be a mapping: {val}",
          loc = loc )

    all_keys = set(self._schema.struct.keys()) | set(val.keys())

    _locs = {
      k : loc( val, k )
      for k in all_keys }

    if tag_key in val:
      _tag = val[tag_key]

      if _tag != tag:
        log.warning(f"schema {self._schema.__module__}.{self._schema.__name__} expected `{tag_key}` of `{tag}`: `{_tag}`, {loc}")

    _keys = list(self._schema.struct.keys())

    for k in val.keys():

      if k not in _keys and k != tag_key:
        # issue warnings for unexpected keys
        log.warning(f"not in schema {self._schema.__module__}.{self._schema.__name__}: '{k}', {_locs[k]}")


    for k, _schema in self._schema.struct.items():
      _schema = _schema.schema

      # decode data according to schema
      _val = None
      _loc = _locs[k]

      if k in val:
        _val = val[k]

      try:
        _val = _schema.decode(
          val = _val,
          loc = _loc )

      except SchemaError as e:

        raise SchemaValidationError(
          f"Schema item `{k}` could not be decoded",
          loc = _loc,
          hints = SchemaHint.cast( e ) ) from e

      if _val is not None and not is_valued(_val):
        self._p_valued = False

      self._p_dict[k] = _val

  #-----------------------------------------------------------------------------
  @property
  def _valued( self ):
    """bool : False if any item is not fully evaluated. True otherwise.
    """
    return self._p_valued

  #-----------------------------------------------------------------------------
  @property
  def _src( self ):
    return self._p_src

  #-----------------------------------------------------------------------------
  @property
  def _loc( self ):
    """:class:`Loc <partis.schema_meta.base.Loc>` : Location information of source
    data (E.G. file, line/column number)
    """
    return self._p_loc

  #-----------------------------------------------------------------------------
  @property
  def _schema( self ):
    """:class:`SchemaStruct <partis.schema.struct.SchemaStruct>` :  Schema class
    of this instance
    """
    return type(self).schema

  #-----------------------------------------------------------------------------
  @property
  def _encode( self ):
    """dict : Plain-data values of items.
    """
    if is_evaluated( self._src ):
      return self._src._encode

    val = odict()

    val[ self._schema.tag_key ] = self._schema.tag

    for k, _schema in self._schema.struct.items():
      _schema = _schema.schema

      _val = self._p_dict[k]

      if is_valued_type( _val ) or is_evaluated( _val ):
        _val = _val._encode

      if _val is not None:
        if is_mapping( _val ) and is_schema_struct( _schema ):
          # don't need to store tag key since schema is not ambiguous
          _val.pop( _schema.tag_key )

        val[k] = _val

    return val


  #-----------------------------------------------------------------------------
  def __str__( self ):
    # return self._p_dict.__str__( )
    return f"{type(self).__name__}({list(self._p_dict.items())})"

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    # return self._p_dict.__repr__( )
    return f"{type(self).__name__}({list(self._p_dict.items())})"


  #-----------------------------------------------------------------------------
  def __len__( self ):
    return len(self._p_dict)

  #-----------------------------------------------------------------------------
  def __iter__( self ):
    return iter(self._p_dict)

  #-----------------------------------------------------------------------------
  def keys( self ):
    return self._p_dict.keys()

  #-----------------------------------------------------------------------------
  def values( self ):
    return self._p_dict.values()

  #-----------------------------------------------------------------------------
  def items( self ):
    return self._p_dict.items()

  #-----------------------------------------------------------------------------
  def get( self, key, default = None ):
    return self._p_dict.get( key, default )


  # #-----------------------------------------------------------------------------
  # def __getattribute__( self, name ):
  #
  #   try:
  #     return super().__getattribute__(name)
  #
  #   except AttributeError as e:
  #
  #     if name in self._p_dict:
  #       return self._p_dict[name]
  #
  #     raise AttributeError(
  #       f"'{type(self).__name__}' object has no attribute '{name}'") from e
  #
  # #-----------------------------------------------------------------------------
  # def __setattr__( self, name, val ):
  #   if name in self._schema.struct or name == self._schema.tag_key:
  #     self[name] = val
  #     return
  #
  #   if not name.startswith('_'):
  #     raise AttributeError(f"Cannot assign new exposed attribute: {name}")
  #
  #   super().__setattr__( name, val )

  #-----------------------------------------------------------------------------
  def __iter__( self ):
    return iter(self._p_dict)

  #-----------------------------------------------------------------------------
  def __copy__( self ):

    obj = type(self)( self._p_dict, self._loc )

    return obj

  #-----------------------------------------------------------------------------
  def __getitem__( self, key ):
    if key == self._schema.tag_key:
      return self._schema.tag

    if key not in self._schema.struct:
      raise KeyError(
        f"Schema does not contain key: {key}")

    return self._p_dict[key]

  #-----------------------------------------------------------------------------
  def __setitem__( self, key, val ):

    loc = None

    if is_valued_type( val ):
      loc = val._loc

    tag_key = self._schema.tag_key

    if key == tag_key:
      if val != self._schema.tag:
        raise SchemaValidationError(f"Schema value for`{tag_key}` must be `{self._schema.tag}`: {val}")

    else:

      if key not in self._schema.struct:
        raise SchemaValidationError(f"Schema does not contain key: {key}")

      try:
        val = self._schema.struct[key].schema.decode(
          val = val,
          loc = loc )

      except SchemaError as e:
        raise SchemaValidationError(
          f"value error for key `{key}`",
          hints = [
            SchemaHint("value", hints = val),
            SchemaHint.cast( e ) ] ) from e


      self._p_dict[ key ] = val


  #-----------------------------------------------------------------------------
  def _lint( self,
    context = None,
    logger = None ):
    """Lints source

    Parameters
    ----------
    context : None | :class:`EvaluatedContext` | list[ :class:`EvaluatedContext` ]
      Sets the context for which this expression is to be evaluated.
      The expression is evaluated only when the specified context is equivalent
      to the one for this evaluated class.
    logger : logging.Logger
      A logger object to direct expression logs/prints instead of stdout

    Returns
    -------
    : list[SchemaHint]

    See Also
    --------
    :class:`Evaluated <partis.schema.eval.Evaluated>`
    """

    hints = list()

    if self._valued:
      return hints

    # must evaluate to get value

    if is_evaluated( self._p_src ):

      hints.extend( self._p_src._lint(
        context = context,
        logger = logger ) )

      return hints

    # local variables for items in list or dictionary
    # NOTE: parent of items is the current value, parent of current will be
    # parent of the item parent

    for k, schema in self._schema.struct.items():
      v = self[k]

      if not is_valued(v):

        if isinstance( context, EvaluatedContext ):
          _context = context(
            schema = self._schema,
            parent = self,
            key = k )

        else:
          _context = context

        hints.extend(  v._lint(
          context = _context,
          logger = logger ) )

    if hints:
      return [
        SchemaHint(
          loc = Loc(
            path = self._loc.path,
            line = self._loc.line,
            col = self._loc.col ),
          hints = hints ) ]

    return hints

  #-----------------------------------------------------------------------------
  def _eval( self,
    context = None,
    logger = None ):
    """Evaluates source

    Parameters
    ----------
    context : None | :class:`EvaluatedContext` | list[ :class:`EvaluatedContext` ]
      Sets the context for which this expression is to be evaluated.
      The expression is evaluated only when the specified context is equivalent
      to the one for this evaluated class.
    logger : logging.Logger
      A logger object to direct expression logs/prints instead of stdout

    Returns
    -------
    value : :class:`SchemaStruct <partis.schema.struct.SchemaStruct>`
      Decoded value resulting from evaluation.
      If there are no un-evaluated values, then will return a shallow copy of
      the current data.

    See Also
    --------
    :class:`Evaluated <partis.schema.eval.Evaluated>`
    """

    if self._valued:
      return copy(self)

    # must evaluate to get value

    if is_evaluated( self._p_src ):

      return self._p_src._eval(
        context = context,
        logger = logger )

    # local variables for items in list or dictionary
    # NOTE: parent of items is the current value, parent of current will be
    # parent of the item parent
    val = adict()

    for k, schema in self._schema.struct.items():
      v = self[k]

      if is_valued(v):
        val[k] = v

      else:
        if isinstance( context, EvaluatedContext ):
          _context = context(
            schema = self._schema,
            parent = val,
            key = k )

        else:
          _context = context

        val[k] = v._eval(
          context = _context,
          logger = logger )

    return type(self)( val, self._loc )

  #-----------------------------------------------------------------------------
  def on_child_key_changed( self, key, new_key ):
    pass
