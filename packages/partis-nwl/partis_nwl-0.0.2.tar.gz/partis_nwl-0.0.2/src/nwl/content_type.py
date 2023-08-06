
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
class ContentType( StructValued ):
  schema = dict(
    tag = 'content_type',
    struct_proxy = "media",
    default_val = derived )

  media = StrPrim(
    doc = "Specifies a resource media type",
    default_val = "text",
    max_lines = 1,
    nonempty = True,
    pattern = "(?P<type>application|audio|image|message|multipart|text|video)(/(?P<subtype>[\w\.-]+)(\+(?P<suffix>\w+))?)?" )

  extensions = SeqPrim(
    doc = "List of filename extensions associated with this type, without leading '.'",
    item = StrPrim(
      max_lines = 1,
      default_val = "txt",
      nonempty = True,
      pattern = "\w[\w\.]+" ),
    default_val = list() )

ContentTypeList = SeqPrim(
  doc = "Specifies a list of possible resource media type(s)",
  item = ContentType,
  default_val = list() )
