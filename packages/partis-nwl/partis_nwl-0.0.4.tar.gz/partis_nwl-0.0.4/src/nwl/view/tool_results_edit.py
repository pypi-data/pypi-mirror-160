# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from copy import copy
import re
import logging
log = logging.getLogger(__name__)

from partis.utils import (
  head )

from PySide2 import QtCore, QtGui, QtWidgets

from partis.nwl import (
  ToolResults )

from partis.view.base import (
  blocked,
  WidgetStack )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

from partis.schema import (
  is_mapping,
  is_sequence )

from partis.nwl.context import (
  InputsContext,
  OutputsContext,
  CommandsContext )

from partis.view.edit import SchemaStructTreeFileEditor

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolResultsEditor( SchemaStructTreeFileEditor ):
  default_readonly = True
  guess_strict = True
  default_schema = ToolResults

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    widget_stack,
    schema = None,
    filename = None,
    state = None,
    readonly = None ):

    super().__init__(
      manager = manager,
      widget_stack = widget_stack,
      schema = schema,
      filename = filename,
      state = state,
      readonly = readonly,
      hidden = [] )
