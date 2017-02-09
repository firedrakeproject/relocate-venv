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
    # print "STDOUT:"
    # print stdout
    # print "ERRCODE:"
    # print errcode


def main(src_dir, cur_dir, dst_dir, copy, archer):
    """ Call out the necessary functions."""
    print "I will now create a copy of %s in %s in which all paths point to %s" % (src_dir, cur_dir, dst_dir)

    if copy:
        shutil.copytree(src_dir, cur_dir, symlinks=False, ignore=shutil.ignore_patterns('*.pyc'))

    grep_and_sed(src_dir, cur_dir, dst_dir)

    # If we are on ARCHER, we need to recall that /work/blah is really mounted at /fsX/blah
    # Using os.path always gives us the /fs2 representation, but install scripts sometimes dont resolves
    # paths. So, call grep_and_sed again
    if archer:
        # First, mod the path to look for /fsX and replace that part with /work
        src_split = src_dir.split("/")
        if src_split[1].startswith("fs"):
            src_split[1] = "work"
            src_split = '/'.join(src_split)
        if src_split[1].startswith("home"):
            src_split[1] = "home"
            src_split = '/'.join(src_split)

        grep_and_sed(src_split, cur_dir, dst_dir)

    print "Now ready to compress %s for easy moving to %s.\n" % (cur_dir, dst_dir)
    print "Ie: cd %s && tar -c -f ../firedrake.tar ." % cur_dir


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="Path to existing, functional virtualenv. Note: this may not exist on this system, but is the path which is used inside the virtualenv.")
    parser.add_argument("cur", help="Location of an existing, functional virtualenv, which will be modified. If -c is used, this will be created.")
    parser.add_argument("dst", help="Path where the virtualenv will eventually live. Does not need to be accessible from this system.")
    parser.add_argument("-c", "--copy", help="If specified, src will be copied to cur before modification.", action="store_true")
    parser.add_argument("-a", "--archer", help="If specified, perform ARCHER specific actions (path resolution etc.).", action="store_true")
    args = parser.parse_args()

    src_dir = os.path.normpath(os.path.abspath(args.src))
    cur_dir = os.path.normpath(os.path.abspath(args.cur))
    dst_dir = os.path.normpath(os.path.abspath(args.dst))

    print "Src: %s" % src_dir
    print "Cur: %s" % cur_dir
    print "Dst: %s" % dst_dir
    copy = False
    if args.copy:
        print "Copy requested."
        copy = True
    archer = False
    if args.archer:
        print "ARCHER requested"
        archer = True

    # src_dir is where the target venv was installed to originally
    # cur_dir is where the target venv currently lives, in some cases, this could be a temporary location
    # for example, where you ran "cp -a orig temp" so you didn't break your original before running this
    # cur_dir and src_dir might be the same
    # dst_dir is where the venv will be located at runtime, for example /tmp/firedrake
    try:
        main(src_dir, cur_dir, dst_dir, copy, archer)
    except UserError:
        e = sys.exc_info()[1]
        parser.error(str(e))
