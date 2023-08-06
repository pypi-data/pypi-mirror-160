"""Usage of `setup.py` is deprecated, and is supplied only for legacy installation.
"""
import sys
import os
import os.path as osp
import importlib
import logging
import argparse
import subprocess
import tempfile
from argparse import RawTextHelpFormatter
logger = logging.getLogger(__name__)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def egg_info( args ):

  logger.warning(
    "running legacy 'setup.py egg_info'" )

  dir = osp.join( args.egg_base, EGG_INFO_NAME )

  if not osp.exists( dir ):
    os.mkdir( dir )

  with open( osp.join( dir, 'PKG-INFO' ), 'wb' ) as fp:
    fp.write( PKG_INFO )

  with open( osp.join( dir, 'setup_requires.txt' ), 'wb' ) as fp:
    fp.write( b'' )

  with open( osp.join( dir, 'requires.txt' ), 'wb' ) as fp:
    fp.write( REQUIRES )

  with open( osp.join( dir, 'SOURCES.txt' ), 'wb' ) as fp:
    fp.write( SOURCES )

  with open( osp.join( dir, 'top_level.txt' ), 'wb' ) as fp:
    fp.write( TOP_LEVEL )

  with open( osp.join( dir, 'entry_points.txt' ), 'wb' ) as fp:
    fp.write( ENTRY_POINTS )

  with open( osp.join( dir, 'dependency_links.txt' ), 'wb' ) as fp:
    fp.write( b'' )

  with open( osp.join( dir, 'not-zip-safe' ), 'wb' ) as fp:
    fp.write( b'' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def bdist_wheel( args ):

  logger.warning(
    "running legacy 'setup.py bdist_wheel'" )

  sys.path = backend_path + sys.path

  backend = importlib.import_module( build_backend )

  backend.build_wheel(
    wheel_directory = args.dist_dir or args.bdist_dir or '.' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def install( args ):

  logger.warning(
    "running legacy 'setup.py install'" )

  reqs = [ f"{r}" for r in build_requires ]

  subprocess.check_call([
    sys.executable,
    '-m',
    'pip',
    'install',
    *reqs ] )

  sys.path = backend_path + sys.path

  backend = importlib.import_module( build_backend )

  with tempfile.TemporaryDirectory() as tmpdir:
    wheel_name = backend.build_wheel(
      wheel_directory = tmpdir )

    subprocess.check_call([
      sys.executable,
      '-m',
      'pip',
      'install',
      osp.join(tmpdir, wheel_name) ])

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dummy( args ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

  logging.basicConfig(
    level = logging.INFO,
    format = "{name}:{levelname}: {message}",
    style = "{" )


  logger.warning(
    "'setup.py' is deprecated, limited support for legacy installs. Upgrade pip." )

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  subparsers = parser.add_subparsers()

  #.............................................................................
  egg_info_parser = subparsers.add_parser( 'egg_info' )

  egg_info_parser.set_defaults( func = egg_info )

  egg_info_parser.add_argument( "-e", "--egg-base",
    type = str,
    default = '.' )

  #.............................................................................
  bdist_wheel_parser = subparsers.add_parser( 'bdist_wheel' )

  bdist_wheel_parser.set_defaults( func = bdist_wheel )

  bdist_wheel_parser.add_argument( "-b", "--bdist-dir",
    type = str,
    default = '' )

  bdist_wheel_parser.add_argument( "-d", "--dist-dir",
    type = str,
    default = '' )

  bdist_wheel_parser.add_argument( "--python-tag",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--plat-name",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--py-limited-api",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--build-number",
    type = str,
    default = None )

  #.............................................................................
  install_parser = subparsers.add_parser( 'install' )

  install_parser.set_defaults( func = install )

  install_parser.add_argument( "--record",
    type = str,
    default = None )

  install_parser.add_argument( "--install-headers",
    type = str,
    default = None )

  install_parser.add_argument( "--compile",
    action='store_true' )

  install_parser.add_argument( "--single-version-externally-managed",
    action='store_true' )

  #.............................................................................
  clean_parser = subparsers.add_parser( 'clean' )

  clean_parser.set_defaults( func = dummy )

  clean_parser.add_argument( "-a", "--all",
    action='store_true' )

  args = parser.parse_args( )

  args.func( args )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# NOTE: these are templated literal values substituded by the backend when
# building the source distribution

build_backend = 'partis.pyproj.backend'
backend_path = []
build_requires = ['wheel', 'partis-pyproj==0.0.3']

EGG_INFO_NAME = 'partis-nwl.egg-info'

PKG_INFO = b'Metadata-Version: 2.1\nName: partis-nwl\nVersion: 0.0.3\nRequires-Python: >=3.6.2\nMaintainer-email: "Nanohmics Inc." <software.support@nanohmics.com>\nSummary: Implementation of Nano Workflow Language (NWL)\nLicense-File: LICENSE.txt\nClassifier: Operating System :: POSIX :: Linux\nClassifier: Development Status :: 4 - Beta\nClassifier: Topic :: Scientific/Engineering\nClassifier: Programming Language :: Python\nClassifier: Programming Language :: Python :: 3\nClassifier: License :: OSI Approved :: BSD License\nClassifier: Intended Audience :: Science/Research\nClassifier: Topic :: System :: Clustering\nProvides-Extra: doc\nRequires-Dist: wheel\nRequires-Dist: partis-pyproj==0.0.3\nRequires-Dist: ruamel.yaml==0.16.5\nRequires-Dist: tomli>=1.2.3\nRequires-Dist: partis-utils[asy,lint]==0.0.3\nRequires-Dist: partis-schema==0.0.3\nRequires-Dist: build>=0.7.0\nRequires-Dist: partis-utils[sphinx]==0.0.3; extra == "doc"\nDescription-Content-Type: text/x-rst\n\nThe ``partis.nwl`` package is part of a workflow development toolkit.\n\nhttps://nanohmics.bitbucket.io/doc/partis/nwl'

REQUIRES = b'wheel\npartis-pyproj==0.0.3\nruamel.yaml==0.16.5\ntomli>=1.2.3\npartis-utils[asy,lint]==0.0.3\npartis-schema==0.0.3\nbuild>=0.7.0\npartis-utils[sphinx]==0.0.3; extra == "doc"'

SOURCES = b'partis_nwl-0.0.3/src/nwl/__init__.py\npartis_nwl-0.0.3/src/nwl/results.py\npartis_nwl-0.0.3/src/nwl/job.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/__init__.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/tool_pkg.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/__main__.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/build.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/doc/conf.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/doc/__init__.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/doc/_static/app_icon.svg\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/index.rst\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/partis_nwl_ext.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/pyproject.toml\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/__init__.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/results.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/index.rst\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/commands.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/commands.rst\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/__main__.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/inputs.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/results.rst\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/outputs.rst\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/outputs.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/_load_tool.py\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/source.rst\npartis_nwl-0.0.3/src/nwl/tool_pkg/pkg_tmpl/tool/inputs.rst\npartis_nwl-0.0.3/src/nwl/commands/__init__.py\npartis_nwl-0.0.3/src/nwl/commands/file.py\npartis_nwl-0.0.3/src/nwl/commands/base.py\npartis_nwl-0.0.3/src/nwl/commands/dir.py\npartis_nwl-0.0.3/src/nwl/commands/process.py\npartis_nwl-0.0.3/src/nwl/commands/script.py\npartis_nwl-0.0.3/src/nwl/__main__.py\npartis_nwl-0.0.3/src/nwl/inputs.py\npartis_nwl-0.0.3/src/nwl/query.py\npartis_nwl-0.0.3/src/nwl/context.py\npartis_nwl-0.0.3/src/nwl/runtime.py\npartis_nwl-0.0.3/src/nwl/allocation.py\npartis_nwl-0.0.3/src/nwl/base.py\npartis_nwl-0.0.3/src/nwl/log.py\npartis_nwl-0.0.3/src/nwl/content_type.py\npartis_nwl-0.0.3/src/nwl/info.py\npartis_nwl-0.0.3/src/nwl/view/__init__.py\npartis_nwl-0.0.3/src/nwl/view/tool_edit.py\npartis_nwl-0.0.3/src/nwl/view/plugin.py\npartis_nwl-0.0.3/src/nwl/view/tool_results_edit.py\npartis_nwl-0.0.3/src/nwl/view/testing.py\npartis_nwl-0.0.3/src/nwl/utils.py\npartis_nwl-0.0.3/src/nwl/outputs.py\npartis_nwl-0.0.3/src/nwl/resources.py\npartis_nwl-0.0.3/src/nwl/path.py\npartis_nwl-0.0.3/src/nwl/tool.py\npartis_nwl-0.0.3/src/nwl/testing.py\npartis_nwl-0.0.3/doc/conf.py\npartis_nwl-0.0.3/doc/__init__.py\npartis_nwl-0.0.3/doc/citations.rst\npartis_nwl-0.0.3/doc/index.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.commands.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.path.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.outputs.rst\npartis_nwl-0.0.3/doc/src/index.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.__main__.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.results.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.context.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.log.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.resources.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.info.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.query.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.runtime.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.inputs.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.tool.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.base.rst\npartis_nwl-0.0.3/doc/src/partis.nwl.testing.rst\npartis_nwl-0.0.3/doc/editor.rst\npartis_nwl-0.0.3/doc/__main__.py\npartis_nwl-0.0.3/doc/glossary.rst\npartis_nwl-0.0.3/doc/walkthrough.rst\npartis_nwl-0.0.3/doc/refs/workflow.bib\npartis_nwl-0.0.3/doc/img/partis_view_themes/__init__.py\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/__init__.py\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/pygments_style.py\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/vsplit.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/new.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/vhsplit.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/settings.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/forward.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/save.svg.2019_07_22_11_53_11.0.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/remove_hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/move_down.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/hsplit.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/move_up.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/script_active.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/base.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/down_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/save.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/load.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/back.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/script.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/config.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/left_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/edit.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/restore.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/remove_pressed.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/right_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/up_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/add.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/app_icon.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/edit_2.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/pancake.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/app_icon.png\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/disk.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/remove.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/connect.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/icons/saveAs.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/tree/branch-skip.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/tree/branch-end.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/tree/branch-more.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/tree/branch-closed.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/tree/branch-open.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/undock-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/right_arrow_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/radio_checked-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/down_arrow-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/radio_checked_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/transparent.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/up_arrow_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/branch_closed-on.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/down_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/checkbox_checked_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/spinup_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/left_arrow_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/stylesheet-vline.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/stylesheet-branch-more.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/left_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/checkbox_checked-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/branch_open-on.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/radio_unchecked_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/vsepartoolbars.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/checkbox_unchecked_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/hmovetoolbar.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/stylesheet-branch-end-open.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/hsepartoolbar.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/stylesheet-branch-end.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/right_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/checkbox_indeterminate_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/radio_unchecked-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/vmovetoolbar.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/up_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/close-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/stylesheet-branch-end-closed.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/checkbox_unchecked-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/down_arrow_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/up_arrow-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/sizegrip.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/radio_checked.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/close-pressed.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/checkbox_indeterminate-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/close.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/checkbox_indeterminate.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/branch_closed.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/branch_open.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/undock.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/images/base/checkbox_checked.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/Roboto-Regular.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/RobotoMono-LightItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/RobotoMono-Thin.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/Roboto-BoldItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/Roboto-Italic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/RobotoMono-MediumItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/RobotoMono-BoldItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/Roboto-BlackItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/Roboto-LightItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/RobotoMono-Medium.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/RobotoMono-Bold.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/RobotoMono-Italic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/RobotoMono-ThinItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/LICENSE.txt\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/Roboto-Thin.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/Roboto-Black.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/RobotoMono-Light.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/Roboto-MediumItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/Roboto-Light.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/RobotoMono-Regular.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/Roboto-Medium.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/Roboto-ThinItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/fonts/Roboto-Bold.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/styles/main.qss\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/styles/base.qss\npartis_nwl-0.0.3/doc/img/partis_view_themes/light/styles/config_tree.qss\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/__init__.py\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/pygments_style.py\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/vsplit.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/new.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/script.svg.2021_05_20_09_51_07.0.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/vhsplit.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/settings.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/forward.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/save.svg.2019_07_22_11_53_11.0.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/remove_hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/move_down.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/hsplit.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/move_up.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/script_active.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/base.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/down_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/save.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/load.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/back.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/script.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/config.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/left_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/edit.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/restore.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/remove_pressed.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/right_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/up_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/add.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/app_icon.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/edit_2.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/pancake.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/app_icon.png\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/remove.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/connect.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/icons/saveAs.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/test/no_data.png\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/test/no_data_pattern.png\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/test/no_data.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/test/no_data_pattern.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/test/pattern.png\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/tree/branch-skip.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/tree/stylesheet-branch-more.png\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/tree/branch-end.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/tree/branch-more.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/tree/branch-closed.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/tree/branch-open.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/undock-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/right_arrow_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/down_arrow-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/readme.md\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/radio_checked_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/transparent.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/up_arrow_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/branch_closed-on.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/down_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/checkbox_checked_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/spinup_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/left_arrow_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/stylesheet-vline.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/stylesheet-branch-more.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/left_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/branch_open-on.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/radio_unchecked_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/vsepartoolbars.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/checkbox_unchecked_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/hmovetoolbar.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/stylesheet-branch-end-open.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/hsepartoolbar.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/stylesheet-branch-end.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/right_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/checkbox_unchecked.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/checkbox_indeterminate_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/vmovetoolbar.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/checkbox_unchecked_active.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/up_arrow.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/close-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/stylesheet-branch-end-closed.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/down_arrow_disabled.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/up_arrow-hover.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/sizegrip.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/radio_unchecked.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/radio_checked.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/close-pressed.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/close.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/checkbox_indeterminate.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/branch_closed.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/branch_open.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/undock.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/images/base/checkbox_checked.svg\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/Roboto-Regular.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/RobotoMono-LightItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/RobotoMono-Thin.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/Roboto-BoldItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/Roboto-Italic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/RobotoMono-MediumItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/RobotoMono-BoldItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/Roboto-BlackItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/Roboto-LightItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/RobotoMono-Medium.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/RobotoMono-Bold.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/RobotoMono-Italic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/RobotoMono-ThinItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/LICENSE.txt\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/Roboto-Thin.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/Roboto-Black.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/RobotoMono-Light.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/Roboto-MediumItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/Roboto-Light.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/RobotoMono-Regular.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/Roboto-Medium.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/Roboto-ThinItalic.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/fonts/Roboto-Bold.ttf\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/styles/main.qss\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/styles/base.qss\npartis_nwl-0.0.3/doc/img/partis_view_themes/dark/styles/config_tree.qss\npartis_nwl-0.0.3/doc/img/motivation-overview.svg\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_list.svg\npartis_nwl-0.0.3/doc/img/nwl_gui/rename_key.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_expression4.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_input2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/text_edit3.png\npartis_nwl-0.0.3/doc/img/nwl_gui/schema_tree_edit.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_string.svg\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_expression3.png\npartis_nwl-0.0.3/doc/img/nwl_gui/union.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_union.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_selection2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_struct.svg\npartis_nwl-0.0.3/doc/img/nwl_gui/eval_output5.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_optional.png\npartis_nwl-0.0.3/doc/img/nwl_gui/log.yaml\npartis_nwl-0.0.3/doc/img/nwl_gui/add_selection3.png\npartis_nwl-0.0.3/doc/img/nwl_gui/new_file_nwl.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_command.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_case.png\npartis_nwl-0.0.3/doc/img/nwl_gui/log_event.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_int.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_selection.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_struct.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_label.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_bool.svg\npartis_nwl-0.0.3/doc/img/nwl_gui/add_arg2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/eval_output6.png\npartis_nwl-0.0.3/doc/img/nwl_gui/eval_output4.png\npartis_nwl-0.0.3/doc/img/nwl_gui/rename_key2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_list.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_float.svg\npartis_nwl-0.0.3/doc/img/nwl_gui/text_edit.png\npartis_nwl-0.0.3/doc/img/nwl_gui/epilog_event.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_arg.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_case3.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_input3.png\npartis_nwl-0.0.3/doc/img/nwl_gui/schema_tree_edit.yaml\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_bool.png\npartis_nwl-0.0.3/doc/img/nwl_gui/eval_output.png\npartis_nwl-0.0.3/doc/img/nwl_gui/move_input.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_union.svg\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_expression5.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_bool2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/change_cmd.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_multiline.png\npartis_nwl-0.0.3/doc/img/nwl_gui/new_file.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_label2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/eval_output2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/schema_tree_edit.svg.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_expression2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_input.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_arg3.png\npartis_nwl-0.0.3/doc/img/nwl_gui/move_input2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_int.svg\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_selection.png\npartis_nwl-0.0.3/doc/img/nwl_gui/save.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_case2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_expression.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_output.png\npartis_nwl-0.0.3/doc/img/nwl_gui/select_type.png\npartis_nwl-0.0.3/doc/img/nwl_gui/schema_tree_edit.svg\npartis_nwl-0.0.3/doc/img/nwl_gui/remove_optional.png\npartis_nwl-0.0.3/doc/img/nwl_gui/text_edit2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/cheetah.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_output2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_string.png\npartis_nwl-0.0.3/doc/img/nwl_gui/eval_output3.png\npartis_nwl-0.0.3/doc/img/nwl_gui/schema_tree_node_ctx.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_multiline2.png\npartis_nwl-0.0.3/doc/img/nwl_gui/add_case4.png\npartis_nwl-0.0.3/doc/img/nwl_gui/edit_float.png\npartis_nwl-0.0.3/doc/img/nwl_gui/save2.png\npartis_nwl-0.0.3/doc/overview.rst\npartis_nwl-0.0.3/test/400_nwl/__init__.py\npartis_nwl-0.0.3/test/400_nwl/test_tool.py\npartis_nwl-0.0.3/test/400_nwl/test_output.py\npartis_nwl-0.0.3/test/400_nwl/test_input.py\npartis_nwl-0.0.3/examples/input.js\npartis_nwl-0.0.3/examples/data_example.yml\npartis_nwl-0.0.3/examples/text.txt\npartis_nwl-0.0.3/examples/pkg_nwl_example.yml\npartis_nwl-0.0.3/examples/pkg_mpi_example.yml\npartis_nwl-0.0.3/examples/generic_inputs_query.yml\npartis_nwl-0.0.3/examples/mpi_example.yml\npartis_nwl-0.0.3/examples/run_mpi_example.batch\npartis_nwl-0.0.3/examples/util.py\npartis_nwl-0.0.3/examples/grep_inputs_query.yml\npartis_nwl-0.0.3/examples/generic_inputs.yml\npartis_nwl-0.0.3/examples/run_nwl_example.sh\npartis_nwl-0.0.3/examples/module_example.yml\npartis_nwl-0.0.3/examples/generic.yml\npartis_nwl-0.0.3/examples/vars.yml\npartis_nwl-0.0.3/examples/grep_inputs.yml\npartis_nwl-0.0.3/examples/run_nwl_pkg.sh\npartis_nwl-0.0.3/examples/mpi_inputs.yml\npartis_nwl-0.0.3/examples/tool_tests.yml\npartis_nwl-0.0.3/examples/run_mpi_example.sh\npartis_nwl-0.0.3/examples/grep.yml\npartis_nwl-0.0.3/LICENSE.txt\npartis_nwl-0.0.3/README.rst\npartis_nwl-0.0.3/pyproject.toml'

TOP_LEVEL = b''

ENTRY_POINTS = b'[partis_view]\nview_editors = partis.nwl.view.plugin:get_view_editors\n\n[console_scripts]\npartis-nwl = partis.nwl.__main__:main\npartis-nwl-pkg = partis.nwl.tool_pkg.__main__:main\n\n'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
  exit( main() )
