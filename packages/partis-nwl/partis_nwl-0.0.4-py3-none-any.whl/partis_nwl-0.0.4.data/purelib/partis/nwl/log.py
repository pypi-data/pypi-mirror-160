
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

from .context import (
  LogContext )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
EvaluatedLogs = PyEvaluated.subclass(
  context = LogContext )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LogEvent( StructValued ):
  """A logging event specified from within an NWL definition
  """

  schema = dict(
    tag = 'log',
    default_val = optional,
    evaluated = EvaluatedLogs,
    struct_proxy = 'msg' )

  level = StrPrim(
    doc = "Level name of the logging event.",
    char_case = 'upper',
    default_val = "INFO",
    restricted = [ "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" ] )

  msg = StrPrim(
    doc = "The log event description message",
    default_val = "",
    evaluated = EvaluatedLogs )

  enabled = BoolPrim(
    doc = "Flag if the log event did or would occur",
    default_val = True,
    evaluated = EvaluatedLogs )
