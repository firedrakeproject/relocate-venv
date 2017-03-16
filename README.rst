#############
relocate-venv
#############

**************************************
Making a Python virtualenv relocatable
**************************************

The default installation of a code into a Python virtualenv, eg `firedrake <http://www.firedrakeproject.org>`_, does not scale well on a supercomputer such as ARCHER, or any system with a large core count. To improve import performance, one solution is to make the virtualenv movable, then move it to /tmp (or some other memory resident file-system) on each of the compute nodes.

On a linux-based system, this can be accomplished using `make-movable` This takes an existing functional virtualenv and replaces links and paths inside it with references to a new, specified path (e.g. /tmp/firedrake). This modified virtualenv is then compressed (e.g. using tar) suitable be distributed to compute nodes efficiently.

************
Installation
************

This repository is pip installable. First clone the repository and then use `pip install -e <repo>` to install. One executable is provided, `make-movable`.
You can also invoke the code directly by calling core.py from the relocate_venv subdirectory.

*****
Usage
*****

An existing virtualenv can be made relocatable thus::
  
  make-movable <exsiting-venv>

With no other options, a new virtualenv will be created as a subdirectory of the current directory, named firetemp, which is a copy of the existing virtualenv but with paths pointing to the new location. Additionally, a tar file, firetemp.tar will be created which is simply a tarchive of the virtualenv suitable for moving elsewhere.

There are further optional arguements::
  
  --map [-m] <a> <b> [--map <c> <d>]
  --archer [-a]
  --output-location <location>

The `--map` option allows you to provide a mapping between paths which exist in the source virtualenv (called existing-venv above) and some other location. It is also callable multiple times to build a mapping table. E.g::

  make-movable clock --map /home/foo/bar /tmp/hammer

Would create a copy of the virtualenv in `./clock` as `./firetemp` in which all references to `/home/foo/bar` are replaced with `/tmp/hammer`. This is useful on clusters and big machines where paths can be complex and require some user specification.
 
The `--archer` option adds extra entries to the mapping table, based on those supplied by the user, which resolve some pathing issues on the ARCHER machine.

The `--output-location` option allows specification of the location of the modified virtualenv.
