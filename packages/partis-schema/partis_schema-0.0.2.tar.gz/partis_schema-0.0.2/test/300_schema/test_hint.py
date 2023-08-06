import pytest

from partis.schema import (
  SchemaError,
  Hint )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_hint():
  for lvl in [ "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" ]:

    hint = Hint(
      msg = "test message",
      loc = "from somewhere",
      level = lvl,
      hints = [
        dict(
          msg = "another message",
          loc = "from somewhere else",
          level = lvl ),
        None ] )

    _hint = hint._cast()
    assert( _hint.msg == "test message" )
    assert( _hint.loc == "from somewhere" )
    assert( _hint.level == lvl )
    assert( len(_hint.hints) == 1 )
    assert( _hint.hints[0].msg == "another message" )
    assert( _hint.hints[0].loc == "from somewhere else" )
    assert( _hint.hints[0].level == lvl )

    s = _hint.fmt()

    assert( s.startswith( "test message" ) )
