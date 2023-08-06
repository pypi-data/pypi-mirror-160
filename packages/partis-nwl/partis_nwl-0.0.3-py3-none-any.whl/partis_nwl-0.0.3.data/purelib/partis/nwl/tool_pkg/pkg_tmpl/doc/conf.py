# -*- coding: utf-8 -*-

import sys
import os
import os.path as osp
import tomli
from partis.utils.sphinx import basic_conf

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# configuration
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

conf_dir = osp.abspath( osp.dirname(__file__) )
root_dir = osp.abspath( osp.join( conf_dir, os.pardir ) )

pptoml_file = osp.join( root_dir, 'pyproject.toml' )

with open( pptoml_file, 'r' ) as fp:
  pptoml = tomli.loads( fp.read() )

globals().update( basic_conf(
  package = pptoml['project']['name'],
  copyright_year = '2022' ) )

intersphinx_mapping['partis.schema'] = (
  "https://nanohmics.bitbucket.io/doc/partis/schema",
  None )

intersphinx_mapping['partis.nwl'] = (
  "https://nanohmics.bitbucket.io/doc/partis/pyproj",
  None )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# processing hooks
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def autodoc_skip_member(app, what, name, obj, skip, options):
  from partis.schema import (
    is_schema )

  if what != 'module' and is_schema(obj):
    # only document schemas at the module level.
    # all other embedded documentation should already be in generated docstrings
    return True

  return skip

def process_docstring(app, what, name, obj, options, lines):
  if isinstance(obj, type) and type(obj).__name__ != 'type':
    # this is a class with a metaclass that is not `type`
    mcls = type(obj)
    lines.insert(0, "")
    lines.insert(0, "")
    lines.insert( 0,
      f"Metaclass: :class:`{mcls.__name__} <{mcls.__module__}.{mcls.__name__}>`" )

  return lines

def setup(app):
    app.connect("autodoc-skip-member", autodoc_skip_member )
    app.connect("autodoc-process-docstring", process_docstring)
