# -*- coding: UTF-8 -*-

import os

import logging
log = logging.getLogger(__name__)

from pygments import (
  lexers )

from partis.utils import (
  adict,
  odict )

from partis.schema import (
  required,
  optional,
  derived,
  is_optional,
  PyEvaluated,
  PassPrim,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  StructValued,
  SeqValued,
  MapValued,
  schema_declared,
  EvaluatedContext )

from partis.schema.prim.any_prim import (
  any_prim_cases,
  AnyPrim )

from .path import (
  WorkAbsolutePathEvaluated,
  RunAbsolutePathEvaluated,
  RunRelativePathEvaluated )

from .log import (
  LogEvent )

from .query import (
  NWLQueryEvaluated )

from .context import (
  InputsContext )

from .content_type import (
  ContentTypeList )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
EvaluatedInputs = PyEvaluated.subclass(
  context = InputsContext )

EvaluatedInputValues = NWLQueryEvaluated.subclass(
  context = InputsContext )

WorkAbsolutePathEvaluatedInput = WorkAbsolutePathEvaluated.subclass(
  context = InputsContext )

RunAbsolutePathEvaluatedInput = RunAbsolutePathEvaluated.subclass(
  context = InputsContext )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# create declareds for all the 'input' schemas

bool_declared = schema_declared( tag = 'bool' )
int_declared = schema_declared( tag = 'int' )
float_declared = schema_declared( tag = 'float' )
string_declared = schema_declared( tag = 'string' )
list_declared = schema_declared( tag = 'list' )
dict_declared = schema_declared( tag = 'dict' )
struct_declared = schema_declared( tag = 'struct' )
union_declared = schema_declared( tag = 'union' )
file_declared = schema_declared( tag = 'file' )
wfile_declared = schema_declared( tag = 'wfile' )
dir_declared = schema_declared( tag = 'dir' )
wdir_declared = schema_declared( tag = 'wdir' )

AnyNonUnionInput = UnionPrim(
  doc = """Union of any non-union input types
  """,
  cases = [
    bool_declared,
    int_declared,
    float_declared,
    string_declared,
    list_declared,
    dict_declared,
    struct_declared,
    file_declared,
    wfile_declared,
    dir_declared,
    wdir_declared ],
  default_case = 0 )

