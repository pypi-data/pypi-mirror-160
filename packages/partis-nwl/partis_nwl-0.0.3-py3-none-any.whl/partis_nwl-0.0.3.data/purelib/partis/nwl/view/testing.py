# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from copy import copy
import logging
import os
import re
import sys
log = logging.getLogger(__name__)

from partis.utils import (
  head )

from PySide2 import QtCore, QtGui, QtWidgets

from partis.schema.serialize.yaml import (
  loads,
  dumps )

from partis.view.base import (
  ToolButton,
  AsyncTarget )

from partis.view.dialog import (
  ProgressDialog )

from partis.view.schema import (
  TreeEditWidget )

from partis.nwl.testing import (
  Test,
  TestSuite,
  TestSuiteResults,
  NWLTestHint )

from partis.view.base import (
  blocked,
  WidgetStack )

from partis.view.edit import SchemaFileEditor

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TestSuiteWidget( SchemaFileEditor ):

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    widget_stack,
    filename = None,
    state = None ):

    if state is None:
      state = TestSuite( TestSuite.schema.init_val )

    super().__init__(
      manager = manager,
      widget_stack = widget_stack,
      filename = filename,
      schema = TestSuite,
      state = state )

    self._config_stack = WidgetStack(
      manager = self._manager )


    self.layout = QtWidgets.QGridLayout( self )
    self.setLayout(self.layout)

    self.layout.setContentsMargins(0,0,0,0)
    self.layout.setSpacing(0)

    self.build_opts = TreeEditWidget(
      manager = self._manager,
      widget_stack = widget_stack,
      schema = TestSuite,
      state = state )

    self.build_opts.state_changed.connect( self.on_build_opts_state_changed )


    self.build_btn = QtWidgets.QPushButton("Run Tests")
    self.build_btn.clicked.connect(self.on_build)


    self.layout.addWidget( self.build_btn, 0, 1 )

    self.layout.addWidget(
      self.build_opts,
      # row
      1,
      # col
      0,
      # rowSpan
      1,
      # colSpan
      2 )

  #-----------------------------------------------------------------------------
  @classmethod
  def guess( self, filename ):
    schema = TestSuite

    try:

      lines = head(
        path = filename,
        n = 10 )

      pattern = rf"^{schema.tag_key}[\t ]*\:[\t ]*{schema.tag}"
      pattern = re.compile(pattern)

      for l in lines:
        if pattern.match( l ):
          return 1.0


    except:
      log.exception("Error while parsing guess", exc_info = True )

    return  0.0

  #-----------------------------------------------------------------------------
  def set_state( self, state ):
    with blocked( self.build_opts ):

      self.build_opts.set_state(
        state = state )


    super().set_state( state )

  #-----------------------------------------------------------------------------
  def on_build_opts_state_changed( self, state ):
    self.state = state

  #-----------------------------------------------------------------------------
  def on_build( self ):

    self._manager._manager._async_queue.append( (self.build, ) )

  #-----------------------------------------------------------------------------
  async def build( self ):

    if self._filename != "":
      fdir = os.path.dirname( self._filename  )
    else:
      fdir = os.getcwd()

    target = AsyncTarget()

    workdir_dialog = QtWidgets.QFileDialog(
      self,
      "Select Working Directory" )

    workdir_dialog.setDirectory( fdir )
    workdir_dialog.setFileMode(QtWidgets.QFileDialog.Directory )
    workdir_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
    workdir_dialog.fileSelected.connect( target.on_result )
    workdir_dialog.filesSelected.connect( target.on_result )
    workdir_dialog.filterSelected.connect( target.on_result )
    workdir_dialog.urlSelected.connect( target.on_result )
    workdir_dialog.urlsSelected.connect( target.on_result )
    workdir_dialog.rejected.connect( target.on_result )
    workdir_dialog.open()

    workdir, error = await target.wait()

    if isinstance( workdir, list ):
      if len(workdir) == 0:
        workdir = None
      else:
        workdir = next(iter(workdir))

    if workdir is None:
      return

    target = AsyncTarget()

    rundir_dialog = QtWidgets.QFileDialog(
      self,
      "Select Run Directory" )

    rundir_dialog.setDirectory( fdir )
    rundir_dialog.setFileMode(QtWidgets.QFileDialog.Directory )
    rundir_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
    rundir_dialog.fileSelected.connect( target.on_result )
    rundir_dialog.filesSelected.connect( target.on_result )
    rundir_dialog.filterSelected.connect( target.on_result )
    rundir_dialog.urlSelected.connect( target.on_result )
    rundir_dialog.urlsSelected.connect( target.on_result )
    rundir_dialog.rejected.connect( target.on_result )
    rundir_dialog.open()

    rundir, error = await target.wait()

    if isinstance( rundir, list ):
      if len(rundir) == 0:
        rundir = None
      else:
        rundir = next(iter(rundir))

    if rundir is None:
      return

    _log = log.getChild("test_suite")
    _log.setLevel( logging.DEBUG )

    self.setEnabled(False)

    pbar = ProgressDialog(
      self._manager,
      with_log = True )

    _log.addHandler( pbar.log_handler )

    pbar.set_title( "Running Test Suite" )
    pbar.set_status( "" )
    pbar.set_range( 0, 0 )
    pbar.show()

    _log.info(f"Working directory: {workdir}")
    _log.info(f"Run directory: {rundir}")

    try:

      test_results = await self.state._run(
        logger = _log,
        workdir = workdir,
        rundir = rundir )

      fail_hints = list()

      if not test_results.success:

        # TODO: give the option to save results somewhere
        failed = list()
        stack = list( test_results.tests.items() )

        while len(stack) > 0:
          path, test = stack.pop(0)

          if not test.success:
            if isinstance( test, TestSuiteResults ):
              for k, _test in test.tests.items():
                stack.append( (f"{path}.{k}", _test) )

            else:
              failed.append( ( path, test ) )

        for path, test in failed:

          fail_hints.append( NWLTestHint(
            msg = f"test: {path}",
            level = 'error',
            hints = [ l._cast() for l in test.logs ] ) )

      result_hint = NWLTestHint(
        msg = f"Tests: {test_results.npass} passed, {test_results.nfail} failed",
        hints = fail_hints )

      if not test_results.success:
        _log.error( result_hint )
      else:
        _log.info( result_hint )


      pbar.set_range( 0, 1 )
      pbar.set_value( 1 )

      # pbar.close()

    except BaseException as e:
      pbar.set_range( 0, 1 )
      pbar.set_value( 0 )

      _log.error("Could not run test suite.", exc_info = True )


    # pbar.hide()

    _log.removeHandler(pbar.log_handler)

    self.setEnabled(True)

  #-----------------------------------------------------------------------------
  async def overwrite( self ):

      target = AsyncTarget()


      message_box = QtWidgets.QMessageBox()
      message_box.setWindowTitle( f"Overwrite" )
      message_box.setWindowIcon( QtGui.QIcon(self._manager.resource_path("images/icons/app_icon.png")) )
      message_box.setStyleSheet( self._manager.stylesheet )
      message_box.setText(
        f"Overwrite existing output package file?")

      message_box.setStandardButtons(
        QtWidgets.QMessageBox.Yes
        | QtWidgets.QMessageBox.Cancel )


      message_box.setDefaultButton( QtWidgets.QMessageBox.Yes )


      message_box.finished.connect( target.on_result )
      message_box.open()

      result, error = await target.wait()

      return result == QtWidgets.QMessageBox.Yes
