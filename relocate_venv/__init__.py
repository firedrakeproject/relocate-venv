# License goes here ...
import sys
import os
import argparse
from .core import main


def entrypt():
    """Entry point for the application script"""
    print("Main in __init__.py")
    print len(sys.argv)
    print sys.argv

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
