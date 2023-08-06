# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .base import (
  CommandsContext,
  EvaluatedCommands,
  BaseCommandOutput,
  BaseCommand )

from .file import (
  FileCommandOutput,
  FileCommand )

from .dir import (
  DirCommandOutput,
  DirCommand )

from .process import (
  StdFile,
  StdInFile,
  StdOutFile,
  StdErrFile,
  ProcessCommandOutput,
  ProcessArgument,
  ProcessCommand )

from .script import (
  EvaluatedScript,
  ScriptCommandOutput,
  ScriptCommand )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from partis.schema import (
  UnionPrim )

AnyCommand = UnionPrim(
  cases = [
    ProcessCommand,
    FileCommand,
    DirCommand,
    ScriptCommand ] )
