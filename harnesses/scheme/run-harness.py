#!/usr/bin/env python3

import subprocess
import pathlib

#change these for each harness
extensions = (".scm", ".sps", ".ss", ".sls", ".sld", ".sc", ".sch")  # file extensions to check
glob_names = ("main", "*main*", "*")  # globs to check SEQUENTIALLY
def runfile(path: pathlib.Path):
    return subprocess.run(["scheme", "--batch-mode", "--load", str(path)]).returncode

working_dir = pathlib.Path(".")


# the rest of this code should stay the same

# search for a given file name glob (re)
for glob_start in glob_names:
    # search for correct file types
    executables = []
    for extension in extensions:
        executables.extend(working_dir.glob("*" + extension, case_sensitive=False))

    # multiple executables is not allowed
    if len(executables) > 1:
        print("HARNESS_ERROR: Multiple executables found")
        exit(1002)  # multiple executables
    elif len(executables) == 1:
        rc = runfile(executables[0])
        if rc != 0:
            exit(2000 + rc)  # error in user file, subtract 2000 to get the error code
        exit(0)

print("HARNESS_ERROR: No executables found")
exit(1001)  # no executable