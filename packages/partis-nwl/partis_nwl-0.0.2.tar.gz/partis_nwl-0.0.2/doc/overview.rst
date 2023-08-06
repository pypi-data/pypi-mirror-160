
Overview
========

Data Types
----------

:term:`NWL` follows a strictly defined structure composed of
elementary data types, each with a 'plain text' representation.
There are many additional predefined types, but all are derived as some
composition of the following elementary types:

* ``bool``: boolean True / False values
* ``int``: integer digit values
* ``float``: floating point values
* ``string``: array of encoded characters
* ``list``: ordered sequence of values
* ``dict``: ordered mapping of key-value pairs
* ``struct``: like a ``dict``, but the types are fixed for each key-value pair,
  and each key may be defined by different types.
* ``union``: a set of types

.. note::

  :term:`NWL` itself does not restrict the format of data stored in files,
  but :term:`YAML` is currently the only implemented format for
  loading and saving the :term:`NWL` definitions, inputs, and result files.

  An important, but sometimes subtle, distinction is made in :term:`NWL` that
  **all mappings are assumed to be ordered**.
  This restriction was chosen to provide consistent order for evaluation and
  visualization of mapping fields.
  Care should be taken by third-party serialization to ensure that the order of
  mappings is preserved, which :term:`YAML` amd :term:`JSON` do not specify,
  and which parsing libraries may not enforce by default.

A :term:`NWL Tool` (:class:`~partis.nwl.tool.Tool`) definition consists of four primary sections:

* ``info`` (:mod:`partis.nwl.info`): user-friendly label, version, author, and documentation.
* ``resources`` (:mod:`partis.nwl.resources`): Computational capabilities,
  static data, and program requirements.
* ``inputs`` (:mod:`partis.nwl.inputs`): data schema for the input values.
* ``prolog``: issue messages regarding the ``inputs`` as a whole.
* ``commands`` (:mod:`partis.nwl.commands`): prepares and executes scripts or
  underlying program(s) to achieve the goal of the tool.
* ``outputs`` (:mod:`partis.nwl.outputs`): data schema for the output values.
* ``epilog``: issue messages regarding overall tool execution.

Evaluated Expressions
---------------------

Expressions are non-literal values such as a Python statement/function or a
Cheetah template string.
The actual value used for the field is determined by evaluating the expression,
such as using the Python interpreter or template engine.

Expressions may use input values, run-time information, command results,
or output values depending on where they appear in the tool definition.
All values accessible in an expression are stored within the underscore ``_``
object available in the expression's local context.

Expressions in the inputs context only have access to ``_.data.inputs``.
If the inputs section is hierarchical, then child values may be accessed using
attributes, mapping, or sequence operators.
For example, for the following inputs file, the integer value ``3`` can be
accessed in an expression as ``_.data.inputs.this_is_it.x``:

.. code:: yaml

  this_is_it:
    x: 3


Expressions are embedded as plain-text beginning with the ``$`` escape
character that is followed by a specifier for how the expression is to be
evaluated.
Currently there are three supported types of expressions:

* ``$expr:py``: A :term:`Python` expression, the value being the equivalent
  to using :func:`eval`.

  .. code-block:: yaml

    enabled: $expr:py _.data.inputs.some_input == 3

* ``$func:py``: A :term:`Python` function.
  If there is a ``return`` statement, the value returned is used.

  .. code-block:: yaml

    enabled: |-
      $func:py

      x = ( _.data.inputs.some_input + 2 ) % 3

      return x == 0

* ``$tmpl:cheetah``: A :term:`Cheetah` template for a string.

  .. code-block:: yaml

    value: |-
      $tmpl:cheetah
      #if $_.data.inputs.some_input == 3:
      It's going to do the thing.
      #else
      Not doing it.
      #end if

  .. note::

    Cheetah templates are only available for certain fields that have a string
    value.

Note that the interpreter used to evaluate the ``inputs`` and root
``prolog`` expressions may have limited
capabilities, since these are intended mainly for graphical editors and not the
run-time environment.
Expressions in the ``commands``, ``outputs``, and ``epilog`` are evaluated
by the tool run-time engine, and may make use of import statements
and perform expensive operations.
There are some fields within these sections treated dynamically at different
points in the tool workflow:

* ``enabled``: An expression that can dynamically enable/disable a field or section.
  For logging events and commands the ``enabled`` field controls whether the event
  occurs or whether the command should be executed.

