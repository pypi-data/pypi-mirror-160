
import os
import subprocess
import shutil
from timeit import default_timer as timer

import logging
log = logging.getLogger(__name__)

from partis.schema import (
  required,
  optional,
  derived,
  is_sequence,
  is_mapping,
  is_evaluated,
  is_valued,
  is_valued_type,
  is_optional,
  PyEvaluated,
  CheetahEvaluated,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  StructValued,
  schema_declared,
  EvaluatedContext )

from partis.utils import (
  ModelHint,
  HINT_LEVELS_DESC,
  indent_lines )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
hint_declared = schema_declared( tag = 'hint' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
HintList = SeqPrim(
  doc = "List of hints",
  item = hint_declared,
  default_val = list() )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Hint( StructValued ):
  """A schema for serializing ModelHints
  """

  schema = dict(
    declared = hint_declared,
    default_val = optional,
    struct_proxy = 'msg' )

  level = StrPrim(
    char_case = 'upper',
    default_val = "INFO",
    restricted = [ k.upper() for k,v in HINT_LEVELS_DESC.items() ],
    doc = "\n".join([ f"- ``'{k.upper()}'``: {indent_lines(2, v, start = 1)}" for k,v in HINT_LEVELS_DESC.items() ]) )

  msg = StrPrim(
    doc = "Message",
    default_val = "" )

  loc = StrPrim(
    doc = "Referenced location",
    default_val = "",
    max_lines = 1 )

  hints = HintList

  #-----------------------------------------------------------------------------
  def _cast( self ):
    """Converts instance of this to instance of a regular ModelHint

    Returns
    :class:`ModelHint <partis.utils.hint.ModelHint>`
    """
    return ModelHint(
      self.msg,
      loc = self.loc,
      level = self.level,
      hints = [ h._cast() if h is not None else None for h in self.hints ] )
