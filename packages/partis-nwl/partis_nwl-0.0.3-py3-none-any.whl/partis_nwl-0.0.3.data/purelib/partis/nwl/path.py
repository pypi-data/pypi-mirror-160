import os
import os.path as osp

import logging
log = logging.getLogger(__name__)

from Cheetah.Template import Template

from partis.schema import (
  SchemaEvaluationError,
  ProviderSupport,
  Provider,
  Evaluated )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class WorkAbsolutePathProvider( Provider ):
  """Evaluates paths
  """

  #-----------------------------------------------------------------------------
  @property
  def supported( self ):
    return dict(
      rel_path = ProviderSupport(
        name = f"Coerces relative paths into absolute paths from working directory",
        lexer = 'text' ) )

  #-----------------------------------------------------------------------------
  def check( self, src ):

    if src == '':

      return None

    try:
      head, tail = osp.split( src )

      if not osp.isabs(src):
        return self.supported['rel_path'], src

    except:
      pass

    return None

  #-----------------------------------------------------------------------------
  def escaped( self, support, src ):
    return src

  #-----------------------------------------------------------------------------
  def eval( self,
    schema,
    src,
    locals = None,
    module = None,
    logger = None ):

    if not self.check( src ):
      raise SchemaEvaluationError(f"Not valid relative path: {src}")

    if locals is None:
      return src

    path = src

    if not osp.isabs(path):
      path = osp.realpath( osp.join( locals._.runtime.workdir, path ) )

    return path


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class WorkRelativePathProvider( Provider ):
  """Evaluates paths
  """

  #-----------------------------------------------------------------------------
  @property
  def supported( self ):
    return dict(
      abs_path = ProviderSupport(
        name = f"Coerces absolute paths into relative paths from working directory",
        lexer = 'text' ) )

  #-----------------------------------------------------------------------------
  def check( self, src ):

    if src == '':
      return None

    try:
      head, tail = osp.split( src )

      if osp.isabs(src):
        return self.supported['abs_path'], src

    except:
      pass

    return None

  #-----------------------------------------------------------------------------
  def escaped( self, support, src ):
    return src

  #-----------------------------------------------------------------------------
  def eval( self,
    schema,
    src,
    locals = None,
    module = None,
    logger = None ):

    if not self.check( src ):
      raise SchemaEvaluationError(f"Not valid absolute path: {src}")

    if locals is None:
      return src

    path = osp.realpath(src)
    dir = locals._.runtime.workdir

    if osp.commonpath([path, dir]) == dir:
      path = osp.relpath(
        path,
        start = dir)

    return path

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RunAbsolutePathProvider( Provider ):
  """Evaluates paths
  """

  #-----------------------------------------------------------------------------
  @property
  def supported( self ):
    return dict(
      rel_path = ProviderSupport(
        name = f"Coerces relative paths into absolute paths from run directory",
        lexer = 'text' ) )

  #-----------------------------------------------------------------------------
  def check( self, src ):

    if src == '':
      return None

    try:
      head, tail = osp.split( src )

      if not osp.isabs(src):
        return self.supported['rel_path'], src

    except:
      pass

    return None

  #-----------------------------------------------------------------------------
  def escaped( self, support, src ):
    return src

  #-----------------------------------------------------------------------------
  def eval( self,
    schema,
    src,
    locals = None,
    module = None,
    logger = None ):

    if not self.check( src ):
      raise SchemaEvaluationError(f"Not valid relative path: {src}")

    if locals is None:
      return src

    path = src

    if not osp.isabs(path):
      path = osp.realpath( osp.join( locals._.runtime.rundir, path ) )

    return path

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RunRelativePathProvider( Provider ):
  """Evaluates paths
  """

  #-----------------------------------------------------------------------------
  @property
  def supported( self ):
    return dict(
      abs_path = ProviderSupport(
        name = f"Coerces absolute paths into relative paths from run directory",
        lexer = 'text' ) )

  #-----------------------------------------------------------------------------
  def check( self, src ):

    if src == '':
      return None

    try:
      head, tail = osp.split( src )

      if osp.isabs(src):
        return self.supported['abs_path'], src

    except:
      pass

    return None

  #-----------------------------------------------------------------------------
  def escaped( self, support, src ):
    return src

  #-----------------------------------------------------------------------------
  def eval( self,
    schema,
    src,
    locals = None,
    module = None,
    logger = None ):

    if not self.check( src ):
      raise SchemaEvaluationError(f"Not valid absolute path: {src}")

    if locals is None:
      return src

    path = osp.realpath(src)
    dir = locals._.runtime.rundir

    if osp.commonpath([path, dir]) == dir:
      path = osp.relpath(
        path,
        start = dir)

    return path

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
work_rel_path_provider = WorkRelativePathProvider()

class WorkRelativePathEvaluated( Evaluated, provider = work_rel_path_provider ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
work_abs_path_provider = WorkAbsolutePathProvider()

class WorkAbsolutePathEvaluated( Evaluated, provider = work_abs_path_provider ):
  pass


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
run_rel_path_provider = RunRelativePathProvider()

class RunRelativePathEvaluated( Evaluated, provider = run_rel_path_provider ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
run_abs_path_provider = RunAbsolutePathProvider()

class RunAbsolutePathEvaluated( Evaluated, provider = run_abs_path_provider ):
  pass
