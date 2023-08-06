#!/bin/bash
set -ef -o pipefail

# NOTE: need run_nwl_pkg.sh at least once to package examples

export NWL_MPIEXEC='mpiexec -n {processes} -machinefile {nodefile}'

partis-nwl \
  --find-links ./dist \
  --np 10 \
  --tool mpi_example.mpi_example \
  --inputs mpi_inputs.yml \
  --rundir tmp/mpi_example
