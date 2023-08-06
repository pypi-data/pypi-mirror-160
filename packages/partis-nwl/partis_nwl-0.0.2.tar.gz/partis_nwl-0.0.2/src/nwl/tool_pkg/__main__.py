"""
"""

import argparse
from argparse import RawTextHelpFormatter
import trio

from partis.utils import init_logging
from .build import build

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def argument_parser( ):

  """Parse for commandline arguments.
  """

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )


  parser.add_argument( "pkg_file",
    type = str,
    help = "path to tool package definition file" )

  parser.add_argument( "-o", "--out",
    type = str,
    help = "path to place the resulting package file" )

  parser.add_argument( "--tmp",
    type = str,
    help = "temporary build directory" )

  parser.add_argument( "--no-cleanup",
    action = 'store_true',
    help = "do not cleanup temporary build directory" )

  parser.add_argument( "--no-doc",
    action = 'store_true',
    help = "do not generate documentation" )

  parser.add_argument( "-l", "--log",
    type = str,
    default = "",
    help = "Redirect output to the given log file" )

  parser.add_argument( "-v", "--verbosity",
    type = str,
    default = 'info',
    help = "Log verbosity {all, debug, info, warning, error, critical}" )



  return parser

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def _main():
  parser = argument_parser( )
  args = parser.parse_args( )

  init_logging(
    level = args.verbosity,
    filename = args.log )

  await build(
    pkg_file = args.pkg_file,
    outdir = args.out,
    tmpdir = args.tmp,
    cleanup = not args.no_cleanup,
    build_docs = not args.no_doc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():
  trio.run( _main )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
  main()
