#!/usr/bin/env python3

import subprocess
import pathlib
import os

#change these for each harness
extensions = ("clp")  # file extensions to check
glob_names = ("main", "*main*", "*")  # globs to check SEQUENTIALLY
def runfile(paths: list[pathlib.Path]):
    args = ["clips"]
    for path in paths:
        args.append("-f")
        args.append(str(path))
    args.append("-f")
    args.append("/usr/local/bin/run.clp")
    return subprocess.run(args).returncode

working_dir = pathlib.Path(".")


# the rest of this code should stay the same

file_count = int(os.environ.get("RANDOGRADER_COUNT", 1))

# search for a given file name glob (re)
for glob_start in glob_names:
    # search for correct file types
    executables = []
    for extension in extensions:
        executables.extend(working_dir.glob("*" + extension, case_sensitive=False))

    # too many executables is not allowed
    if len(executables) > file_count:
        print("HARNESS_ERROR: Too many executables found")
        exit(32)  # too many executables
    elif len(executables) > 0:
        rc = runfile(executables)
        if rc != 0:
            exit(64 + rc)  # error in user file, subtract 64 to get the error code
        exit(0)

print("HARNESS_ERROR: Not enough executables found")
exit(33)  # no executable