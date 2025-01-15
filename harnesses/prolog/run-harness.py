#!/usr/bin/env python3

import subprocess
import pathlib

#change these for each harness
extensions = (".pl")  # file extensions to check
glob_names = ("main", "*main*", "*")  # globs to check SEQUENTIALLY
def runfile(path: pathlib.Path):
    command_args = ["swipl", "-g", "true.", "-t", "halt.", "--on-error=status", str(path)]
    # command_args = ["gprolog", "--", str(path)]  # experimenting with gprolog
    return subprocess.run(command_args).returncode

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
        exit(32)  # multiple executables
    elif len(executables) == 1:
        rc = runfile(executables[0])
        if rc != 0:
            exit(64 + rc)  # error in user file, subtract 64 to get the error code
        exit(0)

print("HARNESS_ERROR: No executables found")
exit(33)  # no executable