* ``visible``: Controls whether the input should be visible when it is
  *not* enabled.
  A field that is visible may appear disabled or grayed out when not enabled.

* ``value``: For outputs, an expression is used
  to compute the value that is supplied as an output result.

* ``prolog``, ``epilog``: Dynamically triggered and formatted logging events to
  provide additional feedback about the execution of the tool.

* ``contents``, ``source``, ``args``: For commands, expressions used for generating
  file contents, arbitrary scripting actions, and dynamically computed process
  arguments.

The order in which expressions are evaluated at run-time is summarized by the pseudo-code:

* eval ``prolog``
* for each command in ``commands``

  * eval ``enabled``
  * if ``enabled``

    * eval ``prolog``
    * eval  ``contents``, ``source``, ``args``
    * eval ``epilog``

* for each output in ``outputs``

  * eval ``value``

* eval ``epilog``

The ``inputs`` and tool ``prolog`` has access to ``_.data.inputs``.
The commands section has access to ``_.data.inputs``,
``_.runtime``, and ``_.data.commands`` (of preceding commands).
Additionally, a **command** ``epilog`` has access to ``_.command`` that references
the result of the current command.
The outputs section also has access to ``_.data.inputs``,
``_.runtime``, and ``_.data.commands`` with all command results.
Finally, the tool ``epilog`` has access to all of the above plus ``_.data.outputs``.



Logging Events
--------------

Logging events are an optional mechanism to include additional information,
feedback to the user, and error handling.
These may be set in the ``prolog`` or ``epilog`` fields at the root level of
the tool and within each command.
Every log event has three fields: ``level``, ``msg``, and ``enabled``.
The ``enabled`` value controls whether the logging event occurs based on input or
run-time values.
The ``msg`` value is the text string that is to be reported if the log event is enabled.
The ``level`` value marks the severity of the event, and is one of ``DEBUG``, ``INFO``,
``WARNING``, ``ERROR``, or ``CRITICAL``.
All enabled events are saved in the run-time results, but are also printed to the
terminal based on the level set for the runtime.

Logging events specified for inputs may be used by a graphical inputs editor to
provide additional validation or feedback not provided by the NWL specification.

Events specified in the **tool** ``prolog`` are evaluated before
the tool executes, while the ``epilog`` are evaluated after all
commands and outputs have been successfully evaluated.
Similarly, each **command** ``prolog`` is evaluated at run-time before running the command,
and the command ``epilog`` is evaluated after the command has been evaluated.
If any log event is enabled and has a level of ``ERROR`` or ``CRITICAL``, then the tool
will immediately stop in an error state.


Inputs
------

All input types have fields for ``label``, ``doc``, ``visible``, ``enabled``,
and ``default_val`` (``default_case`` for unions).
The ``label`` is used to provide a short, user-friendly name for the input.
Additional information may be placed in the ``doc`` field, which is used to provide
more contextual information about the purpose of the input.
The ``default_val`` is used as the initial value in the graphical inputs editor,
or to fill in a value when one is not provided in the input file when the tool is run.
Note that **all inputs** have a ``default_val`` even if the value is not used at
run-time. If one is not specified, then the value will chosen by the run-time that
is valid according to the schema.


Selections
^^^^^^^^^^

* :class:`partis.nwl.inputs.IntSelectOption`
* :class:`partis.nwl.inputs.FloatSelectOption`
* :class:`partis.nwl.inputs.StringSelectOption`

The ``selection`` field appears on the ``int``, ``float``, and ``string`` input
types that can be used when there is a predefined set of allowed values.
In the graphical inputs editor, this will create a drop-down combo with the
selection as the available options instead of the general input editor.
If the label of each option is a non-empty string, then it is used as the
displayed value instead of the literal value.

Boolean
^^^^^^^

* :class:`partis.nwl.inputs.BoolInput`


Integer
^^^^^^^

* :class:`partis.nwl.inputs.IntInput`

Float
^^^^^

* :class:`partis.nwl.inputs.FloatInput`

String
^^^^^^

* :class:`partis.nwl.inputs.StrInput`

List
^^^^

* :class:`partis.nwl.inputs.ListInput`

The ``list`` input type allows for a variable length list of values.
Each value in the list is validated against the definition in the list's ``item``.
For example, the list definition shown in :numref:`edit_list` would allow a list
of boolean values.

Struct
^^^^^^

* :class:`partis.nwl.inputs.StructInput`

