
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

from .log import (
  LogContext,
  LogEvent )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolJob( StructValued ):
  schema = dict(
    tag = 'job',
    doc = "Tool job information",
    default_val = derived )

  id = StrPrim(
    doc = "The job id assigned when tool was run, if any.",
    default_val = "",
    max_lines = 1 )

  name = StrPrim(
    doc = "The job name assigned when tool was run, if any.",
    default_val = "",
    max_lines = 1 )

  tool_qualname = StrPrim(
    doc = "Qualified name of tool that produced the results",
    default_val = '',
    max_lines = 1 )

  host = StrPrim(
    doc = "The name of the host where the job was submitted, if any.",
    default_val = "",
    max_lines = 1 )

  user = StrPrim(
    doc = "The user under which the job was run, if any.",
    default_val = "",
    max_lines = 1 )

  curdir = StrPrim(
    doc = "Directory from which the tool was started.",
    default_val = "",
    max_lines = 1 )

  args = SeqPrim(
    doc = "Command line arguments used to run tool, if any",
    item = StrPrim(
      max_lines = 1 ),
    default_val = list() )

  mpiexec = SeqPrim(
    doc = """List of raw arguments to execute a program within MPI, if available.
      """,
    item = StrPrim(
      max_lines = 1 ),
    default_val = list() )
