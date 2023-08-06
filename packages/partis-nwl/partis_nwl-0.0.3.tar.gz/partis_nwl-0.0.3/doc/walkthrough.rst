
Example Walk-through
====================

Create and Save New NWL File
............................

.. figure:: ./img/nwl_gui/new_file.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/new_file_nwl.png
  :figwidth: 40 %
  :align: center

.. figure:: ./img/nwl_gui/save.png
  :figwidth: 60 %
  :align: center

Add Inputs
..........

.. figure:: ./img/nwl_gui/add_input.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/rename_key.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/rename_key2.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/edit_label.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/edit_label2.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/edit_multiline.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/edit_multiline2.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/edit_expression.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/edit_expression2.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/edit_expression3.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/edit_expression4.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/edit_expression5.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/select_type.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/add_optional.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/remove_optional.png
  :figwidth: 60 %
  :align: center

Add Outputs
...........

.. figure:: ./img/nwl_gui/add_output.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/add_output2.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/eval_output.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/eval_output2.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/eval_output3.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/eval_output4.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/eval_output5.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/eval_output6.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/cheetah.png
  :figwidth: 60 %
  :align: center

Add Commands
............

.. figure:: ./img/nwl_gui/add_command.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/change_cmd.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/add_arg.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/add_arg2.png
  :figwidth: 60 %
  :align: center

.. figure:: ./img/nwl_gui/add_arg3.png
  :figwidth: 60 %
  :align: center


Tool Definition Save File (yaml)
................................

.. code:: yaml

  type: tool
  label: ''
  version:
  - 0
  - 1
  author:
    name: ''
    email: ''
  inputs:
    second_input:
      type: bool
      label: ''
      doc: ''
      visible: true
      enabled: true
      logs: []
      default_val: false
    first_input:
      type: string
      label: ''
      doc: ''
      visible: true
      enabled: true
      logs: []
      default_val: ''
      max_lines: 1
      selection:
      - label: ''
        doc: ''
        value: my string
    third_input:
      type: union
      label: ''
      doc: ''
      visible: true
      enabled: true
      logs: []
      cases:
        my_case:
          type: wfile
          label: ''
          doc: ''
          visible: true
          enabled: true
          logs: []
        another_case:
          type: list
          label: ''
          doc: ''
          visible: true
          enabled: true
          logs: []
          item:
            type: bool
            label: ''
            doc: ''
            visible: true
            enabled: true
            logs: []
            default_val: false
          default_val: []
  commands:
    new_union_prim:
      type: process
      label: ''
      doc: ''
      env: {}
      enabled: true
      prolog: []
      epilog:
      - level: ERROR
        msg: Command failed from non-zero process exit code
        enabled: $expr:py _.command.returncode != 0
      args:
      - value: echo
        label: ''
        doc: ''
        enabled: true
      - value: ''
        label: ''
        doc: ''
        enabled: true
      stdin: ''
  outputs:
    first_output:
      type: string
      label: ''
      doc: ''
      enabled: true
      logs: []
      value: |-
        $tmpl:cheetah
        #if $_.data.inputs.second_input:
        Is true
        #else
        Is false
        #end if
  prolog: []
  epilog: []
