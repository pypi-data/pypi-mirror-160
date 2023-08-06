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
  PJCEvaluated,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  StructValued,
  schema_declared )

from ..base import (
  ToolError )

from ..log import (
  LogEvent )

from .base import (
  EvaluatedCommands,
  BaseCommandOutput,
  BaseCommand )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DirCommandOutput( BaseCommandOutput ):
  schema = dict(
    tag = 'dir',
    default_val = derived )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DirCommand( BaseCommand ):
  """Creates a directory in the run directory
  """

  schema = dict(
    tag = 'dir' )

  path = StrPrim(
    doc = "Path relative to run directory. Parent directories will be created.",
    evaluated = EvaluatedCommands,
    max_lines = 1 )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, module = None ):
    return DirCommandOutput

  #-----------------------------------------------------------------------------
  def __init__( self, *args, **kwargs ):
    super().__init__(*args, **kwargs)

    self._path = None

  #-----------------------------------------------------------------------------
  def _reset( self ):
    super()._reset()

    self._path = None

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

    super()._config(
      tool = tool,
      workdir = workdir,
      rundir = rundir,
      env = env,
      venv = venv,
      id = id,
      tool_results = tool_results,
      timeout = timeout,
      log = log )

    self._path = os.path.join(rundir, self.path)

    return self._results

  #-----------------------------------------------------------------------------
  def _open( self,
    tool_results ):

    super()._open(
      tool_results = tool_results )

    try:

      if not os.path.exists( self._path ):
        self._log.info(f"Created directory: {self._path}" )

        os.makedirs( self._path )

    except Exception as e:
      self._log.error( ModelHint(
        msg = f"Failed to create directory: {self._path}",
        hints = e ) )
