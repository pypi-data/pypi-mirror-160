# -*- coding: UTF-8 -*-
"""NWL Tool runner

example usage:

  partis-nwl [tool_name] [inputs_file]

"""

import sys
import os
import os.path as osp
import re
from pprint import pformat
from copy import copy
import time
import argparse
from argparse import RawTextHelpFormatter
import logging
import traceback
import zipfile
import shutil
import tempfile
import importlib
import subprocess

import datetime
from timeit import default_timer as timer

from partis.pyproj import (
  norm_dist_filename )

from partis.utils import (
  init_logging,
  log_levels,
  getLogger,
  LogListHandler,
  ModelHint,
  VirtualEnv,
  MutexFile )

log = getLogger(__name__)

from .tool import (
  Tool )

from .testing import (
  Test,
  TestSuite,
  TestSuiteResults )

from .utils import (
  detect_run_with_mpi,
  get_mpiexec,
  get_processes,
  get_cpus_per_process,
  get_threads_per_cpu,
  get_gpus_per_process )

from partis.schema import (
  is_mapping,
  SchemaHint,
  SchemaError,
  Loc,
  SeqPrim,
  SchemaModule )

from partis.schema.serialize.yaml import (
  load,
  dump,
  dumps )

from partis.nwl.tool_pkg.build import build as build_pkg

from .results import (
  ToolResults )

