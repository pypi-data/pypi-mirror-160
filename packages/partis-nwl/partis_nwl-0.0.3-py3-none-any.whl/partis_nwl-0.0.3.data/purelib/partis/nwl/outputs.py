from collections import OrderedDict as odict

import logging
log = logging.getLogger(__name__)

from partis.schema import (
  required,
  optional,
  derived,
  is_valued,
  is_optional,
  PyEvaluated,
  CheetahEvaluated,
  PassPrim,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  StructValued,
  schema_declared,
  EvaluatedContext )

from partis.schema.prim.any_prim import (
  any_prim_cases,
  AnyPrim )

from .log import (
  LogEvent )

from .path import (
  RunRelativePathEvaluated )

from .context import (
  OutputsContext )

from .content_type import (
  ContentTypeList )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
EvaluatedOutputs = PyEvaluated.subclass(
  context = OutputsContext )

CheetahOutputs = CheetahEvaluated.subclass(
  context = OutputsContext )

RunRelativePathEvaluated = RunRelativePathEvaluated.subclass(
  context = OutputsContext )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# create declareds for all the 'output' schemas
bool_declared = schema_declared( tag = 'bool' )
int_declared = schema_declared( tag = 'int' )
float_declared = schema_declared( tag = 'float' )
string_declared = schema_declared( tag = 'string' )
list_declared = schema_declared( tag = 'list' )
dict_declared = schema_declared( tag = 'dict' )
struct_declared = schema_declared( tag = 'struct' )
union_declared = schema_declared( tag = 'union' )
file_declared = schema_declared( tag = 'file' )
dir_declared = schema_declared( tag = 'dir' )

