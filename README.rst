#############
relocate-venv
#############

**************************************
Making a Python virtualenv relocatable
**************************************

The default installation of a code into a Python virtualenv, eg `firedrake <http://www.firedrakeproject.org>`_, does not scale well on a supercomputer such as ARCHER, or any system with a large core count. To improve import performance, one solution is to make the virtualenv movable, then move it to /tmp (or some other memory resident file-system) on each of the compute nodes.

On a linux-based system, this can be accomplished using make-movable.py. This script takes an existing functional virtualenv and replaces links and paths inside it with references to a new, specified path (usually /tmp/firedrake). This modified virtualenv can then be compressed (e.g. using tar) to be distributed to compute nodes efficiently.

Usage::
  python make-movable.py <existing-virtualenv-path> <modifiable-virtualenv-path> <node-local-path> (-c, -a)


The existing-virtulenv-path and modifiable-virtualenv-path can be equal if yuo wish to modifiy in-place your virtualenv but this is strong *not* recommended. You should either copy your virtualenv first, or, use the optional -c (--copy) flag to have the script create the modifiable version. The node local path can be any path, it does not have to be accessible where you run the script, which is useful for systems with a front-end which is of different configuration to the compute nodes. There is no default, but /tmp/firedrake is generally a good starting point.
