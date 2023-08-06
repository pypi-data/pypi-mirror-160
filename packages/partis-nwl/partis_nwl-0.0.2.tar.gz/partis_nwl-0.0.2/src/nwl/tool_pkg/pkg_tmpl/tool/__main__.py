# -*- coding: UTF-8 -*-
"""Tool runner utility

"""

from pprint import pformat
from copy import copy
import time
import os
import sys
import argparse
from argparse import RawTextHelpFormatter
import logging
import traceback

import datetime
from timeit import default_timer as timer

from partis.utils import (
  init_logging,
  log_levels,
  ModelHint )

log = logging.getLogger(__name__)

from partis.nwl.utils import (
  get_mpiexec,
  get_processes,
  get_cpus_per_process,
  get_threads_per_cpu,
  get_gpus_per_process )

from partis.schema import (
  SchemaHint,
  SchemaError,
  Loc,
  SeqPrim )

from partis.schema.serialize.yaml import (
  load,
  dump )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def argument_parser( ):

  """Parse for commandline arguments.
  """

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  parser.add_argument( "-d", "--rundir",
    type = str,
    default = None,
    help = "Run directory" )

  parser.add_argument( "-c", "--workdir",
    type = str,
    default = None,
    help = "Current working directory" )

  parser.add_argument( "-e", "--environ",
    type = bool,
    default = True,
    help = "Whether to preserve current environment" )

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
    help = "Number of cores per process" )

  parser.add_argument( "--ntc",
    type = int,
    default = None,
    help = "Number of threads per core" )

  parser.add_argument( "--ngp",
    type = int,
    default = None,
    help = "Number of gpus per process" )

  parser.add_argument( "--tool",
    type = str,
    default = None,
    help = "Tool file" )

  parser.add_argument( "--inputs",
    type = str,
    default = None,
    help = "Tool inputs" )

  parser.add_argument( "--template",
    type = str,
    default = None,
    help = "Generate template tool inputs file using default values." )

  parser.add_argument( "--doc",
    default = False,
    action='store_true',
    help = "Print extra tool documentation" )

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

  return parser

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def main():

  job = None
  returncode = 0
  time_start = timer()

  parser = argument_parser( )
  args = parser.parse_args( )

  init_logging(
    level = args.verbosity,
    filename = args.log )

  if not ( args.doc or args.template or args.inputs ):
    log.error(f"No actions to take,  must specify one of '--doc', '--template', or '--inputs'.")
    return

  from . import (
    tool,
    inputs,
    outputs,
    commands,
    results )

  if args.doc:
    log.info( "Input Schema" )
    log.info( inputs.inputs_schema.__doc__)
    log.info( "Output Schema" )
    log.info( outputs.outputs_schema.__doc__)
    log.info( "Commands Output Schema" )
    log.info( commands.commands_schema.__doc__)

  elif args.template is not None:
    init_val = inputs.inputs_schema.init_val

    doc = dump( args.template, init_val )

    log.info(f"Tool inputs template generated: {args.template}")

  elif args.inputs is not None:

    try:
      inputs = load(
        file = args.inputs,
        schema = inputs.inputs_schema,
        loc = Loc(
          filename = args.inputs ) )

    except SchemaError as e:
      log.error("Inputs validation errors:")
      log.error(e.fmt(), exc_info = True )

      returncode = 1

    else:
      log.info(f"Inputs validation passed: {args.inputs}")

      if args.mpiexec is not None:
        os.environ['NWL_MPIEXEC'] = str(args.mpiexec)

      if args.np is not None:
        os.environ['NWL_PROCS'] = str(args.np)

      if args.ncp is not None:
        os.environ['NWL_CPUS_PER_PROC'] = str(args.ncp)

      if args.ntc is not None:
        os.environ['NWL_THREADS_PER_CPU'] = str(args.ntc)

      if args.ngp is not None:
        os.environ['NWL_GPUS_PER_PROC'] = str(args.ngp)


      try:

        result = tool.run_wait(
          inputs = inputs,
          workdir = args.workdir,
          rundir = args.rundir,
          env = dict( os.environ ) if args.environ else dict(),
          timeout = args.timelimit,
          truncate = args.truncate,
          mpiexec = get_mpiexec( args.mpiexec ),
          processes = get_processes( args.np ),
          cpus_per_process = get_cpus_per_process( args.ncp ),
          threads_per_cpu = get_threads_per_cpu( args.ntc ),
          gpus_per_process = get_gpus_per_process( args.ngp ) )

        returncode = 0 if result.runtime.success else 1

      except Exception as e:
        returncode = 1
        log.error( "Tool runtime failure", exc_info = True )

  time_end = timer()
  walltime = time_end - time_start

  if returncode != 0:
    log.error(f"Job exited with errors: wall-time {datetime.timedelta(seconds = walltime)} (H:M:S)")
  else:
    log.info(f"Job completed successfully: wall-time {datetime.timedelta(seconds = walltime)} (H:M:S)")

  return returncode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
if __name__ == "__main__":
  exit( main() )
