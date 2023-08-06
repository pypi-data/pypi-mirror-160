
import os
import re
import subprocess
import shutil
import shlex
from timeit import default_timer as timer

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  odict,
  adict,
  ModelHint,
  ModelError,
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


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolAuthor( StructValued ):
  schema = dict(
    tag = 'tool_author',
    default_val = derived )

  name = StrPrim(
    doc = "Name of tool author",
    default_val = "unknown",
    max_lines = 1,
    max_cols = 80 )

  email = StrPrim(
    doc = "Email to contact tool author",
    default_val = "",
    max_lines = 1,
    max_cols = 80 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolInfo( StructValued ):
  schema = dict(
    tag = 'tool_info',
    doc = 'Tool information',
    default_val = derived )

  label = StrPrim(
    doc = "Short user-friendly description of tool",
    max_lines = 1,
    max_cols = 80,
    default_val = "unknown" )

  doc = StrPrim(
    doc = "Additional information about the tool",
    default_val = "",
    max_lines = 200 )

  version = SeqPrim(
    doc = "Version of tool",
    item = IntPrim(
      min = 0 ),
    default_val = [ 0, 1 ] )

  author = ToolAuthor
