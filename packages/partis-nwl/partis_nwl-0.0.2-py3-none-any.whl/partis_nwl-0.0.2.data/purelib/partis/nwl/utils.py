import os
import os.path as osp
import re
import shlex
import shutil
from glob import glob
import hashlib
import pathlib
import platform

from partis.utils import (
  join_attr_path )

from partis.schema import (
  is_sequence,
  is_mapping,
  SchemaDetectionError )

from .inputs import (
  PathInputValue )

from .outputs import (
  PathOutputValue )

from partis.schema.serialize import (
  yaml,
  json )

env_var_rec = re.compile(r'\${?(\w+)}?')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def expand_environ( var ):
  e_var = osp.expandvars(var)

  while e_var != var:
    var = e_var
    e_var = osp.expandvars(var)

  return shlex.split( e_var )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def detect_run_with_mpi():
  for var in [
    'OMPI_COMM_WORLD_SIZE',
    'PMI_SIZE']:

    if var in os.environ:
      return True

  return False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_mpiexec( mpiexec_str = None ):
  mpiexec = None

  if mpiexec_str is None and 'NWL_MPIEXEC' in os.environ:
    mpiexec_str = os.environ['NWL_MPIEXEC']

  if mpiexec_str is not None:
    mpiexec = expand_environ( mpiexec_str )

  if mpiexec is None:
    exe = shutil.which('mpiexec')

    if exe is not None:
      mpiexec = [
        'mpiexec',
        '-n', '{processes}',
        '-host', '{nodes}' ]

  return mpiexec

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_processes( val = None ):

  if val is None:
    for var in [
      'NWL_PROCS',
      'SLURM_NTASKS',
      'PBS_NP' ]:

      if var in os.environ:
        val = os.environ[var]

        if val:
          break

  if val is not None:
    val = int(val)

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_cpus_per_process( val = None ):

  if val is None:
    for var in [
      'NWL_CPUS_PER_PROC',
      'SLURM_CPUS_PER_TASK' ]:

      if var in os.environ:
        val = os.environ[var]

        if val:
          break

  if val is not None:
    val = int(val)

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_threads_per_cpu( val = None ):

  if val is None:
    for var in [
      'NWL_THREADS_PER_CPU' ]:

      if var in os.environ:
        val = os.environ[var]

        if val:
          break

  if val is not None:
    val = int(val)

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_gpus_per_process( val = None ):

  if val is None:
    for var in [
      'NWL_GPUS_PER_PROC' ]:

      if var in os.environ:
        val = os.environ[var]

        if val:
          break

  if val is not None:
    val = int(val)

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_runhost( val = None ):

  if val is None:
    val = platform.node()

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_jobhost( val = None ):

  if val is None:

    for var in [
      'NWL_JOBHOST',
      'SLURM_SUBMIT_HOST',
      'PBS_O_HOST']:

      if var in os.environ:
        val = os.environ[var]
        break

  if val is None:
    val = get_runhost()

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_nodelist( val = None ):
  if val is None:

    for var, isfile in [
      ( 'NWL_NODELIST', False ),
      ( 'NWL_NODEFILE', True ),
      ( 'SLURM_JOB_NODELIST', False ),
      ( 'PBS_NODEFILE', True ) ]:

      if var in os.environ:
        val = os.environ[var]

        if isfile:
          with open(val, 'rb') as fp:
            val = fp.read().decode('utf-8', errors = 'replace')

        break

  if isinstance(val, str):
    val = [ n.strip() for n in re.split(r'[\s,]', val) ]
    val = [ n for n in val if len(n) > 0 ]

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_runuser( val = None ):

  if val is None:
    val = os.getlogin()

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_jobuser( val = None ):

  if val is None:

    for var in [
      'NWL_JOBUSER',
      'SLURM_JOB_USER',
      'PBS_O_LOGNAME' ]:

      if var in os.environ:
        val = os.environ[var]
        break

  if val is None:
    val = get_runuser()

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_jobid( val = None ):
  if val is None:
    for var in [
      'NWL_JOBID',
      'SLURM_JOBID',
      'SLURM_JOB_ID',
      'PBS_JOBID' ]:

      if var in os.environ:
        val = os.environ[var]
        break

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_jobname( val = None ):
  if val is None:
    for var in [
      'NWL_JOBNAME',
      'SLURM_JOB_NAME',
      'PBS_JOBNAME' ]:

      if var in os.environ:
        val = os.environ[var]
        break

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def check_inout_files( dir, path, val ):

  missing = list()

  if isinstance( val, (PathInputValue, PathOutputValue) ):
    if len(val.path) > 0 and not osp.exists( val.path ):
      missing.append(
        f"{join_attr_path(path)}: {shlex.quote(osp.realpath(val.path))}" )

  elif is_sequence( val ):
    for i, v in enumerate(val):
      missing.extend( check_inout_files(
        dir = dir,
        path = path + [i],
        val = v ) )

  elif is_mapping( val ):
    for k, v in val.items():
      missing.extend( check_inout_files(
        dir = dir,
        path = path + [k],
        val = v ) )

  return missing

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def load_results( rundir = None ):
  results_file = "nwl.tool.results.yml"

  if rundir:
    results_file = osp.join( rundir, results_file )

  # ensure plugs reloaded with access to additional search paths
  from partis.schema.plugin import (
    schema_plugins )

  schema_plugins.load_plugins()

  results = yaml.load(
    results_file,
    loc = results_file,
    detect_schema = True )

  return results
