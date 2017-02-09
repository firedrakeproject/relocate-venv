============================================
Using relocate-venv with firedrake on ARCHER
============================================

This README describes how to make use of a relocateable virtualenv on `ARCHER <http://www.archer.ac.uk>`_ which has been made relocatable with the make-moveable script.


*********************
Moving the virtualenv
*********************
Once virtualenv has been made relocatable, you should compress (with tar or another similar utility) the modified virtualenv so that it can be copied to the computes nodes efficiently. If you do not compress it, performing the copy will take a long time as serialisation may occur. The following example assumes your archive is named ``firedrake.tar``, is in the current directory and has the destination set as ``/tmp/firedrake``.

The below bash script can be run on one process per node via aprun with the -N 1 option to copy the archive to the compute node and uncompress it into ``/tmp``

.. code-block:: bash
		
   #!/bin/bash
   cp firedrake.tar /tmp/
   mkdir -p /tmp/firedrake
   cd /tmp/firedrake
   tar -x -f ../firedrake.tar .


***********************************
Activating and using the virtualenv
***********************************

Activating the virtualenv on the compute nodes can be problematic. On ARCHER the MOM node environment (where the PBS script is executed) is mirrored to the compute nodes, providing an easier method. Assuming that the above step has completed, and that the modified firedrake is available at ``/tmp/firedrake``, the following line will activate the virtualenv such that it is useable on the compute nodes without further setup::

  source /tmp/firedrake/bin/activate

********************************
An example PBS script for ARCHER
********************************

The below script will copy the compressed, modified virtualenv to the compute node, unpack it and measure the import time. It also assumes the bash script in the above section is available in the same place as the job script, and archive, as ``copy_firedrake.bash``. Both are available in the ``examples/`` directory of this repository for ease of use.

  .. code-block:: bash
		  
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


