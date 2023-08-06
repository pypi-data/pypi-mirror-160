
import os
import re
import subprocess
import shutil
import shlex
from timeit import default_timer as timer

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  odict,
  adict,
  ModelHint,
  ModelError,
  LogListHandler )

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
  PJCEvaluated,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  PassPrim,
  StructValued,
  MapValued,
  SchemaError,
  SeqValued,
  schema_declared,
  SchemaModule )

from partis.schema.prim.any_prim import (
  any_prim_cases,
  AnyPrim )

from .log import (
  LogContext,
  LogEvent )

from .job import ToolJob
from .runtime import ToolRuntime

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolData( StructValued ):
  schema = dict(
    tag = 'data',
    doc = "Data",
    default_val = derived )

  # These schemas are place-holders that should be overwritten by the actual
  # tool schema, but needed here so that this schema can also be used to validate
  # a results file even without the tool definition
  inputs = MapPrim(
    doc = "Inputs",
    default_val = dict(),
    item = UnionPrim(
      cases = any_prim_cases ) )

  outputs = MapPrim(
    doc = "Outputs",
    default_val = dict(),
    item = UnionPrim(
      cases = any_prim_cases ) )

  commands = MapPrim(
    doc = "Commands",
    default_val = dict(),
    item = UnionPrim(
      cases = any_prim_cases ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolResults( StructValued ):
  schema = dict(
    tag = 'results',
    doc = "Results",
    default_val = derived )

  # placeholder for tool data schema
  data = ToolData

  job = ToolJob
  
  runtime = ToolRuntime
