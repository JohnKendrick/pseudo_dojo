#!/usr/bin/env python
"""
Script to rename pseudodojo files under revision control (git)
"""
from __future__ import unicode_literals, division, print_function, absolute_import

import sys
import os
import json

def main():
    usage = "Usage: dojo_runemall.py pseudo"
    if "--help" in sys.argv or "-h" in sys.argv:
        print(usage)
        return 1
    try:
        path = sys.argv[1]
    except:
        print(usage)
        return 1

    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise ValueError("%s does not exist" % path)
    basename = os.path.basename(path)

    retcode = 0
    for trial in ["gbrv", "df", "phgamma", "ghosts"]:
        workdir, logfile = basename + "_df", basename + "_df.log"
        cmd = "nohup dojorun.py %s -w %s --trials=df > %s &" % (workdir, logfile, basename)
        print("Executing:", cmd, newline="")
        retcode += os.system(cmd)
        print("retcode", retcode)

    return retcode

if __name__ == "__main__":
    sys.exit(main())
