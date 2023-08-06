# -*- coding: UTF-8 -*-

import os
import subprocess
import shutil
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
  PyEvaluated,
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

from partis.schema.prim.any_prim import (
  any_prim_cases,
  AnyPrim )

from ..base import (
  ToolError )

from ..log import (
  LogEvent )

from .base import (
  EvaluatedCommands,
  BaseCommandOutput,
  BaseCommand )

from ..context import (
  ScriptContext )

from ..outputs import (
  BoolOutput,
  IntOutput,
  FloatOutput,
  StrOutput,
  ListOutput,
  StructOutput,
  UnionOutput,
  RunFileOutput,
  RunDirOutput )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
AnyScriptResult = UnionPrim(
  doc = """Type for result value of script command
    """,
  default_val = optional,
  cases = [
   BoolOutput,
   IntOutput,
   FloatOutput,
   StrOutput,
   ListOutput,
   StructOutput,
   UnionOutput,
   RunFileOutput,
   RunDirOutput ] )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
EvaluatedScript = PyEvaluated.subclass(
  context = ScriptContext )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ScriptCommandOutput( BaseCommandOutput ):
  schema = dict(
    tag = 'script',
    default_val = derived )

  return_val = UnionPrim(
    doc = "Return value of script",
    cases = any_prim_cases,
    default_val = optional,
    evaluated = EvaluatedScript )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ScriptCommand( BaseCommand ):
  schema = dict(
    tag = 'script' )

  source = UnionPrim(
    doc = """Script source to run

      The return value may be structured plain JSON compatible data types.""",
    cases = any_prim_cases,
    default_val = required,
    evaluated = EvaluatedScript,
    init_val = "$func:py\n  return 0" )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, module = None ):
    return ScriptCommandOutput

  #-----------------------------------------------------------------------------
  def _open( self,
    tool_results ):

    super()._open(
      tool_results = tool_results )

    eval_log = self._log.getChild('eval')
    eval_log.propagate = False
    eval_handler = LogListHandler()
    eval_log.addHandler( eval_handler )

    try:
      # TODO: how to impose timeout?
      self._results.return_val = self.source


      self._results.return_val = self._results.return_val._eval(
        context = ScriptContext(
          results = tool_results,
          static = self._tool.resources.static ),
        logger = eval_log )

      self._log.info(
        ModelHint(
          f"Script finished",
          hints = eval_handler.hints ) )

    except BaseException as e:
      self._log.error( ModelHint(
        msg = "Failed to evaluate script",
        hints = eval_handler.hints + [e] ) )

      return

    finally:
      eval_log.removeHandler(eval_handler)

  #-----------------------------------------------------------------------------
  def lint( self, tool, cmd_id, results ):
    hints = super().lint( tool, cmd_id, results )

    cmd_results = results.data.commands[cmd_id]
    cmd_results.return_val = self.source

    hints.extend( cmd_results.return_val._lint(
      context = ScriptContext(
        results = results,
        static = tool.resources.static ) ) )


    return hints
