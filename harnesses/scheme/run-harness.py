#!/usr/bin/env python3

import subprocess
import pathlib

#change these for each harness
extensions = (".scm", ".sps", ".ss", ".sls", ".sld", ".sc", ".sch")  # file extensions to check
glob_names = ("main", "*main*", "*")  # globs to check SEQUENTIALLY
def runfile(path: pathlib.Path):
    subprocess.run(["scheme", "--load", str(path)])

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
        print("Multiple executables found")
        exit(1002)
    elif len(executables) == 1:
        runfile(executables[0])
        exit(0)

print("No executables found")
exit(1001)