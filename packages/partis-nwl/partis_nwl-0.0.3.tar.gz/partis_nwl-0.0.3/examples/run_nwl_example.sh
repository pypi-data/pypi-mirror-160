#!/bin/bash
set -ef -o pipefail

# NOTE: need run_nwl_pkg.sh at least once to package examples

partis-nwl -v trace --find-links ./dist --tool nwl_example.data_example --inputs '' --rundir tmp/data_example
partis-nwl --find-links ./dist --tool nwl_example.grep --inputs grep_inputs_query.yml --rundir tmp/grep  --venv-in tmp/data_example/venv_nwlrun
partis-nwl --find-links ./dist --tool nwl_example.module_example --inputs '' --rundir tmp/module_example  --venv-in tmp/data_example/venv_nwlrun
partis-nwl --find-links ./dist --tool nwl_example.generic --inputs generic_inputs_query.yml --rundir tmp/generic  --venv-in tmp/data_example/venv_nwlrun
