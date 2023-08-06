
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

from partis.schema.hint import (
  Hint,
  HintList )

from .allocation import RunAllocation

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolRuntime( RunAllocation ):
  schema = dict(
    tag = 'runtime',
    doc = "Tool runtime information",
    default_val = derived )

  success = BoolPrim(
    doc = "Flag for whether the tool ran and closed successfully",
    default_val = False )

  workdir = StrPrim(
    doc = "Directory from which the tool resolves relative input file paths.",
    default_val = "",
    max_lines = 1 )

  host = StrPrim(
    doc = """The local `hostname` or fully qualified domain name
    of the machine where the tool was run.

    .. note::

      If the tool was run with more than one allocated node, this will
      be the hostname of only the node on which the run script was executed.""",
    default_val = "",
    max_lines = 1 )

  nodes = SeqPrim(
    doc = """List of hostnames that are allocated for running multiple processes
      """,
    item = StrPrim(
      max_lines = 1 ),
    default_val = list() )

  threads_per_process = IntPrim(
    doc = """Maximum number of logical threads.

    Computed as ``threads_per_process = threads_per_cpu * cpus_per_process``""",
    min = 1,
    default_val = 1 )

  pid = IntPrim(
    doc = "The process id of the primary process running the tool on the `runhost`",
    default_val = 0 )

  cmd_index = IntPrim(
    doc = "Index of last attempted command",
    default_val = -1 )

  cmd_id = StrPrim(
    doc = "ID (key) of last attempted command",
    default_val = optional,
    max_lines = 1 )

  mpiexec = SeqPrim(
    doc = """List of arguments to execute a program within MPI, if available.

      This will be set, and the `{np}` variable in the original format strings
      will be replaced with the current value of `processes`, only if
      `processes > 1`.
      The arguments may be taken from the environment variable `NWL_MPIEXEC`,
      for example:

      .. code-block:: bash

        export NWL_MPIEXEC='mpirun -np {np:d} -host {nodes:s}'""",
    item = StrPrim(
      max_lines = 1 ),
    default_val = list() )

  env = MapPrim(
    doc = """Environment variables set for tool run

      .. note::

        All environment variable names are first sanitized to contain only
        alpha|digit|underscore, with runs of other characters replaced by a
        single underscore '_'.""",
    item = StrPrim(),
    default_val = dict() )

  logs = HintList
