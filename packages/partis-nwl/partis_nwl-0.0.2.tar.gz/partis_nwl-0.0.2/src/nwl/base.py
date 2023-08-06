# -*- coding: UTF-8 -*-

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  ModelHint,
  ModelError )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolError( ModelError ):
  pass
