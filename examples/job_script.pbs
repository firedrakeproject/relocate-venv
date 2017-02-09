#!/bin/bash --login

#PBS -N firedrake
#PBS -l select=1
#PBS -l walltime=0:05:0
#PBS -A <BUDGET-CODE>

# This shifts to the directory that you submitted the job from
cd $PBS_O_WORKDIR

module swap PrgEnv-cray PrgEnv-gnu
module unload bolt
module unload xalt

# Set up any compilers which may be required
export CC=cc
export CXX=CC
export F90=ftn
export MPICC=cc
export MPICXX=CC
export MPIF90=ftn

# Ensure any linking done is dynamic
export CRAYPE_LINK_TYPE=dynamic

# Load correct system modules
module load cray-libsci
module load cmake
module load python-compute

export PETSC_DIR=/path/to/precompiled/petsc

# Required for pip on ARCHER
export PIP_CERT=/home/y07/y07/cse/curl/7.34.0/lib/ca-bundle.crt

# Be safe by unsetting any existing PYTHONPATH before run
unset PYTHONPATH

export LD_LIBRARY_PATH=/tmp/firedrake/lib:$LD_LIBRARY_PATH
export TMPDIR=/tmp

# Set up firedrake on nodes
aprun -n 1 -N 1 copy_firedrake.sh
# echo "Copy complete."

# Activate the virtualenv on the MOM node as the same environment is used on all compute nodes at aprun time.
source /path/to/modfd/bin/activate

# Run on the compute nodes and measure import time in seconds.
aprun -n 1 -N 1 python -v -c "import time; st=time.time(); import firedrake; print time.time()-st"
