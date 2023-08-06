
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


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolGPU( StructValued ):
  """Tool GPU resource requirements
  """

  schema = dict(
    tag = 'gpu',
    default_val = derived )

  gpu_required = BoolPrim(
    doc = """Tool must have GPU to run.
      If false, the tool may be run without a GPU allocated""",
    default_val = False )

  gpu_support = SeqPrim(
    doc = """Tool supports acceleration through a GPU device interface.
      If given, GPU allocations may be made for one of the listed GPU
      interfaces""",
    item = StrPrim(
      doc = """GPU supported by tool""",
      restricted = [ 'CUDA', 'HIP' ],
      default_val = 'CUDA' ),
    default_val = list() )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolModule( StructValued ):
  """Tool included Python module resource
  """

  schema = dict(
    tag = 'module',
    default_val = derived,
    struct_proxy = 'path' )

  path = StrPrim(
    doc = """Path to a Python module to include, relative to tool file.

      If the path is a directory, the directory must contain an '__init__.py'.""",
    max_lines = 1,
    default_val = '' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolPython( StructValued ):
  """Tool Python requirements
  """

  schema = dict(
    tag = 'python',
    default_val = derived )

  module = ToolModule

  requires_python = StrPrim(
    doc = """The Python version requirements
      See Also
      --------
      * https://www.python.org/dev/peps/pep-0621/#requires-python
      """,
    default_val = optional ),

  dependencies = SeqPrim(
    doc = """Runtime dependencies on Python packages.
    Equivalent to those listed in a requirements file, `install_requires` of
    a `setup.py`, or `dependencies` of a `pyproject.toml` file.
    These must only be for those dependencies needed at **runtime**, and **not**
    needed for evaluating any expressions contained within the inputs section
    of the tool.
    """,
    item = StrPrim(
      doc = """A Python dependency
        See Also
        --------
        * https://www.python.org/dev/peps/pep-0508/
        """,
      max_lines = 1,
      default_val = required ),
    default_val = list() )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolData( StructValued ):
  """Tool included data resource
  """

  schema = dict(
    tag = 'data',
    struct_proxy = 'path' )

  path = StrPrim(
    doc = """Path to data relative to tool file or directory.

      If the path is a directory, the entire contents of the directory will be
      recursivly included.""",
    max_lines = 1,
    default_val = required )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolResources( StructValued ):
  """Tool resources information
  """

  schema = dict(
    tag = 'resources',
    default_val = derived )

  multi_thread = BoolPrim(
    doc = """Tool supports multiple threads per process.
      If true, CPU allocation may be made for running multiple threads for
      each process""",
    default_val = False )

  multi_process = BoolPrim(
    doc = """Tool supports multiple processes.
      If true, CPU allocation may be made for running multiple processes.
      If a a multiprocess CPU allocation is made, the `mpiexec` runtime
      variable will contain the command needed to run a program under MPI with
      the given allocation, but it is not a requirement to use MPI.""",
    default_val = False )

  multi_process_mpi = BoolPrim(
    doc = """Tool supports multiple processes through an MPI implementation.
      Setting to true will prevent the tool from running if no MPI startup commands
      are specified when the number of requested processes is > 1""",
    default_val = True )

  multi_node = BoolPrim(
    doc = """Tool supports multiple compute nodes.
      If true, multi-process CPU allocations may be distributed to more than one
      node (host machine).
      If a a multi-node CPU allocation is made, the `mpiexec` runtime
      variable will contain the command needed to run a program under MPI with
      the given allocation, which specifies a machine file listing the
      hosts on which the allocations were made.""",
    default_val = True )

  gpu = ToolGPU

  python = ToolPython

  static = MapPrim(
    doc = """Static files included with the tool, not including the tool file""",
    item = ToolData,
    default_val = dict() )
