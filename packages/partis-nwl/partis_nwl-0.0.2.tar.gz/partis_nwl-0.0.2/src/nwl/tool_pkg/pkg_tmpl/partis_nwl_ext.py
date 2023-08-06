

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_tools():
  from . import tools
  from partis.schema.plugin import (
    SchemaPluginGroup )

  plugins = list()

  for tool in tools:
    plugins.append( SchemaPluginGroup(
      label = tool.tool.info.label,
      schemas = {
        'Inputs' : tool.results.results.data.inputs,
        'Results' : tool.results.results } ) )

  return plugins

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_editors():
  from . import tools
  from partis.view.edit.plugin import (
    EditorPluginGroup )

  from partis.view.edit import (
    SchemaStructTreeFileEditor )

  from partis.nwl.view import (
    ToolResultsEditor )

  plugins = list()

  for tool in tools:
    plugins.append( EditorPluginGroup(
      label = tool.tool.info.label,
      editors = {
        'Inputs' : SchemaStructTreeFileEditor.specialize_schema(
          tool.results.results.data.inputs ),
        'Results' : ToolResultsEditor.specialize_schema(
          tool.results.results ) } ) )

  return plugins
