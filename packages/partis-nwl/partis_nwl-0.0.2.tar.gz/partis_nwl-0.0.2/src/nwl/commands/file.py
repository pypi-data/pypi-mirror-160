# -*- coding: UTF-8 -*-

import os
import subprocess
import shutil
import base64
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
  CheetahCommands,
  BaseCommandOutput,
  BaseCommand )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FileCommandOutput( BaseCommandOutput ):
  schema = dict(
    tag = 'file',
    default_val = derived )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FileCommand( BaseCommand ):
  """Creates a file with given contents in the run directory
  """

  schema = dict(
    tag = 'file' )

  path = StrPrim(
    doc = "Path relative to run directory. Parent directories will be created.",
    evaluated = EvaluatedCommands,
    max_lines = 1 )

  content_mode = StrPrim(
    doc = "Mode used to write contents to file",
    restricted = [ 'text', 'binary' ],
    default_val = 'text' )

  contents = StrPrim(
    doc = """Contents to write to file

      In `binary` mode, the contents are assumed to be in standard
      Base64 format ( RFC 3548 ).""",
    evaluated = EvaluatedCommands | CheetahCommands,
    default_val = optional )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, module = None ):
    return FileCommandOutput

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
    log = None, ):

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

      _dir = os.path.dirname( self._path )

      if not os.path.exists( _dir ):
        self._log.info(f"Created directory: {_dir}" )

        os.makedirs( _dir )

      if self.contents is None:
        # just "touch" the file
        with open( self._path, 'a'):
          os.utime( self._path, None )

      else:
        if self.content_mode == 'text':

          content_bytes = self.contents.encode('utf-8')

        elif self.content_mode == 'binary':

          content_bytes = base64.urlsafe_b64decode( self.contents.strip() )

        else:
          assert False

        with open( self._path, 'wb' ) as fp:
          fp.write( content_bytes )

      self._log.info(f"Created file: {self._path}" )

    except Exception as e:
      self._log.error( ModelHint(
        msg = f"Failed to create file: {self._path}",
        hints = e ) )