AnyUnionOutput = UnionPrim(
  doc = """Union of any non-union output types
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
    dir_declared ],
  default_case = 0 )

AnyOutput = UnionPrim(
  doc = """Union of any output type, including a union of output types
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
    dir_declared ],
  default_case = 0 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BaseOutput( StructValued ):
  """Tool output
  """
  schema = dict(
    tag = 'base_output',
    default_val = derived )

  label = StrPrim(
    doc = "Short identifying string for this output",
    default_val = '',
    max_lines = 1,
    max_cols = 80 )

  doc = StrPrim(
    doc = "Documentation string for more information about this output",
    default_val = '',
    max_lines = 100 )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    raise SchemaError(f"Value schema not implemented for this output")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BoolOutput( BaseOutput ):
  """Boolean output value
  """
  schema = dict(
    declared = bool_declared )

  default_val = BoolPrim(
    default_val = False )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    return BoolPrim(
      default_val = self.default_val,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BoolOutputMain( BoolOutput ):

  value = BoolPrim(
    evaluated = EvaluatedOutputs,
    default_val = False )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    return BoolPrim(
      evaluated = EvaluatedOutputs,
      default_val = self.value,
      default_eval = self.default_val if not is_valued( self.value ) else required,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class IntOutput( BaseOutput ):
  """Integer output value
  """
  schema = dict(
    declared = int_declared )

  default_val = IntPrim(
    default_val = 0 )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    return IntPrim(
      default_val = self.default_val,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class IntOutputMain( IntOutput ):

  value = IntPrim(
    evaluated = EvaluatedOutputs,
    default_val = 0 )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    return IntPrim(
      evaluated = EvaluatedOutputs,
      default_val = self.value,
      default_eval = self.default_val if not is_valued( self.value ) else required,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FloatOutput( BaseOutput ):
  """Floating point output value
  """
  schema = dict(
    declared = float_declared )

  default_val = FloatPrim(
    default_val = 0.0 )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    return FloatPrim(
      default_val = self.default_val,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FloatOutputMain( FloatOutput ):

  value = FloatPrim(
    evaluated = EvaluatedOutputs,
    default_val = 0.0 )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    return FloatPrim(
      evaluated = EvaluatedOutputs,
      default_val = self.value,
      default_eval = self.default_val if not is_valued( self.value ) else required,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StrOutput( BaseOutput ):
  """String output value
  """

  schema = dict(
    declared = string_declared )

  default_val = StrPrim(
    default_val = "" )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    return StrPrim(
      default_val = self.default_val,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StrOutputMain( StrOutput ):

  value = StrPrim(
    evaluated = EvaluatedOutputs | CheetahOutputs,
    default_val = "" )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    return StrPrim(
      evaluated = EvaluatedOutputs | CheetahOutputs,
      default_val = self.value,
      default_eval = self.default_val if not is_valued( self.value ) else required,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ListOutput( BaseOutput ):
  """List output value
  """

  schema = dict(
    declared = list_declared )

  item = AnyOutput

  default_val = SeqPrim(
    item = AnyPrim,
    default_val = list() )


  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    return SeqPrim(
      item = self.item.value_schema(
        module = module,
        name = name + '_item' ),
      default_val = self.default_val,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ListOutputMain( ListOutput ):

  value = SeqPrim(
    item = AnyPrim,
    evaluated = EvaluatedOutputs,
    default_val = list() )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    return SeqPrim(
      item = self.item.value_schema(
        module = module,
        name = name + '_item' ),
      evaluated = EvaluatedOutputs,
      default_val = self.value,
      default_eval = self.default_val if not is_valued( self.value ) else required,
      name = name,
      module = module,
      loc = self._loc )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DictOutput( BaseOutput ):
  """Dictionary output value
  """

  schema = dict(
    declared = dict_declared )

  item = AnyOutput

  default_val = MapPrim(
    item = AnyPrim,
    default_val = dict() )


  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    return MapPrim(
      item = self.item.value_schema(
        module = module,
        name = name + '_item' ),
      default_val = self.default_val,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DictOutputMain( DictOutput ):

  value = MapPrim(
    item = AnyPrim,
    evaluated = EvaluatedOutputs,
    default_val = dict() )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):
    return MapPrim(
      item = self.item.value_schema(
        module = module,
        name = name + '_item' ),
      evaluated = EvaluatedOutputs,
      default_val = self.value,
      default_eval = self.default_val if not is_valued( self.value ) else required,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StructOutput( BaseOutput ):
  """Structured output value
  """

  schema = dict(
    declared = struct_declared )

  struct = MapPrim(
    doc = "Specifies the schemas used to validate key-value pairs",
    item = AnyOutput,
    default_val = dict() )

  struct_proxy = StrPrim(
    doc = "Specifies one key that may be populated if the output is not a mapping",
    default_val = optional,
    max_lines = 1,
    max_cols = 80  )

  default_val = MapPrim(
    item = AnyPrim,
    default_val = dict() )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):

    if tag is None:
      tag = "struct"

    struct = list()

    for k,v in self.struct.items():
      struct.append( (k, v.value_schema(
        module = module,
        name = name + f'_{k}' ) ) )

    return StructValued.subclass(
      tag = tag,
      struct = struct,
      struct_proxy = self.struct_proxy,
      default_val = derived,
      name = name,
      module = module,
      loc = self._loc )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StructOutputMain( StructOutput ):

  value = MapPrim(
    item = AnyPrim,
    evaluated = EvaluatedOutputs,
    default_val = optional )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):

    if tag is None:
      tag = "struct"

    struct = list()

    for k,v in self.struct.items():
      struct.append( (k, v.value_schema(
        module = module,
        name = name + f'_{k}' ) ) )

    if is_optional( self.value ):
      default_val = derived
    else:
      default_val = self.value

    if is_valued( self.value ):
      default_eval = required
    else:
      default_eval = self.default_val

    return StructValued.subclass(
      tag = tag,
      struct = struct,
      struct_proxy = self.struct_proxy,
      evaluated = EvaluatedOutputs,
      default_val = default_val,
      default_eval = default_eval,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class UnionOutput( BaseOutput ):
  """Union of any several types of output value
  """
  schema = dict(
    declared = union_declared )

  cases = MapPrim(
    doc = """The possible types that may appear for the union output

    - Max of one case of type `bool`.
    - Max of one numeric case of either type `int` or `float`.
    - Max of one case of type `string`.
    - Max of one case of type `list`.
    - Any number of cases of type `struct`.
    - If there is more than one case of type `struct`, the input mapping must
      contain the ``type`` equal to the corresponding case key.

    """,
    item = AnyUnionOutput,
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

    case_value_schemas = list()

    for k,v in self.cases.items():
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
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class UnionOutputMain( UnionOutput ):

  value = UnionPrim(
    cases = any_prim_cases,
    evaluated = EvaluatedOutputs,
    default_val = optional )

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):

    case_value_schemas = list()

    for k,v in self.cases.items():
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
      evaluated = EvaluatedOutputs,
      default_val = self.value,
      default_case = default_case,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PathOutputValue( StructValued ):

  schema = dict(
    tag = 'path',
    struct_proxy = "path" )

  path = StrPrim(
    doc = "Path relative to run directory.",
    # evaluated = EvaluatedOutputs | RunRelativePathEvaluated,
    max_lines = 1 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PathOutput( BaseOutput ):
  schema = dict(
    tag = 'path' )

  default_val = StrPrim(
    default_val = '',
    doc = "Value used if `value` is an expression that evaluates to None" )

  content_types = ContentTypeList

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):

    return PathOutputValue.subclass(
      tag = self._schema.tag,
      default_val = self.default_val,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PathOutputMain( PathOutput ):

  value = StrPrim(
    evaluated = EvaluatedOutputs | RunRelativePathEvaluated,
    default_val = '',
    doc = "Value assigned to output" )

  content_types = ContentTypeList

  #-----------------------------------------------------------------------------
  def value_schema( self, name, tag = None, module = None ):

    return PathOutputValue.subclass(
      tag = self._schema.tag,
      default_val = self.value,
      default_eval = self.default_val if not is_valued( self.value ) else required,
      evaluated = EvaluatedOutputs | RunRelativePathEvaluated,
      name = name,
      module = module,
      loc = self._loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RunFileOutput( PathOutput ):
  """Path to file in run directory
  """
  schema = dict(
    declared = file_declared )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RunFileOutputMain( PathOutputMain ):
  schema = dict(
    tag = 'file' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RunDirOutput( PathOutput ):
  """Path to directory in run directory
  """
  schema = dict(
    declared = dir_declared )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RunDirOutputMain( PathOutputMain ):
  schema = dict(
    tag = 'dir' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# now that schemas have been defined, resolve from the schema declareds
# AnyOutput = UnionPrim(
#   cases = [ v.schema for v in AnyOutput.cases ] )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
AnyMainOutput = UnionPrim(
  doc = """Union of any output type, including a union of output types
  """,
  cases = [
   BoolOutputMain,
   IntOutputMain,
   FloatOutputMain,
   StrOutputMain,
   ListOutputMain,
   DictOutputMain,
   StructOutputMain,
   UnionOutputMain,
   RunFileOutputMain,
   RunDirOutputMain ] )
