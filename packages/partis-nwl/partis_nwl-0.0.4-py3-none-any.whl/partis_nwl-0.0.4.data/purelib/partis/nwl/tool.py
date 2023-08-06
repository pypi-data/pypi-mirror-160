
import os
import os.path as osp
import re
import subprocess
import shutil
import shlex
from timeit import default_timer as timer
import socket
from string import Formatter

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  odict,
  adict,
  ModelHint,
  ModelError,
  LogListHandler,
  ProcessEnv )

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

from .base import (
  ToolError )

from .inputs import (
  AnyInput,
  InputsContext )

from .commands import (
  AnyCommand,
  CommandsContext )

from .outputs import (
  AnyOutput,
  AnyMainOutput,
  OutputsContext )

from .log import (
  LogContext,
  LogEvent )

from partis.schema.serialize.yaml import (
  load,
  dump )

from .utils import (
  check_inout_files )

from .info import ToolInfo

from .resources import ToolResources

from .results import (
  ToolData,
  ToolResults )

from .utils import (
  get_mpiexec,
  get_processes,
  get_nodelist,
  get_cpus_per_process,
  get_threads_per_cpu,
  get_gpus_per_process,
  get_runhost,
  get_jobhost,
  get_jobuser,
  get_jobid,
  get_jobname )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Tool( StructValued ):
  schema = dict(
    tag = 'tool',
    doc = "Tool definition",
    default_val = derived )

  nwl = IntPrim(
    doc = "Version of Nano Workflow Language (NWL)",
    restricted = [ 1, ],
    default_val = 1 )

  qualname = StrPrim(
    doc = """A qualified, unambiguous name for the tool
    This is used to identify the tool as the generator of result files.
    Must be a valid, qualified Python module name.

    .. note::

      This will likely be set/overwritten automatically by the tool packager""",
    max_lines = 1,
    max_cols = 80,
    default_val = '' )

  info = ToolInfo

  resources = ToolResources

  inputs = MapPrim(
    item = AnyInput,
    default_val = dict() )

  outputs = MapPrim(
    item = AnyMainOutput,
    default_val = dict() )

  commands = MapPrim(
    item = AnyCommand,
    default_val = dict() )

  prolog = SeqPrim(
    doc = """List of possible logging events before starting tool execution.
      These may be used to issue messages about input values, such as additional
      sanity checking that depend on the inputs as a whole.
      Like expressions in the inputs, these may be run in a graphical editor to
      inform the user, and should not depend on, or import, non-standard packages.
      Logs with level 'ERROR' or 'CRITICAL' are used to establish whether the
      tool has failed.
      """,
    item = LogEvent,
    default_val = list() )

  epilog = SeqPrim(
    doc = """List of possible logging after tool execution.
      Logs with level 'ERROR' or 'CRITICAL' are used to establish whether the
      tool has failed.
      """,
    item = LogEvent,
    default_val = list() )


  #-----------------------------------------------------------------------------
  def __init__( self, *args, **kwargs ):
    super().__init__(*args, **kwargs)

    self._configured = False
    self._opened = False
    self._closed = False
    self._failed = False

  #-----------------------------------------------------------------------------
  def tool_doc( self ):

    info = self.info

    lines = [
      info.label,
      '='*len(info.label),
      '',
      info.doc,
      '',
      f'* version: ' + '.'.join([str(v) for v in info.version]),
      '' ]

    if info.author.name or info.author.email:
      lines.extend( [ '* author', '' ] )

      if info.author.name:
        lines.append(f'  * name: {info.author.name}')

      if info.author.email:
        lines.append(f'  * email: {info.author.email}')

    return '\n'.join(lines)

  #-----------------------------------------------------------------------------
  def inputs_schema( self, module = None ):

    module = module or SchemaModule()

    struct = list()

    inputs = self.inputs

    for k,v in inputs.items():
      struct.append( (k, v.value_schema(
        module = module,
        name = f'results_data_inputs_{k}' ) ) )

    return StructValued.subclass(
      tag = 'inputs',
      doc = "Inputs",
      struct = struct,
      default_val = derived,
      module = module,
      name = 'results_data_inputs' )

  #-----------------------------------------------------------------------------
  def commands_schema( self, module = None ):

    module = module or SchemaModule()

    struct = list()

    commands = self.commands

    for k, v in commands.items():

      struct.append( (k, v.value_schema(
        module = module,
        name = f'results_data_commands_{k}' ) ) )

    return StructValued.subclass(
      tag = 'commands',
      doc = "Commands",
      struct = struct,
      default_val = derived,
      module = module,
      name = 'results_data_commands' )

  #-----------------------------------------------------------------------------
  def outputs_schema( self, module = None ):

    module = module or SchemaModule()

    struct = list()

    outputs = self.outputs

    for k,v in outputs.items():
      struct.append( (k, v.value_schema(
        module = module,
        name = f'results_data_outputs_{k}' ) ) )

    return StructValued.subclass(
      tag = 'outputs',
      doc = "Outputs",
      struct = struct,
      default_val = derived,
      module = module,
      name = 'results_data_outputs' )

  #-----------------------------------------------------------------------------
  def results_schema( self,
    module = None,
    input_module = None,
    output_module = None,
    command_module = None ):

    module = module or SchemaModule()
    input_module = input_module or module
    output_module = output_module or module
    command_module = command_module or module

    inputs_schema = self.inputs_schema( module = input_module )
    commands_schema = self.commands_schema( module = command_module )
    outputs_schema = self.outputs_schema( module = output_module )

    data_schema = ToolData.subclass(
      struct = dict(
        inputs = inputs_schema,
        outputs = outputs_schema,
        commands = commands_schema ),
      module = module,
      name = 'results_data' )

    results_schema = ToolResults.subclass(
      tag = 'results',
      struct = dict(
        data = data_schema ),
      module = module,
      name = 'results' )

    return results_schema

  #-----------------------------------------------------------------------------
  def _config( self, *,
    workdir = None,
    rundir = None,
    env = None,
    aux = None,
    timeout = None,
    truncate = None,
    log = None,
    mpiexec = None,
    processes = None,
    nodes = None,
    cpus_per_process = None,
    threads_per_cpu = None,
    gpus_per_process = None,
    jobargs = None,
    inputs = None,
    inputs_file = None,
    venv = None,
    results_schema = None,
    initlogs = None ):
    """Configure tool execution

    Parameters
    ----------
    workdir : None | str
      Directory from which the tool resolves relative input file paths.
      Defaults to the present working directory.
    rundir : None | str
      Directory in which to run the command.
      Defaults to `workdir`.
    env : None | dict
      Environment variables to set while running tool and any sub-processes.
      If None, sub-processes will not inherit the current environment.

      .. note::

        All environment variable names are first sanitized to contain only
        alpha|digit|underscore, with runs of other characters replaced by a
        single underscore '_'.
    aux : None | dict
      Auxiliary variables that may be used for input query substitution.
    timeout : int | None
      Timeout to terminate command in seconds
    truncate : None | bool
      If true, and rundir already exists, will completely remove directory and
      all contents before starting command. (default: False)
    log : None | logging.Logger
      Parent logger to issue logging events
    mpiexec : None | list[str]
      List of commands to execute a program within MPI, if available.
      Also set by the environment variable ``NWL_MPIEXEC``.

      .. note::

        The arguments may contain format strings which are substituded with
        runtime parameters. For example,

        .. code-block:: bash

          export NWL_MPIEXEC='mpiexec -n {processes} -host {nodes}'

        or

        .. code-block:: bash

          export NWL_MPIEXEC='mpiexec -n {processes} -machinefile {nodefile}'

    processes : None | int
      Also set by the environment variable ``NWL_PROCS``.
    nodes : None | list[str]
      List of nodes to use for multiprocessing (MPI)
      Also set by the environment variable ``NWL_NODELIST`` or ``NWL_NODEFILE``.
    cpus_per_process : None | int
      Also set by the environment variable ``NWL_CPUS_PER_PROC``.
    threads_per_cpu : None | int
      Also set by the environment variable ``NWL_THREADS_PER_CPU``.
    gpus_per_process : None | int
      Also set by the environment variable ``NWL_GPUS_PER_PROC``.
    jobargs : None | list[str]
      Raw command line arguments used to run tool.
    inputs : None | dict | :class:`StructValued <partis.schema.StructValued>`
      Pre-parsed inputs to use
    inputs_file : None | str
      Path to raw input file that was used.
      If a relative path, it will be resolved relative to `workdir`.
    venv : :class:`ProcessEnv <partis.utils.venv.ProcessEnv`
      Virtual process environment to run any subprocesses.
      If not given, the current environment will be used.
    results_schema :
      Pre-generated results schema to use
    initlogs : list
      Logs to add to results that occurred before running tool
    Returns
    -------
    None
    """

    if self._configured:
      raise ValueError("Tool already configured")

    self._configured = True

    if log is not None:
      self._log = log.getChild(f"tool")
    else:
      self._log = logging.getLogger(f"tool")

    self._log_handler = LogListHandler()
    self._log.addHandler( self._log_handler )

    self._cmd_log = self._log.getChild("commands")
    self._cmd_log.propagate = False
    self._cmd_handler = LogListHandler()
    self._cmd_log.addHandler( self._cmd_handler )

    # issue non-command logs to child logger to prvent mixing
    self._runtime_log = self._log.getChild("runtime")

    self._pwd = osp.realpath( os.getcwd() )

    if workdir is None:
      workdir = self._pwd

    if rundir is None:
      rundir = workdir

    workdir = osp.realpath( workdir )

    rundir = osp.realpath( rundir )

    self._workdir = workdir
    self._rundir = rundir

    if truncate is None:
      truncate = False

    self._truncate = truncate

    self._timeout = timeout


    self._results_file = osp.join( self._rundir, "nwl.tool.results.yml")
    self._results_file_tmp = self._results_file + ".tmp"

    self._nodefile = osp.join( self._rundir, "nwl.nodes")

    if results_schema is None:
      results_schema = self.results_schema()

    # create a default results object
    self._results = results_schema()

    if initlogs:
      self._results.runtime.logs += initlogs

    self._results.job.tool_qualname = self.qualname

    if jobargs:
      self._results.job.args = jobargs

    self._results.job.host = get_jobhost()
    self._results.job.user = get_jobuser()
    self._results.job.id = get_jobid()
    self._results.job.name = get_jobname()
    self._results.job.curdir = self._pwd

    # set initial runtime information
    self._results.runtime.workdir = self._workdir
    self._results.runtime.rundir = self._rundir

    self._results.runtime.host = get_runhost()
    self._results.runtime.pid = int(os.getpid())

    if env is not None:
      # strip out all 'weird' characters from environment variable names
      env = {
        re.sub( r'[^A-Za-z0-9\_]+', "_", k ) : v
        for k,v in env.items() }

      self._results.runtime.env = env

    if aux is not None:
      self._results.runtime.aux = aux

    # handles parsing/setting defaults from environment variables
    processes = get_processes( processes )
    nodes = get_nodelist( nodes )

    cpus_per_process = get_cpus_per_process( cpus_per_process )
    threads_per_cpu = get_threads_per_cpu( threads_per_cpu )
    gpus_per_process = get_gpus_per_process( gpus_per_process )
    mpiexec = get_mpiexec( mpiexec )

    if processes is not None:
      self._results.runtime.processes = processes

    if nodes is not None:
      self._results.runtime.nodes = nodes

    if cpus_per_process is not None:
      self._results.runtime.cpus_per_process = cpus_per_process

    if threads_per_cpu is not None:
      self._results.runtime.threads_per_cpu = threads_per_cpu

    if gpus_per_process is not None:
      self._results.runtime.gpus_per_process = gpus_per_process

    self._results.runtime.threads_per_process = (
      self._results.runtime.threads_per_cpu
      * self._results.runtime.cpus_per_process )

    if mpiexec:

      self._results.job.mpiexec = mpiexec

      if self._results.runtime.processes > 1:
        mpi_np = self._results.runtime.processes
        mpi_nodes = ','.join(self._results.runtime.nodes)

        mpi_kwargs = {
          'processes' : self._results.runtime.processes,
          'cpus_per_process' : self._results.runtime.cpus_per_process,
          'threads_per_cpu' : self._results.runtime.threads_per_cpu,
          'threads_per_process' : self._results.runtime.threads_per_process,
          'gpus_per_process' : self._results.runtime.gpus_per_process,
          'nodes' : None,
          'nodefile' : None }

        if len(self._results.runtime.nodes) > 0:
          mpi_kwargs['nodes'] = ','.join(self._results.runtime.nodes)
          mpi_kwargs['nodefile'] = self._nodefile

        _mpiexec = list()

        for arg in mpiexec:
          keys = [
            s[1]
            for s in Formatter().parse(arg)
            if s[1] is not None ]

          for k in keys:
            if k not in mpi_kwargs:
              self._runtime_log.error(f"Unknown MPI variable '{k}': {mpiexec}")
              break

            elif mpi_kwargs[k] is None:
              self._runtime_log.error(f"MPI variable '{k}' not set: {mpiexec}")
              break

          else:
            _mpiexec.append(arg.format(**mpi_kwargs))

        # add mpi invocation, if available and needed
        self._results.runtime.mpiexec = _mpiexec

    if self._results.runtime.threads_per_process > 1:
      if 'OMP_NUM_THREADS' not in self._results.runtime.env:
        self._results.runtime.env['OMP_NUM_THREADS'] = str(self._results.runtime.threads_per_process)

    if (
      not self.resources.multi_thread
      and self._results.runtime.threads_per_process > 1 ):

      self._runtime_log.warning(
        f"Tool doesn't support multi-threading: {self._results.runtime.threads_per_process}")

    if (
      not self.resources.multi_process
      and self._results.runtime.processes > 1 ):

      self._runtime_log.warning(
        f"Tool doesn't support multi-processing: {self._results.runtime.processes}")

    if self.resources.multi_process:
      if self._results.runtime.processes > 1:
        if (
          self.resources.multi_process_mpi
          and len(self._results.job.mpiexec) == 0 ):

          self._runtime_log.error(
            f"No MPI startup given, but tool requires MPI for processes > 1: {self._results.runtime.processes}")

        if (
          not self.resources.multi_node
          and len(self._results.runtime.nodes) > 1 ):

          self._runtime_log.warning(
            f"Tool doesn't support processing for len(nodes) > 1: {self._results.runtime.nodes}")

    else:
      if self._results.runtime.processes > 1:
        self._runtime_log.warning(
          f"Tool doesn't support processes > 1: {self._results.runtime.processes}")


    self._cmd_ids = list(self.commands.keys())
    self._results.runtime.cmd_index = -1
    self._results.runtime.cmd_id = None
    self._cur_cmd = None
    self._failed = False

    if venv is None:
      venv = ProcessEnv()

    self._venv = venv

    try:
      inputs_schema = self._results.data.inputs._schema

      if not ( inputs or inputs_file ):
        # default inputs
        inputs = inputs_schema.decode( inputs_schema.init_val )

      elif inputs_file:
        # load from file
        inputs = load(
          file = inputs_file,
          schema = inputs_schema,
          loc = inputs_file )

      else:
        # validate
        inputs = inputs_schema.decode(
          inputs,
          inputs_file )

      self._runtime_log.info(f"Inputs validated.")

      try:
        self._results.data.inputs = inputs._eval(
          context = InputsContext(
            results = self._results,
            static = self.resources.static ),
          logger = self._runtime_log.getChild("inputs") )

        try:
          logs = self.prolog._eval(
            context = LogContext(
              results = self._results,
              static = self.resources.static ),
            logger = self._runtime_log.getChild("prolog") )

          # filter for only enabled log events
          for l in logs:
            if l.enabled:
              self._runtime_log.log( logging.getLevelName(l.level), l.msg )

          missing_files = check_inout_files(
            dir = self._workdir,
            path = [ 'data', 'inputs', ],
            val = self._results.data.inputs )

          if len( missing_files ) > 0:
            self._runtime_log.warning( ModelHint(
              msg = f"Input files not found: {len(missing_files)}",
              hints = missing_files ) )

        except Exception as e:
          self._runtime_log.error( ModelHint(
            msg = f"Tool prolog evaluation failed",
            hints = e ) )

      except Exception as e:
        self._runtime_log.error( ModelHint(
          msg = f"Tool inputs evaluation failed",
          hints = e ) )

    except Exception as e:
      self._runtime_log.error( ModelHint(
        msg = f"Tool inputs loading failed",
        hints = e ) )

    self._update_result_logs()

  #-----------------------------------------------------------------------------
  def _update_result_logs( self ):
    if self._log_handler is None:
      return

    self._results.runtime.logs += self._log_handler.logs
    self._log_handler.clear()

    # command fails if any prolog event of 'ERROR' or 'CRITICAL'
    self._failed = self._failed or any(
      l['level'] in [ 'ERROR', 'CRITICAL' ]
      for l in self._results.runtime.logs )

  #-----------------------------------------------------------------------------
  def _save_results( self ):
    if not self._opened:
      raise ValueError("Tool never opened")

    try:

      try:
        dump(
          self._results_file_tmp,
          self._results,
          add_hash = True )

        os.replace(
          self._results_file_tmp,
          self._results_file )

      except Exception as e:
        self._runtime_log.error( ModelHint(
          msg = f"Failed to write tool result file",
          hints = e ) )

    except Exception as e:
      self._runtime_log.error( ModelHint(
        msg = f"Failed to encode tool result document",
        hints = e ) )

  #-----------------------------------------------------------------------------
  def _open( self ):
    """Begin tool execution

    Returns
    -------
    None
    """

    if not self._configured:
      raise ValueError("Tool never configured")

    if self._opened:
      raise ValueError("Tool already opened")

    self._opened = True

    try:
      if not osp.exists( self._rundir ):
        os.makedirs( self._rundir )

      elif self._truncate:
        shutil.rmtree( self._rundir )
        os.mkdir( self._rundir )

      if osp.exists( self._results_file ):
        os.remove( self._results_file )

      os.chdir( self._rundir )

      if len(self._results.runtime.nodes) > 0:
        with open(self._nodefile, 'w') as fp:
          fp.write('\n'.join(self._results.runtime.nodes))

    except Exception as e:
      self._runtime_log.error( ModelHint(
        msg = f"Failed to prepare tool runtime directory: {self._rundir}",
        hints = e ) )

    self._update_result_logs()

    self._save_results()

    if self._failed:
      return

    self._open_next_cmd()

  #-----------------------------------------------------------------------------
  def _open_next_cmd( self ):
    """Execute the next available command

    Returns
    -------
    None
    """

    if self._cur_cmd:
      self._cur_cmd._reset()

    self._cur_cmd = None

    while (
      self._cur_cmd is None
      and len(self.commands) > ( self._results.runtime.cmd_index + 1 ) ):

      self._results.runtime.cmd_index += 1
      self._results.runtime.cmd_id = self._cmd_ids[ self._results.runtime.cmd_index ]

      self._cmd_handler.clear()

      try:
        cmd = self.commands[ self._results.runtime.cmd_id ]

        self._cur_cmd = cmd._eval(
          context = CommandsContext(
            results = self._results,
            static = self.resources.static ),
          logger = self._cmd_log.getChild( self._results.runtime.cmd_id ) )

        self._results.data.commands[ self._results.runtime.cmd_id ].enabled = self._cur_cmd.enabled

        if not self._cur_cmd.enabled:
          # non-enabled commands considered successful
          self._results.data.commands[ self._results.runtime.cmd_id ].success = True

          self._runtime_log.info(
            f"Command skipped (not enabled): `{self._results.runtime.cmd_id}`")

          # keep looping to find next enabled command
          self._cur_cmd = None

      except SchemaError as e:
        self._runtime_log.error( ModelHint(
          msg = f"Command evaluation failed: `{self._results.runtime.cmd_id}`",
          hints = e ) )

        self._cur_cmd = None
        return

    if self._cur_cmd is None:
      # no more commands
      return

    # configure command
    res = self._cur_cmd._config(
      tool = self,
      workdir = self._results.runtime.workdir,
      rundir = self._results.runtime.rundir,
      env = self._results.runtime.env,
      venv = self._venv,
      id = self._results.runtime.cmd_id,
      tool_results = self._results,
      timeout = self._timeout,
      log = self._cmd_log )

    # check status of 'prolog' events before opening command
    self._results.data.commands[ self._results.runtime.cmd_id ] = res

    if self._cur_cmd._failed:
      # check `_failed` instead of `res.success`, since `success` is only set to
      # true when the command closes successfuly
      self._runtime_log.error(
        ModelHint(
          f"Command failure reported: `{self._results.runtime.cmd_id}`",
          hints = self._cmd_handler.hints ) )

      if self._cur_cmd:
        self._cur_cmd._reset()

      self._cur_cmd = None
      return

    self._save_results()

    self._cur_cmd._open(
      tool_results = self._results )

  #-----------------------------------------------------------------------------
  def _poll( self ):
    """Monitor tool for completion.

    If completed, will automatically close the command and return final results.

    Returns
    -------
    results : None | dict
    """

    if not self._opened:
      raise ValueError("Tool never opened")

    if self._closed:
      raise ValueError("Tool already closed")

    if self._cur_cmd is None:
      # no more commands
      return self._close()

    res = self._cur_cmd._poll(
      tool_results = self._results )

    if res is None:
      # command not complete
      return None

    # check status of 'epilog' events after command completes
    self._results.data.commands[ self._results.runtime.cmd_id ] = res

    if not res.success:
      self._runtime_log.error(
        ModelHint(
          f"Command failure reported: `{self._results.runtime.cmd_id}`",
          hints = self._cmd_handler.hints ) )

      return self._close()

    self._runtime_log.info(
      ModelHint(
        f"Command finished: `{self._results.runtime.cmd_id}`",
        hints = self._cmd_handler.hints ) )

    self._open_next_cmd()

    if self._cur_cmd is None:
      # no more commands
      return self._close()

    else:
      return None

  #-----------------------------------------------------------------------------
  def _close( self ):
    # finished commands

    if not self._opened:
      raise ValueError("Tool never opened")


    if self._closed:
      raise ValueError("Tool already closed")

    self._closed = True

    if self._cur_cmd:
      self._cur_cmd._reset()
      self._cur_cmd = None

    # tool fails if any log event of 'ERROR' or 'CRITICAL'
    self._update_result_logs()

    if not self._failed:
      eval_log = self._log.getChild('outputs')
      eval_log.propagate = False
      eval_handler = LogListHandler()
      eval_log.addHandler( eval_handler )

      try:

        self._results.data.outputs = self._results.data.outputs._eval(
          context = OutputsContext(
            results = self._results,
            static = self.resources.static ),
          logger = eval_log )

        self._runtime_log.info(
          ModelHint(
            f"Outputs evaluated",
            hints = eval_handler.hints ) )

      except Exception as e:
        self._runtime_log.error( ModelHint(
          msg = f"Tool outputs evaluation failed",
          hints = eval_handler.hints + [e] ) )

        self._failed = True

      finally:
        eval_log.removeHandler(eval_handler)

    if not self._failed:
      missing_files = check_inout_files(
        dir = self._rundir,
        path = [ 'data', 'outputs', ],
        val = self._results.data.outputs )

      if len( missing_files ) > 0:
        self._failed = True

        self._runtime_log.error( ModelHint(
          msg = f"Output files not found: {len(missing_files)}",
          hints = missing_files ) )

    if not self._failed:
      # check epilogs
      try:
        logs = self.epilog._eval(
          context = LogContext(
            results = self._results,
            static = self.resources.static ),
          logger = self._runtime_log.getChild("epilog") )

        # filter for only enabled log events
        for l in logs:
          if l.enabled:
            self._runtime_log.log( logging.getLevelName(l.level), l.msg )

      except Exception as e:
        self._runtime_log.error( ModelHint(
          msg = f"Tool epilog evaluation failed",
          hints = e ) )

    self._update_result_logs()

    # finally set the success to True only if never failed
    self._results.runtime.success = not self._failed

    self._save_results()

    # return to initial working directory when finished
    os.chdir( self._pwd )

    return self._results

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  async def run( self, **kwargs ):

    import trio

    self._config( **kwargs )

    result = None
    self._open()

    while result is None:
      await trio.sleep( 0.2 )

      result = self._poll()

    return result

  #-----------------------------------------------------------------------------
  def run_wait( self, **kwargs ):
    import trio
    from functools import partial

    results = trio.run( partial( self.run, **kwargs ) )

    return results

  #-----------------------------------------------------------------------------
  def lint( self, results = None ):

    if results is None:
      # create a default results object
      results = self.results_schema()()

    hints = list()

    hints.extend( results.data.inputs._lint(
      context = InputsContext(
        results = results,
        static = self.resources.static ) ) )

    hints.extend( self.prolog._lint(
      context = LogContext(
        results = results,
        static = self.resources.static ) ) )

    for cmd_id, cmd in self.commands.items():

      hints.extend( cmd.lint( self, cmd_id, results ) )


    hints.extend( results.data.outputs._lint(
      context = OutputsContext(
        results = results,
        static = self.resources.static ) ) )

    hints.extend( self.epilog._lint(
      context = LogContext(
        results = results,
        static = self.resources.static ) ) )

    return hints
