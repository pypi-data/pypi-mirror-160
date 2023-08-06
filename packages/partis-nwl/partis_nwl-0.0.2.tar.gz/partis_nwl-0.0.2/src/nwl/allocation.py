
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

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RunAllocation( StructValued ):
  schema = dict(
    tag = 'run',
    doc = "Tool runtime information",
    default_val = derived )

  rundir = StrPrim(
    doc = "Directory where tool was told to run, and resolves output file paths",
    default_val = "",
    max_lines = 1 )

  processes = IntPrim(
    doc = """Number of processes allocated

      The total CPU cores allocated is `( processes * cpus_per_process )`.
      The value may be taken from the environment variable `NWL_PROCS`.""",
    min = 1,
    default_val = 1 )

  cpus_per_process = IntPrim(
    doc = """Number of cores allocated per process.

      The value may be taken from the environment variable `NWL_CPUS_PER_PROC`.""",
    min = 1,
    default_val = 1 )

  threads_per_cpu = IntPrim(
    doc = """Number of logical threads per CPU core.

    The total number of logical threads is
    ``( threads_per_cpu * cpus_per_process )``.
    The value may be taken from the environment variable `NWL_THREADS_PER_CPU`.""",
    min = 1,
    default_val = 1 )

  gpus_per_process = IntPrim(
    doc = """Number of GPUs allocated per process.

      The value may be taken from the environment variable `NWL_GPUS_PER_PROC`.""",
    min = 0,
    default_val = 0 )

  timeout = IntPrim(
    doc = """Time allocated (seconds)""",
    min = 1,
    default_val = optional )

  aux = MapPrim(
    doc = """Auxiliary variables that may be used for input query substitution.

      .. note::

        These values should only be used to perform value
        substituion for queries present in an `inputs` file, when those values
        may need to be passed on the command line instead of the inputs file.

        For example:

        .. code-block:: yaml
          :caption:
            inputs_file.yml

          some_input: $nwl:tool?var=runtime.aux.some_aux_val&type=int

        Then values can be specified to be substituted on the command line:

        .. code-block:: bash

          partis-nwl --tool my_tool --inputs inputs_file.yml --aux some_aux_val=42

        The values here are not (and should not) be referenced directly by expressions
        in a tool definition, instead using the result after substitution to input
        values.

      """,
    item = StrPrim(),
    default_val = dict() )
