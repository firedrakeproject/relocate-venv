# Using firedrake on ARCHER

## Making the virtualenv movable

The default installation of firedrake does not scale well on ARCHER or any system with a large cor count. To improve import performance, one solution is to make the virtualenv movable, then move it to /tmp (or some other memory resident file-system) on each of the compute nodes.

On a linux-based system, this can be accomplished using make-movable.py. This script takes an existing functional virtualenv and replaces links and paths inside it with references to a new, specified path (usually /tmp/firedrake). This modified virtualenv can then be compressed (e.g. using tar) to be distributed to compute nodes efficiently.

Usage:
```
python make-movable.py <existing-virtualenv-path> <modifiable-virtualenv-path> <node-local-path> (-c, -a)
```

The existing-virtulenv-path and modifiable-virtualenv-path can be equal if yuo wish to modifiy in-place your virtualenv but this is strong *not* recommended. You should either copy your virtualenv first, or, use the optional -c (--copy) flag to have the script create the modifiable version. The node local path can be any path, it does not have to be accessible where you run the script, which is useful for systems with a front-end which is of different configuration to the compute nodes. There is no default, but /tmp/firedrake is generally a good starting point.

## Running with the movable virtualenv

### Moving the virtualenv
Once the script has completed, you should tar (and/or otherwise compress) the modified virtualenv. The following example assumes you have your archive as firedrake.tar in the current directory and the destination is /tmp/firedrake. The below bash script can be run once per node via the systems normal methods, on ARCHER, via aprun with -N 1 for 1 process per node.

```
#!/bin/bash
cp firedrake.tar /tmp/
mkdir -p /tmp/firedrake
cd /tmp/firedrake
tar -x -f ../firedrake.tar .
```

### Activating the virtualenv

Doing this on the compute nodes direct can be problematic, but on ARCHER, at least, the MOM node environment is mirrored to the compute nodes, providing an easier method. Assuming that the above step has completed, and that the modified firedrake is available at: /path/to/modfd

```
source /path/to/modfd/bin/activate
```

### Example PBS Script for ARCHER

The below script will copy the compressed, modified virtualenv to the compute node, unpack it and measure the import time. It also assumes the bash script in the above section is available in the same place as the job script as copy_firedrake.bash


```
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
```

