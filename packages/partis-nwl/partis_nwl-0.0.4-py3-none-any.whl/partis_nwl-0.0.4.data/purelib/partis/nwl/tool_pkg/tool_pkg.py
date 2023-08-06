
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
  Loc )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PkgAuthor( StructValued ):
  schema = dict(
    tag = 'tool_pkg_author',
    default_val = derived )

  name = StrPrim(
    doc = "Name of author",
    default_val = "",
    max_lines = 1,
    max_cols = 80 )

  email = StrPrim(
    doc = "Email to contact author",
    default_val = "",
    max_lines = 1,
    max_cols = 80 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NWLToolPkgInfo( StructValued ):
  schema = dict(
    tag = 'tool_pkg_info',
    doc = 'Tool package information',
    default_val = derived )

  name = StrPrim(
    doc = "Unique package name. Must conform to Python package name standards",
    default_val = "",
    max_lines = 1,
    max_cols = 80 )

  version = SeqPrim(
    doc = "Version of tool",
    item = IntPrim(
      min = 0 ),
    default_val = [ 0, 1 ] )

  label = StrPrim(
    doc = "Short user-friendly display name of tool package",
    default_val = "",
    max_lines = 1,
    max_cols = 80 )

  doc = StrPrim(
    doc = "Additional information about the tool package",
    default_val = "",
    max_lines = 200 )

  author = PkgAuthor

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolFile( StructValued ):

  schema = dict(
    tag = 'path',
    struct_proxy = "path" )

  path = StrPrim(
    doc = "Path to tool definition file.",
    max_lines = 1 )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NWLToolPkg( StructValued ):

  schema = dict(
    tag = 'tool_pkg',
    default_val = derived )

  nwl = IntPrim(
    doc = "Version of Nano Workflow Language (NWL)",
    restricted = [ 1, ],
    default_val = 1 )

  info = NWLToolPkgInfo

  tools = SeqPrim(
    item = ToolFile,
    default_val = list() )

  #-----------------------------------------------------------------------------
  def pkg_doc( self ):

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
      lines.extend( [ '* author:', '' ] )

      if info.author.name:
        lines.append(f'  * name: {info.author.name}')

      if info.author.email:
        lines.append(f'  * email: {info.author.email}')

    return '\n'.join(lines)
