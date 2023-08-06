
import sys
import os
import subprocess
import re
import tempfile
import shutil
import base64
import difflib
import trio
import logging

import ruamel.yaml

from partis.utils.async_trio import (
  wait_all )

from partis.utils import (
  ModelHint,
  ModelError,
  checksum,
  fmt_base_or_type,
  indent_lines,
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
  PassPrim,
  StructValued,
  schema_declared,
  SchemaHint,
  SchemaError,
  Loc,
  Hint,
  HintList )

from partis.schema.prim.any_prim import (
  any_prim_cases,
  AnyPrim )

from .log import (
  LogEvent )

from .tool import (
  Tool )

from partis.schema.serialize.yaml import (
  loads,
  dumps )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NWLTestError( ModelError ):
  """Base of all NWL testing related errors
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NWLTestHint( ModelHint ):
  """Base of all NWL testing hints
  """
  pass


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
test_declared = schema_declared( tag = 'test' )
test_result_declared = schema_declared( tag = 'test' )

test_suite_declared = schema_declared( tag = 'test_suite' )
test_suite_result_declared = schema_declared( tag = 'test_suite' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def subprocess_log_cmd( args, cwd, logger ):

  run_ret = await trio.run_process(
    command = args,
    capture_stdout = True,
    capture_stderr = True,
    check = False )

  logger.info( "run stdout\n" + indent_lines(2, run_ret.stdout.decode("ascii", errors = "replace") ) )
  logger.info( "run stderr\n" + indent_lines(2, run_ret.stderr.decode("ascii", errors = "replace") ) )

  if run_ret.returncode != 0:

    raise subprocess.CalledProcessError(
      run_ret.returncode,
      run_ret.args,
      output = run_ret.stdout,
      stderr = run_ret.stderr )

  return run_ret

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def diff_hint( path, ref, val ):
  _path = ".".join(path)

  if is_sequence(ref):
    if not is_sequence( val ):
      return SchemaHint(f"expected sequence at `{_path}`: {fmt_base_or_type(val)}")

    if len( val ) != len( ref ):
      return SchemaHint(f"sequence at `{_path}` length {len(ref)}: {len(val)}")

    hints = list()

    for i, v in enumerate(ref):
      next_path = path + [ str(i), ]

      _hint = diff_hint( next_path, v, val[i] )

      if _hint is not None:
        hints.append( _hint )

    if len(hints) > 0:
      return SchemaHint(
        f"in sequence `{_path}`",
        hints = hints )

  elif is_mapping( ref ):
    if not is_mapping( val ):
      return SchemaHint(f"expected mapping at `{_path}`: {fmt_base_or_type(val)}")

    # if len( val ) != len( ref ):
    #   return SchemaHint(f"mapping at `{_path}` length {len(ref)} : {len(val)}")

    hints = list()

    for k, v in ref.items():
      next_path = path + [ str(k), ]

      _hint = None

      if k not in val:
        _hint = SchemaHint(f"missing key: `{k}`")

      else:

        _hint = diff_hint( next_path, v, val[k] )

      if _hint is not None:
        hints.append( _hint )

    # for k in val.keys():
    #   if k not in ref:
    #     hints.append( SchemaHint(f"un-expected key: `{k}`") )


    if len(hints) > 0:
      return SchemaHint(
        f"in mapping `{_path}`",
        hints = hints )

  elif val != ref:
    return SchemaHint(
      f"expected value at `{_path}`: {ref}",
      hints = [ f"{val}", ] )

  return None


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TestFile( StructValued ):

  schema = dict(
    tag = 'file' )

  path = StrPrim(
    doc = "Path relative to working or run directory",
    max_lines = 1 )

  size = IntPrim(
    doc = "Expected size of file in bytes",
    default_val = optional )

  checksum = StrPrim(
    doc = """Expected checksum of file, in hexadecimal format

      The hash is refixed with the algorithm used to compute the hash.
      For example, the SHA-1 hash would be given as:

        sha1$00ea1da4192a2030f9ae023de3b3143ed647bbab
      """,
    # pattern = r"(\w+)\$([0-9a-fA-F]+)",
    default_val = optional )

  content_mode = StrPrim(
    doc = """Mode used for contents of file

      In `binary` mode, the contents are assumed to be in standard
      Base64 format ( RFC 3548 ).
      """,
    restricted = [ 'text', 'binary' ],
    default_val = 'text' )

  contents = StrPrim(
    doc = """Contents of file""",
    default_val = optional )

  #-----------------------------------------------------------------------------
  def _wfile( self, dir ):

    path = os.path.join( dir, self.path )

    _dir = os.path.dirname( path )

    if not os.path.exists( _dir ):
      os.makedirs( _dir )

    if self.contents is None:
      # just "touch" the file
      with open( path, 'a'):
        os.utime( path, None )

    elif self.content_mode == 'text':

      with open( path, 'w' ) as fp:
        fp.write( self.contents )

    elif self.content_mode == 'binary':

      content_bytes = base64.standard_b64decode( self.contents.strip() )

      with open( path, 'wb' ) as fp:
        fp.write( content_bytes )

    else:
      assert False

  #-----------------------------------------------------------------------------
  def _rfile( self, dir ):
    path = os.path.join( dir, self.path )

    if not os.path.exists( path ):
      raise NWLTestError(f"Expected file does not exist: {path}")

    if self.size is not None:
      size = os.stat( path ).st_size

      if self.size != size:
        raise NWLTestError(f"Expected file size {self.size}: {size}")

    if self.checksum is not None:
      _alg, _hash = self.checksum.split("$")

      hash = checksum( path, algorithm = _alg )

      if hash != _hash:
        raise NWLTestError(
          f"File checksum failed",
          hints = [
            f"file: {path}",
            f"hash: {_alg}",
            f"expected: {_hash}",
            f"actual: {hash}" ])

    if self.contents is not None:
      if self.content_mode == 'text':
        lines_from = self.contents.strip().splitlines()

        with open( path, 'r' ) as fp:
          lines_to = fp.read().strip().splitlines()

        ndiff = (
          sum( a != b for a, b in zip(lines_from, lines_to ) )
          + abs( len(lines_from) - len(lines_to) ) )

        if ndiff > 0:
          dlines = difflib.unified_diff(
            lines_from,
            lines_to,
            fromfile = 'expected',
            tofile = path,
            lineterm = '' )

          # diff = "\n  ".join(dlines)

          raise NWLTestError(
            f"File contents failed",
            hints = [
              f"file: {path}",
              NWLTestHint(
                "lines",
                hints = dlines ) ])

      elif self.content_mode == 'binary':

        bytes_from = base64.standard_b64decode( self.contents.strip() )

        with open( path, 'rb' ) as fp:
          bytes_to = fp.write( )

        if bytes_from != bytes_to:
          raise NWLTestError(f"Expected file binary differs: {path}")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TestResults( StructValued ):

  schema = dict(
    declared = test_result_declared,
    default_val = derived )

  success = BoolPrim(
    doc = "Flag for whether the test was successful",
    default_val = True )

  workdir = StrPrim(
    doc = "Directory from which the tool was initially started",
    default_val = "" )

  rundir = StrPrim(
    doc = "Directory where tool was told to run",
    default_val = "" )

  logs = HintList

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Test( StructValued ):
  schema = dict(
    declared = test_declared,
    default_val = derived )

  tags = SeqPrim(
    doc = "List of tags associated with test",
    item = StrPrim(
      doc = "Tag name",
      max_cols = 20,
      max_lines = 1 ),
    default_val = list() )

  doc = StrPrim(
    doc = "Documentation string for more information about this test",
    default_val = '',
    max_lines = 100 )

  tool = StrPrim(
    doc = "Path to tool file",
    max_lines = 1,
    default_val = optional )

  mpiexec = SeqPrim(
    doc = "List of commands to execute a program within MPI, if available",
    item = StrPrim(
      max_lines = 1 ),
    default_val = list() )

  processes = IntPrim(
    doc = """Number of processes allocated

      The total cores allocated is ( processes * cpus_per_process )""",
    min = 1,
    default_val = 1 )

  cpus_per_process = IntPrim(
    doc = """Number of cores allocated per process""",
    min = 1,
    default_val = 1 )

  threads_per_cpu = IntPrim(
    doc = """Number of threads that can idealy run in parallel per core""",
    min = 1,
    default_val = 1 )

  inputs = MapPrim(
    doc = "Inputs used to run tool for this test case",
    item = AnyPrim,
    default_val = dict() )

  commands = MapPrim(
    doc = "Expected command results",
    item = AnyPrim,
    default_val = optional )

  outputs = MapPrim(
    doc = "Expected outputs",
    item = AnyPrim,
    default_val = optional )

  wfiles = SeqPrim(
    doc = """List of files to create in working directory""",
    item = TestFile,
    default_val = list() )

  rfiles = SeqPrim(
    doc = """List of expected output files in run directory""",
    item = TestFile,
    default_val = list() )

  logs = SeqPrim(
    doc = """List of possible logging events after tool runs.
      Logs with level 'ERROR' or 'CRITICAL' are used to establish whether a
      something has failed.
      """,
    item = LogEvent,
    default_val = list() )

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  async def _run( self, logger, workdir, rundir ):

    if workdir is None:
      workdir = os.getcwd()

    if rundir is None:
      rundir = os.getcwd()

    workdir = os.path.normpath( workdir )
    rundir = os.path.normpath( rundir )

    log_handler = LogListHandler()
    logger.addHandler( log_handler )

    if os.path.exists( rundir ):
      shutil.rmtree( rundir )

    os.makedirs( rundir )

    results = TestResults()

    results.workdir = workdir
    results.rundir = rundir

    try:
      if self.tool is None:
        raise NWLTestError(f"Test must specify `tool` file.")

      tool_src = os.path.join( workdir, self.tool )

      if not os.path.exists( tool_src ):
        raise NWLTestError(f"Test `tool` file not found in workdir: {tool_src}")

      # Load definition of tool to be tested
      tool_file = shutil.copy(
        tool_src,
        rundir )

      with open( tool_file, "r" ) as fp:
        doc = fp.read()

      tool = loads(
        src = doc,
        schema = Tool,
        loc = Loc(
          filename = tool_file ) )

      tool_results_file = os.path.join( rundir, "nwl.tool.results.yml" )

      in_file = os.path.join( rundir, "tool_inputs.yml" )

      in_str = dumps( self.inputs )

      with open( in_file, "w" ) as fp:
        fp.write( in_str )


      # create any initial test files
      for file in self.wfiles:
        file._wfile( dir = rundir )

      _mpiexec = " ".join(self.mpiexec)

      # run the tool with given inputs
      await subprocess_log_cmd( [
          "partis-nwl",
          "--tool",
          tool_file,
          "--inputs",
          in_file,
          "--workdir",
          workdir,
          "--rundir",
          rundir,
          "--np",
          str(self.processes),
          "--ncp",
          str(self.cpus_per_process),
          "--ntc",
          str(self.threads_per_cpu),
          "--mpiexec",
          f"\"{_mpiexec}\"" ],
        cwd = workdir,
        logger = logger )

      with open( tool_results_file, "r" ) as fp:
        doc = fp.read()

      # read in tool results
      tool_results = loads(
        src = doc,
        schema = tool.results_schema(),
        loc = Loc(
          filename = tool_results_file ) )


      if not tool_results.runtime.success:
        logger.error( f"Tool runtime failure" )

      else:

        # check that commands have correct values
        if self.commands is not None:
          hint = diff_hint(
            path = [ 'data', 'commands' ],
            ref = self.commands,
            val = tool_results.data.commands )

          if hint is not None:
            logger.error( hint )

        # check that outputs have correct values
        if self.outputs is not None:
          hint = diff_hint(
            path = [ 'data', 'outputs' ],
            ref = self.outputs,
            val = tool_results.data.outputs )

          if hint is not None:
            logger.error( hint )


        # check that output files have correct values
        for file in self.rfiles:
          try:
            file._rfile( dir = rundir )

          except Exception as e:
            logger.error( NWLTestHint(
              f"Output file error",
              level = 'error',
              hints = e ) )

        # check test logs
        logs = self.logs._eval(
          locals = tool_results,
          locals_key = '_',
          context = "log" )

        # filter for only enabled log events
        for l in logs:
          if l.enabled:
            logger.log( logging.getLevelName(l.level), l.msg )

    except Exception as e:
      logger.error( NWLTestHint(
        f"Test failed due to exception",
        level = 'error',
        hints = e ) )


    results.logs = log_handler.logs
    logger.removeHandler( log_handler )

    results.success = not any(
      l['level'] in [ 'ERROR', 'CRITICAL' ]
      for l in results.logs )

    return results

  #-----------------------------------------------------------------------------
  def _run_wait( self, logger, workdir, rundir ):
    results = trio.run( self._run, logger, workdir, rundir )
    return results

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TestSuiteResults( StructValued ):
  schema = dict(
    declared = test_suite_result_declared,
    default_val = derived )

  success = BoolPrim(
    doc = "Flag for whether all tests were successful",
    default_val = True )

  workdir = StrPrim(
    doc = "Directory from which the tool was initially started",
    default_val = "" )

  rundir = StrPrim(
    doc = "Directory where tool was told to run",
    default_val = "" )

  npass = IntPrim(
    doc = "Number of passing tests",
    default_val = 0 )

  nfail = IntPrim(
    doc = "Number of failing tests",
    default_val = 0 )

  tests = MapPrim(
    doc = "Results of tests",
    item = UnionPrim(
      cases = [
        test_result_declared,
        test_suite_result_declared ] ),
    default_val = dict() )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TestSuite( StructValued ):

  schema = dict(
    declared = test_suite_declared,
    default_val = derived )

  doc = StrPrim(
    doc = "Documentation string for more information about this test",
    default_val = '',
    max_lines = 100 )

  tests = MapPrim(
    doc = "Tests to run as a part of the suite",
    item = UnionPrim(
      cases = [
        test_declared,
        test_suite_declared ] ),
    default_val = dict() )

  #-----------------------------------------------------------------------------
  async def _run( self, logger, workdir, rundir, propagate = False ):

    if workdir is None:
      workdir = os.getcwd()

    if rundir is None:
      rundir = os.getcwd()

    workdir = os.path.normpath( workdir )
    rundir = os.path.normpath( rundir )

    results = TestSuiteResults()
    results.workdir = workdir
    results.rundir = rundir

    runs = dict()

    for k, test in self.tests.items():
      name = f"test_{k}"

      _rundir = os.path.join( rundir, name )
      _logger = logger.getChild( name )
      _logger.propagate = propagate

      runs[k] = test._run(
        logger = _logger,
        workdir = workdir,
        rundir = _rundir )

    results.tests = await wait_all( runs )

    npass = 0
    nfail = 0

    for test in results.tests.values():
      if isinstance( test, TestSuite ):
        npass += test.npass
        nfail += test.nfail

      else:
        if test.success:
          npass += 1
        else:
          nfail += 1

    results.npass = npass
    results.nfail = nfail

    results.success = ( nfail == 0 )

    return results

  #-----------------------------------------------------------------------------
  def _run_wait( self, logger, workdir, rundir ):
    results = trio.run( self._run, logger, workdir, rundir )
    return results