from .utils import (
  get_mpiexec,
  get_processes,
  get_cpus_per_process,
  get_threads_per_cpu,
  get_gpus_per_process,
  get_runhost,
  get_jobhost,
  get_jobuser,
  get_jobid,
  get_jobname )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def argument_parser( ):

  """Parse for commandline arguments.
  """

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  parser.add_argument( "tool_name",
    type = str,
    nargs = '?',
    default = None,
    help = "Tool file or qualified name" )

  parser.add_argument( "inputs_file",
    type = str,
    default = None,
    nargs = '?',
    help = "Tool inputs. An empty string will result in using tool default input values" )

  parser.add_argument( "--tool",
    type = str,
    default = None,
    # dest = 'tool_name',
    help = "Alias for tool_name" )


  parser.add_argument( "--inputs",
    type = str,
    default = None,
    # dest = 'inputs_file',
    help = "Alias for inputs_file" )

  parser.add_argument( "--template",
    action='store_true',
    help = "Generate template tool inputs file using default values instead of running tool." )

  parser.add_argument( "-d", "--rundir",
    type = str,
    default = None,
    help = "Run directory, relative path for output files" )

  parser.add_argument( "-c", "--workdir",
    type = str,
    default = None,
    help = "Working directory, relative path for input files" )

  parser.add_argument( "-e", "--environ",
    type = str,
    default = None,
    help = """Specify alternate environment variables.
      If not specified, the processes will inherit the current environment.
      If an empty string, the current environment will be discarded.
      If a file path, the file should be a YAML file with key-value pairs to use
      for the environment dictionary.""" )

  parser.add_argument( "--aux",
    type = str,
    default = list(),
    metavar="KEY=VALUE",
    nargs='+',
    help = "Auxiliary variables that may be used for input query substitution" )

  parser.add_argument( "-t", "--timelimit",
    type = int,
    default = None,
    help = "Time limit before killing process (seconds)" )

  parser.add_argument( "--np",
    type = int,
    default = None,
    help = "Number of processes" )

  parser.add_argument( "--ncp",
    type = int,
    default = None,
    help = "Number of cpus per process" )

  parser.add_argument( "--ntc",
    type = int,
    default = None,
    help = "Number of logical threads per cpu (usually 1 or 2)" )

  parser.add_argument( "--ngp",
    type = int,
    default = None,
    help = "Number of gpus per process" )

  parser.add_argument( "--doc",
    action='store_true',
    help = "Print extra tool documentation" )

  # parser.add_argument( "--test",
  #   type = str,
  #   default = list(),
  #   action = 'append',
  #   help = "Tool test files" )

  parser.add_argument( "--mpiexec",
    type = str,
    default = None,
    help = "List of commands to execute a program within MPI, if available" )

  parser.add_argument( "--truncate",
    default = False,
    action='store_true',
    help = "Clears run directory before starting job" )

  parser.add_argument( "-l", "--log",
    type = str,
    default = None,
    help = "Redirect output to the given log file" )

  parser.add_argument( "-v", "--verbosity",
    type = str,
    default = 'info',
    help = f"Log verbosity {log_levels}" )

  parser.add_argument( "--venv",
    type = str,
    default = None,
    help = """Specified path to create, or re-use, a virtual environment
      for installing tool packages.
      If not given, one will be created in the tool run directory.""" )

  parser.add_argument( "--venv-force",
    default = False,
    action='store_true',
    help = """Forces the creation of a new virtual environment, even if an existing
      one with the same name is found.""" )

  parser.add_argument( "--venv-in",
    type = str,
    default = list(),
    action = 'append',
    help = """Inherit the 'site-packages' from one or more existing virtual environment(s).""" )

  parser.add_argument( "-f", "--find-links",
    type = str,
    default = list(),
    action = 'append',
    help = """Search location to find installable tool packages. The current
      directory is automatically added.""" )

  return parser

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def parse_key_values( raw_vars ):
  vars = dict()

  for kv in raw_vars:
    parts = kv.split('=', 1)

    if len(parts) > 1:

      k = parts[0].strip()
      v = parts[1].strip()

      vars[k] = v

  return vars

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def load_tool(
  name,
  logger,
  venv,
  find_links ):

  tool_mod = None
  deps_installed = False
  tmpdir = None
  _find_links = list()


  if logger.isEnabledFor( logging.DEBUG ):
    _verbosity = ['-v', '-v', '-v']
  else:
    _verbosity = list()

  _pip_args = [
    # the cache is not safe when changed from multiple processes
    '--no-cache-dir',
    # not going to upgrade pip here
    '--disable-pip-version-check',
    # no user interaction
    '--no-input' ]


  try:
    if osp.isfile( name ):

      tool_name = norm_dist_filename( osp.basename( name ).rsplit('.', 1)[0] )
      _name = f"nwlpkg_{tool_name}.{tool_name}"

      try:
        with venv:
          tool_mod = importlib.import_module(_name)

        name = _name

        tool = tool_mod.tool

        results_schema = tool_mod.results.results

      except ImportError:


        logger.info(f'Building tool package: {name}')

        tmpdir = tempfile.mkdtemp()

        find_links.append( tmpdir )

        import trio
        from functools import partial

        pkg_name = trio.run( partial( build_pkg,
          tool_file = name,
          outdir = tmpdir,
          logger = logger,
          build_docs = False ) )

        name = f"{pkg_name}.{tool_name}"

    logger.info(ModelHint(
      f'PIP Links',
      hints = find_links ) )

    for f in ['.'] + find_links:
      logger.info(f"  '{f}'")

      _find_links.extend([
        '--find-links',
        f ])

    try:
      with venv:
        tool_mod = importlib.import_module(name)

      tool = tool_mod.tool

      results_schema = tool_mod.results.results

    except ImportError:
      pass

    if not tool_mod:

      # search current directory for a distribution containing the tool
      pkg, _, mod = name.partition('.')

      logger.info(f"Installing tool package: {pkg}")

      try:

        venv.install([
            *_verbosity,
            *_find_links,
            *_pip_args,
            f'{pkg}[run]' ],
          env = {
            **os.environ,
            'PIP_NO_BUILD_ISOLATION' : 'True' })

      except subprocess.CalledProcessError:
        logger.error(
          f"Failed to install tool package: {pkg}")

        return None, None

      deps_installed = True

      with venv:
        tool_mod = importlib.import_module(name)

      tool = tool_mod.tool

      results_schema = tool_mod.results.results

    tool_dir = osp.dirname( osp.abspath(tool_mod.__file__) )
    data_dir = osp.join( tool_dir, os.pardir, 'data' )

    # update tool resource data paths
    for name, data in tool.resources.static.items():
      data_path = data.path

      if not osp.isabs( data_path ):
        tool.resources.static[name] = osp.join( data_dir, data_path )

    if not deps_installed and len(tool.resources.python.dependencies) > 0:
      # ensure all tool dependencies are installed
      try:
        venv.install([
            '--upgrade',
            *_verbosity,
            *_find_links,
            *_pip_args,
            *[ str(dep) for dep in tool.resources.python.dependencies ] ],
          env = {
            **os.environ,
            'PIP_NO_BUILD_ISOLATION' : 'True' })

      except subprocess.CalledProcessError:
        logger.error(
          f"Failed to install tool dependencies: {pkg}")

        return None, None

  finally:
    if tmpdir:
      shutil.rmtree( tmpdir )

  return tool, results_schema

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def dump_error_results(
  log,
  log_handler,
  workdir,
  rundir,
  aux ):


  if not osp.exists( rundir ):
    os.makedirs(rundir)

  results_file = osp.join( rundir, "nwl.tool.results.yml" )

  results = ToolResults()

  results.job.args = sys.argv

  results.job.id = get_jobid()
  results.job.name = get_jobname()

  results.job.host = get_jobhost()
  results.job.user = get_jobuser()

  results.runtime.workdir = workdir
  results.runtime.rundir = rundir
  results.runtime.aux = aux

  env = os.environ

  env = {
    re.sub( r'[^A-Za-z0-9\_]+', "_", k ) : v
    for k,v in env.items() }

  results.runtime.env = env

  results.runtime.logs = log_handler.logs

  try:

    try:

      dump(
        results_file,
        results,
        add_hash = True )

    except Exception as e:
      log.error( ModelHint(
        msg = f"Failed to write tool result file",
        hints = e ) )

  except Exception as e:
    log.error( ModelHint(
      msg = f"Failed to encode tool result document",
      hints = e ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def positional_defaults(*args, **kwargs):

  # filter out positional arguments that are None
  pos_args = [ v for v in args if v is not None ]

  for k,v in kwargs.items():

    if v is None and len(pos_args):
      kwargs[k] = pos_args.pop(0)

  return kwargs

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def run_tool( log, tool_log, args ):

  if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

  # keep complete record of runner log in case tool fails
  log_handler = LogListHandler()
  log.addHandler( log_handler )

  # extract from either positional or named arguments
  tool_name, inputs_file = positional_defaults(
    args.tool_name,
    args.inputs_file,
    tool_name = args.tool,
    inputs_file = args.inputs ).values()

  pwd = osp.abspath( os.getcwd() )
  workdir = args.workdir
  rundir = args.rundir
  venv_dir = args.venv

  if not workdir:
    workdir = pwd

  if not rundir:
    rundir = workdir

  if not venv_dir:
    venv_dir = osp.join( rundir, 'venv_nwlrun' )

  workdir = osp.abspath( workdir )

  rundir = osp.abspath( rundir )

  venv_dir = osp.abspath( venv_dir )

  find_links = [
    osp.abspath(p) for p in args.find_links ]

  # extract any auxiliary variables
  aux = parse_key_values( args.aux )

  venv = None
  returncode = 0
  tool_closed = False

  if tool_name is None:
    log.error(
      f"tool_name is required")

    dump_error_results(
      log = log,
      log_handler = log_handler,
      workdir = workdir,
      rundir = rundir,
      aux = aux )

    return 1

  log.info(f'Tool name: {tool_name}')
  log.info(f'Inputs file: {inputs_file}')
  log.info(f'Working dir: {workdir}')
  log.info(f'Run dir: {rundir}')
  log.info(f'Venv dir: {venv_dir}')

  try:
    # determine environment variables
    if args.environ is None:
      # inherit
      env = os.environ

    elif args.environ == '':
      # scrub
      env = dict()

    else:
      # load from YAML file
      env = load(
        file = args.environ,
        loc = Loc(
          filename = args.environ ) )

      if not (
        is_mapping( env )
        and all(
          isinstance(k, str) and isinstance(v, str)
          for k,v in env.items() ) ):

        returncode = 1
        log.error(
          f"`environ` file must be a single-level mapping: {args.environ}\n{env}" )



    # create/re-use virtual environment to install any packages

    venv_in = args.venv_in

    venv_mutex = MutexFile(
        prefix = osp.basename(venv_dir),
        dir = osp.dirname(venv_dir),
        # 10 min
        timeout = 600.0 )

    venv = VirtualEnv(
      path = venv_dir,
      inherit_site_packages = venv_in,
      reuse_existing = not args.venv_force,
      args = ['--without-pip'],
      logger = log,
      mutex = venv_mutex )

    tool, results_schema = load_tool(
      name = tool_name,
      logger = log,
      venv = venv,
      find_links = find_links )

    if not tool and ( args.venv_in or not args.venv_force ):
      # install failed. Attempt again, but with no re-use or inheritance
      # from other environments
      # NOTE: non-install errors will have raised an exception instead of
      # returning None
      # NOTE: existing install(s) may lead to incompatible dependencies
      log.warning(f"Re-initializing virtual environment without inhertied 'site-packages'")
      venv_in = list()

      venv = VirtualEnv(
        path = venv_dir,
        inherit_site_packages = venv_in,
        reuse_existing = False,
        args = ['--without-pip'],
        logger = log,
        mutex = venv_mutex )

      tool, results_schema = load_tool(
        name = tool_name,
        logger = log,
        venv = venv,
        find_links = find_links )

    if not tool:
      returncode = 1

    if returncode == 0:
      with venv:
        # NOTE: using venv as context will update 'os.environ['PATH'] and sys.path
        # to approximate the environment seen by an interpreter run in the venv

        # ensure plugs reloaded with access to additional search paths
        from partis.schema.plugin import (
          schema_plugins )

        schema_plugins.load_plugins()

        log.info(f'Loaded tool: {tool_name}')

        if args.doc:
          log.info( "Input Schema" )
          log.info( results_schema.data.inputs.__doc__)
          log.info( "Output Schema" )
          log.info( results_schema.data.outputs.__doc__)
          log.info( "Commands Output Schema" )
          log.info( results_schema.data.commands.__doc__)

        if args.template:
          init_val = results_schema.data.inputs.schema.init_val

          log.info( dumps(init_val) )

          if inputs_file:
            dump( inputs_file, init_val )

            log.info(f"Tool inputs template generated: {inputs_file}")

        elif inputs_file is not None:
          # run tool
          result = tool.run_wait(
            workdir = workdir,
            rundir = rundir,
            env = env,
            venv = venv,
            aux = aux,
            timeout = args.timelimit,
            truncate = args.truncate,
            mpiexec = args.mpiexec,
            processes = args.np,
            cpus_per_process = args.ncp,
            threads_per_cpu = args.ntc,
            gpus_per_process = args.ngp,
            inputs_file = inputs_file,
            jobargs = sys.argv,
            results_schema = results_schema,
            log = tool_log,
            initlogs = log_handler.logs )

          tool_closed = True
          returncode = 0 if result.runtime.success else 1

  except Exception as e:
    # catch any errors not caught by the tool

    returncode = 1
    log.error( ModelHint(
      "Tool runtime failure",
      hints = e ) )

  if inputs_file is not None and not ( args.template or tool_closed ):

    dump_error_results(
      log = log,
      log_handler = log_handler,
      workdir = workdir,
      rundir = rundir,
      aux = aux )

  return returncode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# def run_tests():
#
#   if returncode == 0 and len(args.test) > 0:
#
#     try:
#       test_suite = TestSuite()
#
#       for i, ftest in enumerate( args.test ):
#         with open( ftest, 'r' ) as fp:
#           doc = fp.read()
#
#         test_suite.tests[ str(i) ] = loads(
#           src = doc,
#           schema = TestSuite,
#           loc = Loc(
#             filename = ftest ) )
#
#       if len( test_suite.tests ) > 0:
#         test_results = test_suite._run_wait(
#           logger = log,
#           workdir = args.workdir,
#           rundir = args.rundir )
#
#         log.info(f"Tests: {test_results.npass} passed, {test_results.nfail} failed")
#
#         if not test_results.success:
#           returncode = 1
#
#           # TODO: give the option to save results somewhere
#           failed = list()
#           stack = list( test_results.tests.items() )
#
#           while len(stack) > 0:
#             path, test = stack.pop(0)
#
#             if not test.success:
#               if isinstance( test, TestSuiteResults ):
#                 for k, _test in test.tests.items():
#                   stack.append( (f"{path}.{k}", _test) )
#
#               else:
#                 failed.append( ( path, test ) )
#
#           for path, test in failed:
#             log.info(f"{path}\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#             for l in test.logs:
#               log.log( logging.getLevelName(l.level), l.msg )
#             log.info(f"{path}\n------------------------------------------------------------------\n")
#
#     except Exception as e:
#       returncode = 1
#       log.exception( "Tool test failure" )
#
#   return returncode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

  parser = argument_parser( )
  args = parser.parse_args( )

  init_logging(
    level = args.verbosity,
    filename = args.log )

  tool_log = getLogger(f"nwl")
  log = tool_log.getChild("run")

  if detect_run_with_mpi():
    log.error(
      f"NWL tool should not be launched directly by an MPI startup program."
      " Set '--mpiexec', or 'NWL_MPIEXEC', with needed MPI launch command and argument template string.")
    return 1

  time_start = timer()

  returncode = run_tool( log, tool_log, args )

  time_end = timer()
  walltime = time_end - time_start

  if returncode != 0:
    log.error(f"Job exited with errors: wall-time {datetime.timedelta(seconds = walltime)} (H:M:S)")
  else:
    log.info(f"Job completed successfully: wall-time {datetime.timedelta(seconds = walltime)} (H:M:S)")

  return returncode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
  exit( main() )
