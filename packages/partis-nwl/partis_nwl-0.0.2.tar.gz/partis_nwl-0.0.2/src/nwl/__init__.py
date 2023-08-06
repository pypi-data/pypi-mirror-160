# -*- coding: UTF-8 -*-

"""Schema definition for the Nano Workflow Language (NWL), and implementation
for
"""


from .base import (
  ToolError )

from .context import (
  ToolContext,
  InputsContext,
  OutputsContext,
  LogContext,
  CommandsContext,
  CommandLogContext,
  ArgumentContext,
  ScriptContext )

from .path import (
  WorkRelativePathEvaluated,
  WorkAbsolutePathEvaluated,
  RunRelativePathEvaluated,
  RunAbsolutePathEvaluated )

from .log import (
  LogEvent )

from .inputs import (
  BaseInput,
  BoolInput,
  IntInput,
  FloatInput,
  StrInput,
  ListInput,
  StructInput,
  UnionInput,
  WorkFileInput,
  RunFileInput,
  WorkDirInput,
  RunDirInput,
  AnyInput )

from .commands import (
  BaseCommandOutput,
  BaseCommand,
  FileCommandOutput,
  FileCommand,
  DirCommandOutput,
  DirCommand,
  ProcessCommandOutput,
  ProcessCommand,
  ScriptCommandOutput,
  ScriptCommand,
  AnyCommand )

from .outputs import (
  BaseOutput,
  BoolOutput,
  IntOutput,
  FloatOutput,
  StrOutput,
  ListOutput,
  StructOutput,
  UnionOutput,
  RunFileOutput,
  RunDirOutput,
  PathOutputValue,
  AnyOutput )

from .info import (
  ToolAuthor,
  ToolInfo )

from .resources import (
  ToolGPU,
  ToolPython,
  ToolResources )

from .runtime import ToolRuntime

from .results import ToolResults

from .tool import Tool

from .tool_pkg import (
  NWLToolPkg,
  ToolFile,
  NWLToolPkgInfo )

from partis.schema.serialize.yaml import (
  load as load_yaml,
  dump as dump_yaml )

from partis.schema.serialize.json import (
  load as load_json,
  dump as dump_json )

from .utils import (
  load_results )
