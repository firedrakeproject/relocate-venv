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
    # grep_cmd = subprocess.Popen(['grep', '-Ilre', src_dir, cur_dir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # sed_pattern = ''.join(["s|", src_dir, "|", dst_dir, "|g"])
    # sed_cmd = subprocess.Popen(['xargs', 'sed', '-i', sed_pattern], stdin=grep_cmd.stdout, stdout=subprocess.PIPE)
    # stdout, errcode = sed_cmd.communicate()


def main(src_dir, new_dir, map_d, archer):
    """ Call out the necessary functions."""
    
    print "Creating a copy of %s in %s" % (src_dir, new_dir)
    # shutil.copytree(src_dir, cur_dir, symlinks=False, ignore=shutil.ignore_patterns('*.pyc'))

    for key in map_d.keys():
        grep_and_sed(key, new_dir, map_d[key])

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

    print "Now ready to compress %s for easy moving.\n" % new_dir
    print "Ie: cd %s && tar -c -f ../firedrake.tar ." % new_dir

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('existing', action='store', help='Path to existing, functional virtualenv.')
    parser.add_argument('--output-location', action='store', help='Path to a location where the new, modified virtualenv will be written.')
    parser.add_argument('--archer', '-a', help='If specified, perform ARCHER specific actions (path resolution etc.).', action='store_true')
    parser.add_argument('--map', '-m', nargs='+', action='append', help='provide a mapping')

    args = parser.parse_args()

    existing = os.path.realpath(args.existing)

    if args.output_location:
        outputloc = os.path.realpath(args.output_location)
    else:
        outputloc = os.path.realpath(os.getcwd() + '/firetemp')
        print outputloc


    # If the user specified a mapping, use that, but sanitise the paths
    if args.map:
        _mapping = dict(args.map)
        mapping_dict={}
        for key in _mapping.keys():
            mapping_dict[os.path.realpath(key)] = os.path.realpath(_mapping[key])
    else:
        mapping_dict=dict([(existing, outputloc)])

    # If on ARCHER, do ARCHER path mods
    archer = False
    if args.archer:
        print "ARCHER requested"
        archer = True


    # Diagnostic
    print "\nMapping Table"
    print "-------------"
    for key in mapping_dict.keys():
        print key, " --> ", mapping_dict[key]
    print "-------------\n"

    # existing is where the target venv was installed to originally
    # outputloc is where the target venv will be created
    # newloc is where the paths in the target venv will be pointed to, for example /tmp/firedrake
    try:
        main(existing, outputloc, mapping_dict, archer)
    except UserError:
        e = sys.exc_info()[1]
        parser.error(str(e))
    



# Provide mechanism to run this as a script if required
if __name__ == '__main__':
    handle_args()
    
