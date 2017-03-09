#! /usr/bin/env python
import os
import subprocess
import sys
import shutil
import argparse


class UserError(Exception):
    pass


def grep_and_sed(src_dir, cur_dir, dst_dir):
    """ Grep and Sed: any mentions of src_dir in files in cur_dir are changed to dst_dir """
    print "All references to %s in all files in %s will be replaced with %s" % (src_dir, cur_dir, dst_dir)
    grep_cmd = subprocess.Popen(['grep', '-Ilre', src_dir, cur_dir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sed_pattern = ''.join(["s|", src_dir, "|", dst_dir, "|g"])
    sed_cmd = subprocess.Popen(['xargs', 'sed', '-i', sed_pattern], stdin=grep_cmd.stdout, stdout=subprocess.PIPE)
    stdout, errcode = sed_cmd.communicate()


def main(src_dir, cur_dir, dst_dir, archer):
    """ Call out the necessary functions."""
    print "I will now create a copy of %s in %s in which all paths point to %s" % (src_dir, cur_dir, dst_dir)

    # shutil.copytree(src_dir, cur_dir, symlinks=False, ignore=shutil.ignore_patterns('*.pyc'))

    # grep_and_sed(src_dir, cur_dir, dst_dir)

    # # If we are on ARCHER, we need to recall that /work/foo is really mounted at /fsX/foo
    # # Using os.path always gives us the /fsX/foo representation, but install scripts sometimes dont resolve
    # # paths. Similarly, /home/bar is really mounted at /homeX/bar.
    # # So, work around this by calling grep_and_sed again with the extra patterns.
    # if archer:
    #     # Firstly, modify the path to look for /fsX and replace that part with /work
    #     src_split = src_dir.split("/")
    #     if src_split[1].startswith("fs"):
    #         src_split[1] = "work"
    #         src_split = '/'.join(src_split)
    #     # Secondly, modify the path to look for /homeX and replace that part with /home
    #     if src_split[1].startswith("home"):
    #         src_split[1] = "home"
    #         src_split = '/'.join(src_split)

    #     grep_and_sed(src_split, cur_dir, dst_dir)

    print "Now ready to compress %s for easy moving to %s.\n" % (cur_dir, dst_dir)
    print "Ie: cd %s && tar -c -f ../firedrake.tar ." % cur_dir


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--existing-location", action="store", help="Path to existing, functional virtualenv.", required=True)
    parser.add_argument("--new-location", action="store", help="Path where the virtualenv will eventually live. Does not need to be accessible from this system.", required=True)
    parser.add_argument("--output-location", action="store", help="Path to a location where the new, modified virtualenv will be written.", required=True)
    parser.add_argument("-a", "--archer", help="If specified, perform ARCHER specific actions (path resolution etc.).", action="store_true")
    args = parser.parse_args()

    if args.existing_location:
        existing = os.path.realpath(args.existing_location)

    if args.new_location:
        newloc = os.path.realpath(args.new_location)

    if args.output_location:
        outputloc = os.path.realpath(args.output_location)

    archer = False
    if args.archer:
        print "ARCHER requested"
        archer = True

    # existing is where the target venv was installed to originally
    # outputloc is where the target venv will be created
    # newloc is where the paths in the target venv will be pointed to, for example /tmp/firedrake
    try:
        main(existing, outputloc, newloc, archer)
    except UserError:
        e = sys.exc_info()[1]
        parser.error(str(e))
