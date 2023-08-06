
import sys
import os
import os.path as osp
import pytest
import tempfile
import subprocess

from pprint import pprint

from partis.nwl import (
  Tool )

from partis.schema import (
  SchemaError )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_default():
  tool = Tool()

  assert tool.info.label == 'unknown'
  assert tool.info.author.name == 'unknown'
  assert tool.info.author.email == ''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_run():

  tool = Tool( loads(TOOL) )

  assert tool.info.label == 'Something tool'
  assert tool.info.author.name == 'Nanohmics, Inc.'
  assert tool.info.author.email == 'software.support@nanohmics.com'

  with tempfile.TemporaryDirectory() as tmpdir:
    results = tool.run_wait(
      inputs = loads(INPUTS),
      rundir = tmpdir )

    assert results.runtime.rundir == osp.realpath(tmpdir)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_runner():


  with tempfile.TemporaryDirectory() as tmpdir:
    tool_file = osp.join(tmpdir, 'tool.yml')
    input_file = osp.join(tmpdir, 'input.yml')
    rundir = osp.join(tmpdir, 'rundir')

    with open( tool_file, 'w') as fp:
      fp.write(TOOL)

    with open( input_file, 'w') as fp:
      fp.write(INPUTS)

    subprocess.check_call([
      'partis-nwl',
      '--venv',
      osp.join(tmpdir, 'venv'),
      '-v',
      'trace',
      '--tool',
      tool_file,
      '--inputs',
      input_file,
      '--rundir',
      rundir ])

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

TOOL = """
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
nwl: 1
type: tool
info:
  label: Something tool
  doc: Tool that does something
  version: [0,1]
  author:
    name: Nanohmics, Inc.
    email: software.support@nanohmics.com

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
resources:
  python:
    dependencies:
      - numpy

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
inputs:
  out_file_name:
    type: wfile
    label: Output file
    default_val: out.txt

  a:
    # optional input value
    type: union
    label: A union of several types
    cases:
      its_not_set:
        type: bool
        label: "'b' not specified"
        doc: This makes this input optional

      my_int_type:
        type: int
        label: Optional integer
        doc: More info about integer
        # since this is editable, this is the initial value if this type is selected
        default_val: 0

  enable_it:
    type: bool
    label: Do it?
    doc: Enable doing the something
    default_val: true

  this_is_it:
    # this type is defined by a schema for a 'map'
    type: struct
    label: A mapped input
    enabled: $expr:py _.data.inputs.enable_it
    struct:
      x:
        type: int
        label: Some integer
        doc: This is inputs.this_is_it.x
        default_val: 0
        min: 0
        max: 10

      y:
        # question mark makes this input optional
        type: float
        label: Fractional part
        doc: This is the fractional part of the number
        # conditional statement using python expression
        enabled: $expr:py _.parent.value.x < 1
        default_val: 0.1

        selection:
          - label: "1/10"
            doc: One tenth
            value: 0.1

          - label: "1/100"
            doc: One-hundredth
            value: 0.01

  coord_sys:
    # selection of value from limited possibilities
    type: string
    label: Coords
    doc: Coordinate system to use
    default_val: xyz
    selection:
      - label: Cylindrical (R, Theta, Z)
        doc: Cylindrical (R, Theta, Z) - polar in x-y, cartesian in z
        value: rzt

      - label: Cartesian (X, Y, Z)
        doc: Cartesian (X, Y, Z) - cartesian in x, y, z
        value: xyz

  list_input:
    type: list
    label: A List Input
    doc: Add multiple entries
    item:
      type: union
      cases:
        first_option:
          type: string
          label: First Option

        second_option:
          type: struct
          label: Second Option
          struct:
            repeat_count:
              type: int
              label: Repeat something
              doc: Does the something this many times
              default_val: 1
              min: 0

            nested_list:
              type: list
              label: Nested Array
              doc: Add multiple entries
              item:
                type: struct
                label: First Option
                struct:
                  a:
                    type: bool
                    label: Use it?
                    doc: Enable using x
                    default_val: true
                  x:
                    label: Value to use
                    type: float
                    enabled: $expr:py _.parent.value.a


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
outputs:

  # capture of cmd stdout
  stdout_output:
    type: file
    label: Standard output
    doc: The standard output printed by the tool
    value: |-
      $func:py
      import os
      x = os.path.abspath( _.data.commands.run_program.stdout.path )
      print(x)
      return x

  rendered:
    type: file
    label: Rendered template
    doc: Rendered content of Cheetah template
    value: $expr:py _.data.inputs.out_file_name.path

  parsed_output:
    type: int
    label: Get a number from file
    doc: Sums values from the generated Numpy file
    value: |-
      $func:py
      import numpy as np

      arr = np.load( "arr.npy" )

      return np.sum(arr)

  some_flag:
    type: bool
    label: My boolean
    value: True

  a_list_output:
    type: list
    label: A list output
    value: $expr:py [ "list with different item cases", True, 12.34, None ]
    item:
      type: union
      label: A union of several types
      default_case: third_opt
      cases:
        first_opt:
          type: bool
          label: First option

        second_opt:
          type: float
          label: Second option

        third_opt:
          type: string
          label: Third option
          value: This ends up being used as a default string value

  a_structured_output:
    type: struct
    label: A structured output
    struct:
      a:
        type: bool
        label: Item A

      b:
        type: bool
        label: Item B
        value: $expr:py _.data.inputs.a == 0

      c:
        type: bool
        label: Item C
        value: $expr:py None
        # expressions returning None for `value` will then use `default_val`
        default_val: True

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
prolog:
  - level: error
    msg: Numpy is required
    enabled: |-
      $func:py
      try:
        import numpy

        return False
      except:
        return True


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
commands:
  #-----------------------------------------------------------------------------
  make_tmpl:
    type: file
    path: $expr:py _.data.inputs.out_file_name.path
    contents: |-
      $tmpl:cheetah
      This was made by the template...


      #if $_.data.inputs.enable_it:
      It's going to do the thing.
      #else
      Not doing it.
      #end if

      $_.data.inputs.this_is_it.x#if $_.data.inputs.this_is_it.x < 1# + $_.data.inputs.this_is_it.y #end if

  #-----------------------------------------------------------------------------
  make_script:
    type: file
    path: run.py
    contents: |-
      import numpy as np
      import sys

      arr = np.array([1,2,3,4])

      np.save( sys.argv[1], arr )

  #-----------------------------------------------------------------------------
  run_script:
    type: process
    label: Runs the python script file created by the previous command
    doc: More info about what this command does
    args: [ python3, run.py, arr ]

  #-----------------------------------------------------------------------------
  evaluate_script:
    type: script
    source: |-
      $func:py

      print(__name__)
      print(__file__)

      import numpy as np
      import sys

      arr = np.array([5,6,7,8])

      np.save( "arr2", arr )

  #-----------------------------------------------------------------------------
  run_program:
    type: process
    label: Built command to run script
    doc: This builds command from bindings
    enabled: $expr:py _.data.inputs.enable_it
    prolog:
      - level: warning
        enabled: $expr:py _.data.inputs.this_is_it.x >= 1
        msg: |-
          $expr:py f"A custom warning about x: {_.data.inputs.this_is_it.x}"

    args: |-
      $func:py

      args = [ "echo", "'hello world'" ]

      return args
"""

INPUTS = """
out_file_name: out.txt
a: false
enable_it: true
this_is_it:
  x: 3
  y: 0.1
coord_sys: xyz
list_input: []
"""
