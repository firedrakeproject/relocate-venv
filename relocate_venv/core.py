#! /usr/bin/env python
import os
import subprocess
import sys
import shutil
import argparse
import glob


class UserError(Exception):
    pass


def grep_and_sed(src_dir, cur_dir, dst_dir):
    """ Grep and Sed: any mentions of src_dir in files in cur_dir are changed to dst_dir """
    # print "All references to %s in all files in %s will be replaced with %s" % (src_dir, cur_dir, dst_dir)
    grep_cmd = subprocess.Popen(['grep', '-Ilre', src_dir, cur_dir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sed_pattern = ''.join(["s|", src_dir, "|", dst_dir, "|g"])
    sed_cmd = subprocess.Popen(['xargs', 'sed', '-i', sed_pattern], stdin=grep_cmd.stdout, stdout=subprocess.PIPE)
    stdout, errcode = sed_cmd.communicate()


def main(src_dir, new_dir, map_d, archer):
    """ Call out the necessary functions."""

    print "Creating a copy of %s in %s" % (src_dir, new_dir)
    shutil.copytree(src_dir, new_dir, symlinks=False, ignore=shutil.ignore_patterns('*.pyc'))

    print "Changing the paths according to the mapping table."
    for key in map_d.keys():
        grep_and_sed(key, new_dir, map_d[key])

    fn = shutil.make_archive(new_dir, 'tar', new_dir)
    print "%s can now be copied elsewhere and used." %(fn)


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('existing', action='store', help='Path to existing, functional virtualenv.')
    parser.add_argument('--output-location', action='store', help='Path to a location where the new, modified virtualenv will be written.')
    parser.add_argument('--archer', '-a', help='If specified, perform ARCHER specific actions (path resolution etc.).', action='store_true')
    parser.add_argument('--map', '-m', nargs='+', action='append', help='provide a mapping')
    args = parser.parse_args()

    # Existing virtualenv to pack up.
    existing = os.path.realpath(args.existing)

    # If user specifies a location for the copy, use that, else default to ./firetemp
    if args.output_location:
        outputloc = os.path.realpath(args.output_location)
    else:
        outputloc = os.path.realpath(os.getcwd() + '/firetemp')
        print outputloc

    # If the user specified a mapping, use that, but sanitise the paths
    if args.map:
        _mapping = dict(args.map)
        mapping_dict = {}
        for key in _mapping.keys():
            mapping_dict[os.path.realpath(key)] = os.path.realpath(_mapping[key])
    else:
        mapping_dict = dict([(existing, outputloc)])

    # If user says they are using ARCHER, do ARCHER path mods
    # These are necessary because not every Python module sanitises and realises paths.
    archer = False
    if args.archer:
        archer = True
        _mapping = mapping_dict
        for key in _mapping.keys():
            mapping_dict[glob.re.sub("/fs\d/", "/work/", key)] = mapping_dict[key]
            mapping_dict[glob.re.sub("/home\d/", "/home/", key)] = mapping_dict[key]
        

    # Diagnostic
    print "\nMapping Table"
    print "-------------"
    for key in mapping_dict.keys():
        print key, " --> ", mapping_dict[key]
    print "-------------\n"

    # existing is where the target venv was installed to originally
    # outputloc is where the target venv will be created
    # mapping_dict is a dict containing the mapping between existing paths, and what they
    # should become.
    try:
        main(existing, outputloc, mapping_dict, archer)
    except UserError:
        e = sys.exc_info()[1]
        parser.error(str(e))


# Provide mechanism to run this as a script if required
if __name__ == '__main__':
    handle_args()