The ``struct`` input type allows for a mapping of pre-defined key-value pairs
defined by the children in the ``struct`` field.
The ``struct_proxy`` field optionally allows a non-mapping value to be given as
an input value, which is assigned as the value for the given key leaving all other
values given by their respective ``default_val``.
However, note that a ``struct_proxy`` may not be used in a struct that is one
of the cases of a ``union``.

Union
^^^^^

* :class:`partis.nwl.inputs.UnionInput`

The ``union`` input type allows the input value to be valid against one of
several possible cases.
In order to prevent ambiguity which case a value corresponds to while parsing
the input file, the cases allowed in the union is restricted to the following
combinations:

- Max of one case of type ``bool``.
- Max of one numeric case of either type ``int`` or ``float``.
- Max of one case of type ``string``.
- Max of one case of type ``list``.
- Any number of cases of type ``struct`` without any ``struct_proxy``.
  If there is more than one case of type ``struct``, the input value must be a
  mapping that has a key ``type`` with a value equal to the corresponding case key
  to distinguish which case is to be used.
- No cases of type ``union``.

The union type has a ``default_case`` instead of ``default_val``, which is the
key of the case that will be used to get the initial/default value.
If the ``default_case`` is not given, then the first case is used as the default.


Commands
--------

The ``commands`` section of the tool defines a sequence of operations to perform
when the tool is executed.
Each command is identified by a unique key that is used to reference the command
during and after its execution.
There are currently four types of commands available that may be used.

File
^^^^

* :class:`~partis.nwl.commands.file.FileCommand`

Create a file in the run directory with given contents.

.. code-block:: yaml

  type: file
  path: path/to/file.txt
  contents: |-
    Some file contents....

By default, the ``contents`` are given as text and encoded as UTF-8.
However, it may be an expression that generates the content of the file

.. code-block:: yaml

  type: file
  path: path/to/file.txt
  contents: |-
    $func:py
    return "Some file contents...."

or, by setting ``content_mode: binary``, the contents given as raw binary data
in the URL- and filesystem-safe Base64 alphabet, which substitutes
``-`` instead of ``+``, and ``_`` instead of ``/``.

.. code-block:: yaml

  type: file
  path: path/to/file.txt
  content_mode: binary
  contents: aGVsbG8gd29ybGQ=

Directory
^^^^^^^^^

* :class:`~partis.nwl.commands.dir.DirCommand`

Create a directory in the run directory.

.. code-block:: yaml

  type: dir
  path: path/to/dir

Process
^^^^^^^

* :class:`~partis.nwl.commands.process.ProcessCommand`

Run a command line program.

.. code-block:: yaml

  type: process
  args: [ 'echo', 'hello world' ]

.. note::

  The first item in the ``args`` list is the base command to run.

  By default, the process ``returncode`` is used to determine if the process
  exited because of an error.
  This is done in the default ``epilog``, and must be preserved, or altered, to
  impose other conditions on the success of the command.

  .. code-block:: yaml

    epilog:
      - level: ERROR
        msg: Command failed from non-zero process exit code
        enabled: $expr:py _.command.returncode != 0

Script
^^^^^^

* :class:`~partis.nwl.commands.script.ScriptCommand`

Run a Python script

.. code-block:: yaml

  type: script
  source: |-
    $func:py

    import numpy as np
    import sys

    arr = np.array([5,6,7,8])

    np.save( "arr2", arr )

The return value of the script is accessible to subsequent commands and output
expressions, and may be composed of the above elementary data types.
Specific validation may be imposed on the return value using the ``result``
field to define a local data schema similar to the final outputs, which may be
useful for the NWL static analysis utilities.

.. code-block:: yaml

  type: script
  result:
    type: struct
    struct:
      x:
        type: float
      y:
        type: string

  source: |-
    $func:py

    return {
      'x' : 1.234,
      'y' : "hello world" }

Example Tool
------------

A complete example is given here for an NWL Tool that wraps a sub-set of
the Linux ``grep`` command, which reads a text file and returns the lines of
the file that match a given pattern.

.. literalinclude:: ../examples/grep.yml
  :language: yaml
  :linenos:
  :emphasize-lines: 8-34
  :caption: grep.yml

In order to run the tool, an input file has to be supplied that matches the
data structure specified in the ``inputs`` section highlighted above.
The :term:`NWL CLI` can be used to generate a template input file that
is filled with default values.

.. code-block:: bash

  partis-nwl --tool grep.yml --template inputs.yml

.. code-block:: yaml
  :caption: inputs.yml

  type: inputs
  invert_match: false
  inclusion_mode: default
  pattern: ''
  files: []


