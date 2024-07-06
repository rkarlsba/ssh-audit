#!/usr/bin/env python3
# Some docs and vim stuff{{{
#
# vim:ts=4:sw=4:sts=4:et:ai:fdm=marker
#
# src/ssh_audit/ssh_audit.py wrapper for backwards compatibility"""
#
# Forked by Roy Sigurd Karlsbakk <roy@karlsbakk.net> 2024-07-06
#
# }}}
# Global libs {{{

import argparse
import multiprocessing
import platform
import sys
import traceback
from pathlib import Path

# }}}
# Globals {{{

builtinhelp = False
verbose = 1
printallvars = False
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

# }}}
# Local libs {{{

from ssh_audit.ssh_audit import main  # noqa: E402
from ssh_audit import exitcodes  # noqa: E402

# }}}
# def Verbose {{{

def Verbose(s):
    if verbose > 0:
        print(s)

# }}}
# Main {{{

if __name__ == "__main__":
    # Parse args {{{

    argparser = argparse.ArgumentParser(add_help=builtinhelp)
    if not builtinhelp:
        argparser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")
    argparser.add_argument("-v", "--verbose", action="count", default=0, help="Increase output verbosity")
    args = argparser.parse_args()

    if args.verbose:
        verbose = args.verbose

    print(f"Verbose is {args.verbose} and help is {args.help}");
    if not builtinhelp and args.help:
        argparser.print_help()
        exit(0)

    # }}}
    # And the rest {{{

    # Might be needed for PyInstaller (Windows) builds.
    # But then, it might not https://stackoverflow.com/questions/24374288/where-to-put-freeze-support-in-a-python-script
    if platform.system() == 'Windows':
        Verbose('Running on windoze - yuch!')
        multiprocessing.freeze_support()

    exit_code = exitcodes.GOOD
    try:
        exit_code = main()
    except Exception:
        exit_code = exitcodes.UNKNOWN_ERROR
        print(traceback.format_exc())

    sys.exit(exit_code)

    # }}}

# }}}
