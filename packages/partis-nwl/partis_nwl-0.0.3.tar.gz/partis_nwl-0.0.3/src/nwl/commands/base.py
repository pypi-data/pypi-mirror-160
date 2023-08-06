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

from ..base import (
  ToolError )

from ..log import (
  LogEvent )

from ..context import (
  CommandsContext,
  CommandLogContext )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
EvaluatedCommands = PyEvaluated.subclass(
  context = CommandsContext )

CheetahCommands = CheetahEvaluated.subclass(
  context = CommandsContext )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BaseCommandOutput( StructValued ):
  schema = dict(
    tag = 'base_command_out',
    doc = "",
    default_val = derived )

  enabled = BoolPrim(
    doc = "Flag for whether the command was enabled.",
    default_val = False )

  success = BoolPrim(
    doc = "Flag for whether the command ran and closed successfully.",
    default_val = False )

  starttime = FloatPrim(
    doc = "Unix timstamp of starting time of command.",
    default_val = 0.0 )

  timeout = FloatPrim(
    doc = "Time limit imposed before terminating command in seconds.",
    default_val = 0.0 )

  walltime = FloatPrim(
    doc = "Amount of real time command was running in seconds.",
    default_val = 0.0 )

  env = MapPrim(
    doc = "Additional environment variables that were set for this command.",
    item = StrPrim(),
    default_val = dict() )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BaseCommand( StructValued ):
  schema = dict(
    tag = 'base_command' )

  label = StrPrim(
    doc = "Short identifying string for this command",
    default_val = '',
    max_lines = 1,
    max_cols = 80 )

  doc = StrPrim(
    doc = "Documentation string for more information about this command",
    default_val = '',
    max_lines = 100 )

  env = MapPrim(
    doc = "Additional environment variables to set for this command.",
    item = StrPrim(
      doc = "Environment variable",
      evaluated = EvaluatedCommands ),
    default_val = dict(),
    evaluated = EvaluatedCommands )

  enabled = BoolPrim(
    doc = "Marks the command as enabled if True, disabled if False",
    default_val = True,
    evaluated = EvaluatedCommands )

  prolog = SeqPrim(
    doc = """List of possible logging events before opening command.
      Logs with level 'ERROR' or 'CRITICAL' are used to establish whether a
      command has failed.
      """,
    item = LogEvent,
    default_val = list() )

  epilog = SeqPrim(
    doc = """List of possible logging after closing command.
      Logs with level 'ERROR' or 'CRITICAL' are used to establish whether a
      command has failed.
      """,
    item = LogEvent,
    default_val = list() )

  #-----------------------------------------------------------------------------
  def __init__( self, *args, **kwargs ):
    super().__init__(*args, **kwargs)

    self._workdir = None
    self._rundir = None
    self._cmd_id = None
    self._time_start = None
    self._timeout = None
    self._time_limit = None

    self._walltime = None

    self._log = None
    self._log_handler = None
    self._env = None
    self._venv = None

    self._configured = False
    self._opened = False
    self._closed = False
    self._failed = False

  #-----------------------------------------------------------------------------
  def value_schema( self, name, module = None ):
    """Schema for command output
    """
    raise SchemaError(f"`value_schema` not implemented for this command")

  #-----------------------------------------------------------------------------
  def _reset( self ):
    if self._log is not None:
      if self._log_handler is not None:
        self._log.removeHandler(self._log_handler)

    self._workdir = None
    self._rundir = None
    self._cmd_id = None
    self._time_start = None
    self._timeout = None
    self._time_limit = None

    self._walltime = None

    self._log = None
    self._log_handler = None
    self._env = None
    self._venv = None

    self._configured = False
    self._opened = False
    self._closed = False
    self._failed = False

  #-----------------------------------------------------------------------------
  def _config( self,
    tool,
    workdir,
    rundir,
    env,
    venv,
    id,
    tool_results,
    timeout = None,
    log = None ):
    """Configure command execution

    Parameters
    ----------
    workdir : str
      Current directory from which the command was started
    rundir : str
      Working in which to run the command
    env : dict
      Environment variables
    venv : :class:`ProcessEnv <partis.utils.venv.ProcessEnv`
      Virtual process environment to run any subprocesses
    id : int
      Command index
    tool_results : dict[str,object]
      Current tool results
    timeout : int | None
      Timeout to terminate command in seconds

    Returns
    -------
    result: BaseCommandOutput
      Result of command before opening
    """

    if self._configured and not self._closed:
      raise ValueError("Command already configured")

    self._reset()

    self._configured = True

    if log is not None:
      self._log = log.getChild(f"{id}")
    else:
      self._log = logging.getLogger(f"{id}")

    self._log_handler = LogListHandler()

    self._log.addHandler( self._log_handler )

    self._tool = tool

    self._workdir = workdir
    self._rundir = rundir
    self._cmd_id = id

    self._log.debug(f"Command configuring: `{self._cmd_id}`")

    self._results = self.value_schema(
      name = self._cmd_id,
      module = tool_results._schema.__module__ )()

    self._results.timeout = timeout
    self._results.env = self.env
    self._results.enabled = self.enabled

    self._env = { **env, **self.env }
    self._venv = venv

    try:
      logs = self.prolog._eval(
        context = CommandLogContext(
          results = tool_results,
          static = self._tool.resources.static,
          command = self._results ),
        logger = self._log.getChild('prolog') )

      # filter for only enabled log events
      for l in logs:
        if l.enabled:
          self._log.log( logging.getLevelName(l.level), l.msg )

    except Exception as e:
      self._log.error( ModelHint(
        msg = f"Command prolog evaluation failed: `{self._cmd_id}`",
        hints = e ) )

    self._update_result_logs()

    return self._results

  #-----------------------------------------------------------------------------
  def _update_result_logs( self ):
    if self._log_handler is None:
      return

    logs = self._log_handler.logs
    self._log_handler.clear()

    # command fails if any prolog event of 'ERROR' or 'CRITICAL'
    self._failed = self._failed or any(
      l['level'] in [ 'ERROR', 'CRITICAL' ]
      for l in logs )

  #-----------------------------------------------------------------------------
  def _open( self,
    tool_results ):
    """Start command execution

    Parameters
    ----------
    tool_results : dict[str,object]
      Current tool results

    Returns
    -------
    None
    """

    if not self._configured:
      raise ValueError("Command never configured")

    if self._opened:
      raise ValueError("Command already opened")

    self._opened = True

    self._log.info(f"Command opening: `{self._cmd_id}`")

    self._results.starttime = timer()

    if self._results.timeout > 0:
      self._time_limit = self._time_start + self._results.timeout


  #-----------------------------------------------------------------------------
  def _poll( self,
    tool_results ):
    """Monitor command for completion.

    If completed, will automatically close the command and return final results.

    Parameters
    ----------
    tool_results : dict[str,object]
      Current tool results

    Returns
    -------
    result: None | BaseCommandOutput
      If None, the command has not completed. Otherwise returns result of command
    """
    return self._close(
      tool_results = tool_results )

  #-----------------------------------------------------------------------------
  def _close( self,
    tool_results ):
    """Closes command, even if still executing or if was never fully opened

    Parameters
    ----------
    tool_results : dict[str,object]
      Current tool results

    Returns
    -------
    result: BaseCommandOutput
      Returns result of command after closing
    """
    if not self._opened:
      raise ValueError("Command never opened")


    if self._closed:
      raise ValueError("Command already closed")

    self._closed = True

    self._log.debug(f"Command closing: `{self._cmd_id}`")

    self._results.walltime = timer() - self._results.starttime
    self._update_result_logs()

    if not self._failed:
      try:
        logs = self.epilog._eval(
          context = CommandLogContext(
            results = tool_results,
            static = self._tool.resources.static,
            command = self._results ),
          logger = self._log.getChild('epilog') )

        # filter for only enabled log events
        for l in logs:
          if l.enabled:
            self._log.log( logging.getLevelName(l.level), l.msg )

      except Exception as e:
        self._log.error( ModelHint(
          msg = f"Command epilog evaluation failed: `{self._cmd_id}`",
          hints = e ) )

    self._update_result_logs()

    self._results.success = not self._failed

    return self._results

  #-----------------------------------------------------------------------------
  def lint( self, tool, cmd_id, results ):
    hints = list()

    cmd_results = results.data.commands[cmd_id]

    hints.extend( self._lint(
      context = CommandsContext(
        results = results,
        static = tool.resources.static ) ) )

    hints.extend( self.prolog._lint(
      context = CommandLogContext(
        results = results,
        static = tool.resources.static,
        command = cmd_results ) ) )

    hints.extend( self.epilog._lint(
      context = CommandLogContext(
        results = results,
        static = tool.resources.static,
        command = cmd_results ) ) )

    return hints