In this case the templated values will not produce anything useful since both
the ``pattern`` and ``files`` remain empty.
An example file to be searched is created in ``text.txt``, and the pattern is set
to ``'tools,'``, which should match all the lines in the file that have the
word 'tools' followed by a comma.

.. note::

  Default values do not need to be explicitly set in the input file.

.. code-block:: none
  :caption: text.txt

  https://en.wikipedia.org/wiki/Tool

  A tool is an object that can extend an individual's ability to modify features
  of the surrounding environment.
  Although many animals use simple tools, only human beings, whose use of stone
  tools dates back hundreds of millennia, have been observed using tools to make
  other tools.
  Early tools, made of such materials as stone, bone, and wood, were used for
  preparation of food, hunting, manufacture of weapons, and working of materials
  to produce clothing and useful artifacts. The development of metalworking made
  additional types of tools possible. Harnessing energy sources such as animal
  power, wind, or steam, allowed increasingly complex tools to produce an even
  larger range of items, with the Industrial Revolution marking an marked
  inflection point in the use of tools. The introduction of automation allowed
  tools to operate with minimal human supervision, further increasing the
  productivity of human labor.

.. code-block:: yaml
  :caption: inputs.yml

  type: inputs
  pattern: 'tools,'
  files: [ 'text.txt' ]

After updating the values, the tool can be run using the :term:`NWL CLI`.
The ``--rundir`` argument tells the runner to generate all out in the given
directory, otherwise it will run in the directory the command was invoked.

.. code-block:: bash

  partis-nwl --tool grep.yml --inputs inputs.yml --rundir tmp

.. code-block:: bash

  root:INFO: Initialized logging: 20
  partis.nwl.__main__:INFO: Tool validation passed
  partis.nwl.__main__:INFO: Inputs validation passed: inputs.yml
  tool.commands.run_grep:INFO: Command configuring
  tool.commands.run_grep:INFO: Command opening
  tool.commands.run_grep:INFO: Started process 14158
  tool.commands.run_grep:INFO: last 3 lines of: partis.tool.commands.run_grep.stdout.txt
  Although many animals use simple tools, only human beings, whose use of stone
  Early tools, made of such materials as stone, bone, and wood, were used for

  tool.commands.run_grep:INFO: last 1 lines of: partis.tool.commands.run_grep.stderr.txt

  tool.commands.run_grep:INFO: Command closing
  partis.nwl.__main__:INFO: Job completed successfully: wall-time 0:00:00.738429 (H:M:S)

Example Output
--------------

In addition to what is printed to the terminal, the complete ``stdout``,
``stderr``, and a ``results`` file is saved in the run directory.

.. code-block:: none
  :caption: tmp/partis.tool.commands.run_grep.stdout.txt

  Although many animals use simple tools, only human beings, whose use of stone
  Early tools, made of such materials as stone, bone, and wood, were used for

The ``results`` file contains a copy of the values for ``inputs`` used to run the tool
( after filling in default values and performing evaluations ),
the processing ``commands``,
the ``outputs`` (in this case, the filename of the ``stdout`` file)
and information on the ``runtime`` environment.

.. code-block:: yaml
  :caption: tmp/nwl.tool.results.yml

  type: results
  data:
    inputs:
      invert_match: false
      inclusion_mode: default
      pattern: tools,
      files:
      - path: /media/cdodd/box/projects/gembio-n1893/partis/examples/nwl/text.txt
    commands:
      run_grep:
        enabled: true
        success: true
        starttime: 116014.251851176
        timeout: 0.0
        walltime: 0.5988925590063445
        logs: []
        env: {}
        args:
        - grep
        - tools,
        - /media/cdodd/box/projects/gembio-n1893/partis/examples/nwl/text.txt
        pid: 14158
        stdin:
          path: ''
        stdout:
          path: partis.tool.commands.run_grep.stdout.txt
        stderr:
          path: partis.tool.commands.run_grep.stderr.txt
        returncode: 0
    outputs:
      main_output:
        path: partis.tool.commands.run_grep.stdout.txt
  runtime:
    success: true
    workdir: /media/cdodd/box/projects/gembio-n1893/partis/examples/nwl
    rundir: /media/cdodd/box/projects/gembio-n1893/partis/examples/nwl/tmp
    cmd_index: 0
    cmd_id: run_grep
    logs: []
    env: {}
    mpiexec: []
    processes: 1
    cpus_per_process: 1
    threads_per_cpu: 1
    gpus_per_process: 0
