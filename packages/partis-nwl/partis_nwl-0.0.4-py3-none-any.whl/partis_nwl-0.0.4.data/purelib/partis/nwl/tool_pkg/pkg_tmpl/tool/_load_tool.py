__all__ = list()

import os
import os.path as osp
import re

from partis.nwl import (
  ToolRuntime,
  Tool,
  NWLToolPkg )

from partis.schema import (
  SchemaHint,
  SchemaError,
  Loc,
  SchemaModule )

from partis.schema.serialize.yaml import (
  load,
  dump )

pkg_dir = osp.dirname( osp.abspath( __file__ ) )
tool_file = osp.join( pkg_dir, 'tool.yml' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def load_tool( ):

  from . import inputs
  from . import outputs
  from . import commands
  from . import results


  tool = load(
    file = tool_file,
    schema = Tool,
    loc = Loc(
      filename = tool_file ) )

  tool.results_schema(
    module = results,
    input_module = inputs,
    output_module = outputs,
    command_module = commands  )

  return tool
