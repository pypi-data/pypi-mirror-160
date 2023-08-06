# -*- coding: UTF-8 -*-

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  adict )

from partis.schema import (
  EvaluatedContext )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolContext( EvaluatedContext,
  id = 'nwl' ):
  """Base evaluation context for NWL tools
  """

  #-----------------------------------------------------------------------------
  def __init__( self, *,
    results,
    static ):

    super().__init__(
      module = results._schema.__module__ )

    self._p_results = results
    self._p_static = static

  #-----------------------------------------------------------------------------
  def locals( self, schema ):
    return {
      '_' : self._p_results,
      'static' : self._p_static }


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class InputsContext( ToolContext,
  id = 'inputs' ):
  """Evaluation context for NWL tool input expressions
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class OutputsContext( ToolContext,
  id = 'outputs' ):
  """Evaluation context for NWL tool output expressions
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LogContext( ToolContext,
  id = 'log' ):
  """Evaluation context for NWL tool logging expressions
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CommandsContext( ToolContext,
  id = 'commands' ):
  """Evaluation context for NWL tool command expressions
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CommandLogContext( CommandsContext,
  id = 'log' ):
  """Evaluation context for NWL tool command log expressions
  """

  #-----------------------------------------------------------------------------
  def __init__( self, *,
    results,
    static,
    command ):

    super().__init__(
      results = results,
      static = static )

    self._p_command = command

  #-----------------------------------------------------------------------------
  def locals( self, schema ):

    return {
      '_' : adict({
        **self._p_results,
        'command' : self._p_command }),
      'static' : self._p_static }

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ArgumentContext( CommandsContext,
  id = 'arg' ):
  """Evaluation context for NWL tool command argument expressions
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ScriptContext( CommandsContext,
  id = 'script' ):
  """Evaluation context for NWL tool command scripts
  """
  pass