AnyInput = UnionPrim(
  doc = """Union of any input type, including a union of input types
  """,
  cases = [
    bool_declared,
    int_declared,
    float_declared,
    string_declared,
    list_declared,
    dict_declared,
    struct_declared,
    union_declared,
    file_declared,
    wfile_declared,
    dir_declared,
    wdir_declared ],
  default_case = 0 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def process_base( schema ):

  restricted = None
  doc = [ f"{schema.label} [ {schema._schema.tag} ]", ]

  if schema.doc is not None:
    doc.append(schema.doc)

  if hasattr(schema, 'selection') and schema.selection is not None and len(schema.selection) > 0:
    restricted = list()

    for s in schema.selection:
      restricted.append( s.value )

      if s.label is None:
        label = f"{s.value}"
      else:
        label = s.label

      if s.doc is None:
        _doc = ""
      else:
        _doc = s.doc

      if s.value == schema.default_val:
        doc.append( f"- {label} ( {s.value}, default ): {_doc}" )
      else:
        doc.append( f"- {label} ( {s.value} ): {_doc}" )

  doc = "\n".join(doc)

  return doc, restricted

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BaseInput( StructValued ):
  """Tool input
  """

  schema = dict(
    tag = 'base_input' )

  label = StrPrim(
    doc = "Short identifying string for this input",
    default_val = '',
    max_lines = 1,
    max_cols = 80 )

  doc = StrPrim(
    doc = "Documentation string for more information about this input",
    default_val = '',
    max_lines = 100 )

  visible = BoolPrim(
    doc = "If false, becomes invisible when `enabled` is False. Otherwise remains visible",
    default_val = True )

  enabled = BoolPrim(
    doc = "Marks the input as enabled if True, disabled if False",
    default_val = True,
    evaluated = EvaluatedInputs )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    """Returns the schema for the value defined by this input

    Parameters
    ----------
    name : None | str
      The name to set for the schema class
    tag : str
      If returning a schema class to a union, the tag used to uniquely identify the class.
    module : None | ModuleType
      The module to set for the schema
    """
    raise SchemaError(f"Value schema not implemented for this input")

  #-----------------------------------------------------------------------------
  # def value_meta( self, val ):
  #   raise SchemaError(f"Value schema not implemented for this input")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BaseSelectOption( StructValued ):
  """A selection option for an input with restricted values
  """

  schema = dict(
    tag = 'base_select' )

  label = StrPrim(
    doc = "Short identifying string for this selection option",
    default_val = '',
    max_lines = 1,
    max_cols = 80 )

  doc = StrPrim(
    doc = "Documentation string for more information about this option",
    default_val = '',
    max_lines = 100 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BoolInput( BaseInput ):
  """Boolean input
  """
  schema = dict(
    declared = bool_declared )

  default_val = BoolPrim(
    doc = "Default value if input is not given",
    default_val = False )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    doc, restricted = process_base( self )

    return BoolPrim(
      default_val = self.default_val,
      doc = doc,
      module = module,
      evaluated = EvaluatedInputValues,
      name = name,
      loc = self._loc )

  #-----------------------------------------------------------------------------
  # def value_meta( self, val ):
  #   path = ".".join( val._loc.path )
  #
  #   return self._schema.subclass(
  #     struct = odict(
  #       value = BoolPrim(
  #         default_val = f"$expr:py _.data{path}" ) ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class IntSelectOption( BaseSelectOption ):
  schema = dict(
    tag = 'int_select',
    struct_proxy = 'value' )

  value = IntPrim()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class IntInput( BaseInput ):
  """Integer input
  """
  schema = dict(
    declared = int_declared )

  default_val = IntPrim(
    doc = "Default value if input is not given",
    default_val = 0 )

  selection = SeqPrim(
    doc = "Limits values to one of a set of values",
    item = IntSelectOption,
    default_val = optional )

  min = IntPrim(
    default_val = optional )

  max = IntPrim(
    default_val = optional )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    doc, restricted = process_base( self )

    return IntPrim(
      default_val = self.default_val,
      restricted = restricted,
      min = self.min,
      max = self.max,
      doc = doc,
      module = module,
      evaluated = EvaluatedInputValues,
      name = name,
      loc = self._loc )

  #-----------------------------------------------------------------------------
  # def value_meta( self, val ):
  #   path = ".".join( val._loc.path )
  #
  #   return self._schema.subclass(
  #     struct = odict(
  #       value = IntPrim(
  #         default_val = f"$expr:py _.data{path}" ) ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FloatSelectOption( BaseSelectOption ):
  schema = dict(
    tag = 'float_select',
    struct_proxy = 'value' )

  value = FloatPrim()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FloatInput( BaseInput ):
  """Floating point input
  """
  schema = dict(
    declared = float_declared )

  default_val = FloatPrim(
    doc = "Default value if input is not given",
    default_val = 0.0 )

  selection = SeqPrim(
    doc = "Limits values to one of a set of values",
    item = FloatSelectOption,
    default_val = optional )

  min = FloatPrim(
    default_val = optional )

  max = FloatPrim(
    default_val = optional )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    doc, restricted = process_base( self )

    return FloatPrim(
      default_val = self.default_val,
      restricted = restricted,
      min = self.min,
      max = self.max,
      doc = doc,
      module = module,
      evaluated = EvaluatedInputValues,
      name = name,
      loc = self._loc )

  #-----------------------------------------------------------------------------
  # def value_meta( self, val ):
  #   path = ".".join( val._loc.path )
  #
  #   return self._schema.subclass(
  #     struct = odict(
  #       value = FloatPrim(
  #         default_val = f"$expr:py _.data{path}" ) ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StrSelectOption( BaseSelectOption ):
  schema = dict(
    tag = 'str_select',
    struct_proxy = 'value' )

  value = StrPrim()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PygmentizeOption( StructValued ):
  """Specifies syntax highlighting of text using Pygments (pygments.org)
  """

  schema = dict(
    tag = 'str_pygment',
    default_val = optional )

  lexer = StrPrim(
    restricted = [ l[1][0]
      for l in lexers.get_all_lexers()
      if len(l) > 1 and len(l[1]) > 0 ] )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StrInput( BaseInput ):
  """String input
  """
  schema = dict(
    declared = string_declared )

  default_val = StrPrim(
    doc = "Default value if input is not given",
    default_val = "" )

  max_lines = IntPrim(
    doc = "Maximum number of lines for user input",
    min = 1,
    default_val = 1 )

  max_cols = IntPrim(
    doc = "Maximum number of columns for user input",
    min = 1,
    default_val = optional )

  char_case = StrPrim(
    doc = "Cased characters are converted to given case",
    restricted = [ 'lower', 'upper' ],
    default_val = optional )

  strip = BoolPrim(
    doc = "Strips leading and trailing white-space if ``True``.",
    default_val = optional )

  pattern = StrPrim(
    doc = "Regular expression pattern for valid strings",
    default_val = optional )

  nonempty = BoolPrim(
    doc = "Only non-empty strings are valid if ``True``.",
    default_val = optional )

  pygment = PygmentizeOption

  selection = SeqPrim(
    doc = "Limits values to one of a set of values",
    item = StrSelectOption,
    default_val = optional )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    doc, restricted = process_base( self )

    return StrPrim(
      default_val = self.default_val,
      restricted = restricted,
      char_case = self.char_case,
      pattern = self.pattern,
      max_lines = self.max_lines,
      max_cols = self.max_cols,
      nonempty = self.nonempty,
      strip = self.strip,
      doc = doc,
      module = module,
      evaluated = EvaluatedInputValues,
      name = name,
      loc = self._loc )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ListInput( BaseInput ):
  """List input, sequence of values
  """
  schema = dict(
    declared = list_declared )

  item = AnyInput

  min_len = IntPrim(
    doc = "Minimum length of list",
    min = 0,
    default_val = 0 )

  default_val = SeqPrim(
    doc = "Default value if input is not given",
    item = AnyPrim,
    # Note: value does not get validated until `value_schema` is called
    default_val = list() )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    doc, restricted = process_base( self )

    return SeqPrim(
      item = self.item.value_schema(
        name = name + '_item',
        module = module ),
      default_val = self.default_val,
      min_len = self.min_len,
      doc = doc,
      module = module,
      evaluated = EvaluatedInputValues,
      name = name,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DictInput( BaseInput ):
  """Dictionary input, mapping of values
  """
  schema = dict(
    declared = dict_declared )

  item = AnyInput

  min_len = IntPrim(
    doc = "Minimum length of list",
    min = 0,
    default_val = 0 )

  default_val = MapPrim(
    doc = "Default value if input is not given",
    item = AnyPrim,
    # Note: value does not get validated until `value_schema` is called
    default_val = dict() )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    doc, restricted = process_base( self )

    return MapPrim(
      item = self.item.value_schema(
        name = name + '_item',
        module = module ),
      default_val = self.default_val,
      min_len = self.min_len,
      doc = doc,
      module = module,
      evaluated = EvaluatedInputValues,
      name = name,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StructInput( BaseInput ):
  """Struct input, fixed mapping
  """
  schema = dict(
    declared = struct_declared )

  struct = MapPrim(
    doc = "Specifies the schemas used to validate key-value pairs",
    item = AnyInput )

  struct_proxy = StrPrim(
    doc = "Specifies one key that may be populated if the input is not a mapping",
    default_val = optional,
    max_lines = 1,
    max_cols = 80  )

  default_val = MapPrim(
    doc = "Default value if input is not given",
    item = AnyPrim,
    # Note: value does not get validated until `value_schema` is called
    default_val = optional )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    doc, restricted = process_base( self )

    if tag is None:
      tag = "struct"

    struct = list()

    for k,v in self.struct.items():
      struct.append( (k, v.value_schema(
        module = module,
        name = name + f'_{k}' ) ) )

    if is_optional( self.default_val ):
      default_val = derived
    else:
      default_val = self.default_val

    return StructValued.subclass(
      tag = tag,
      struct = struct,
      struct_proxy = self.struct_proxy,
      default_val = default_val,
      doc = doc,
      module = module,
      evaluated = EvaluatedInputValues,
      name = name,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class UnionInput( BaseInput ):
  """Union of multiple input tyoes
  """
  schema = dict(
    declared = union_declared )

  # NOTE: overriden to make the label optional, since every case will have a label
  label = StrPrim(
    doc = "Short identifying string for this input",
    max_lines = 1,
    max_cols = 80,
    default_val = "" )

  cases = MapPrim(
    doc = """The possible types that may appear for the union input

    - Max of one case of type `bool`.
    - Max of one numeric case of either type `int` or `float`.
    - Max of one case of type `string`.
    - Max of one case of type `list`.
    - Any number of cases of type `struct`.
    - If there is more than one case of type `struct`, the input mapping must
      contain the ``type`` equal to the corresponding case key.

    """,
    item = AnyNonUnionInput,
    min_len = 1,
    default_val = { 'new_key' : { 'type' : 'bool' } } )

  default_case = StrPrim(
    doc = """The default case to use when there is no value.
      Must be one of the keys given in `cases`
      If not given, the first case will be used as the default.""",
    default_val = optional,
    max_lines = 1,
    max_cols = 80 )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    doc, restricted = process_base( self )

    case_value_schemas = list()

    for k, v in self.cases.items():
      case_value_schemas.append( v.value_schema(
        tag = k,
        name = name + f'_{k}',
        module = module ) )

    # convert the default case 'key' into the index of the default case schema
    default_case = 0

    if self.default_case is not None:
      keys = list(self.cases.keys())

      if self.default_case not in keys:
        raise SchemaError(
          f"`default_case` must be one of {keys}: {self.default_case}")

      default_case = keys.index(self.default_case)

    return UnionPrim(
      cases = case_value_schemas,
      default_case = default_case,
      doc = doc,
      module = module,
      evaluated = EvaluatedInputValues,
      name = name,
      loc = self._loc )

  #-----------------------------------------------------------------------------
  # def value_meta( self, val ):
  #   case = self.cases[ val['case'] ]
  #
  #   return MapValued(odict(
  #     **self,
  #     data = MapValued(odict(
  #       case = val['case'],
  #       value = case.value_meta( val['value'] ) )) ))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PathValue( StructValued ):
  """Value for filesystem path
  """
  schema = dict(
    tag = 'path',
    struct_proxy = "path" )

  path = StrPrim( )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PathInputValue( PathValue ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PathInput( BaseInput ):
  """Filesystem path input
  """
  schema = dict(
    tag = 'path' )

  default_val = StrPrim(
    default_val = "",
    max_lines = 1 )

  nonempty = BoolPrim(
    doc = "If true, requires the path to be non-empty",
    default_val = False )

  content_types = ContentTypeList

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    raise NotImplementedError("PathInputValue sublcass must implement")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class WorkFileInput( PathInput ):
  """Path to file that must already exist
  """
  schema = dict(
    declared = file_declared )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    doc, restricted = process_base( self )

    return PathInputValue.subclass(
      tag = tag or self._schema.tag,
      doc = doc,
      module = module,
      # NOTE: this is for evaluating a query
      evaluated = EvaluatedInputValues,
      name = name,
      loc = self._loc,
      default_val = derived,
      struct = dict(
        path = StrPrim(
          doc = "Path to file relative to initial working directory.",
          # NOTE: this is for resolving relative paths
          evaluated = WorkAbsolutePathEvaluatedInput,
          max_lines = 1,
          default_val = self.default_val,
          nonempty = self.nonempty,
          loc = self._loc ) ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RunFileInput( PathInput ):
  """Path to file that will be created
  """
  schema = dict(
    declared = wfile_declared )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    doc, restricted = process_base( self )

    return PathValue.subclass(
      tag = tag or self._schema.tag,
      doc = doc,
      module = module,
      # NOTE: this is for evaluating a query
      evaluated = EvaluatedInputValues,
      name = name,
      loc = self._loc,
      default_val = derived,
      struct = dict(
        path = StrPrim(
          doc = "Path to file relative to run directory.",
          evaluated = RunRelativePathEvaluated,
          max_lines = 1,
          default_val = self.default_val,
          nonempty = self.nonempty,
          loc = self._loc ) ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class WorkDirInput( PathInput ):
  """Path to directory that must already exist
  """
  schema = dict(
    declared = dir_declared )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    doc, restricted = process_base( self )

    return PathInputValue.subclass(
      tag = tag or self._schema.tag,
      doc = doc,
      module = module,
      # NOTE: this is for evaluating a query
      evaluated = EvaluatedInputValues,
      name = name,
      loc = self._loc,
      default_val = derived,
      struct = dict(
        path = StrPrim(
          doc = "Path to file relative to initial working directory.",
          evaluated = WorkAbsolutePathEvaluatedInput,
          max_lines = 1,
          default_val = self.default_val,
          nonempty = self.nonempty,
          loc = self._loc ) ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RunDirInput( PathInput ):
  """Path to directory that will be created
  """
  schema = dict(
    declared = wdir_declared )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    doc, restricted = process_base( self )

    return PathValue.subclass(
      tag = tag or self._schema.tag,
      doc = doc,
      module = module,
      # NOTE: this is for evaluating a query
      evaluated = EvaluatedInputValues,
      name = name,
      loc = self._loc,
      default_val = derived,
      struct = dict(
        path = StrPrim(
          doc = "Path to file relative to run directory.",
          evaluated = RunRelativePathEvaluated,
          max_lines = 1,
          default_val = self.default_val,
          nonempty = self.nonempty ) ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# now that schemas have been defined, resolve from the schema declareds
# AnyInput = UnionPrim(
#   cases = [ v.schema for v in AnyInput.cases ],
#   default_case = 0 )
