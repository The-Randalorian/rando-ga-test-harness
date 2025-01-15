import functools
import pathlib
import typing
import datetime

import docker_interface

MAX_TIME = 60.0

def run_test(image: docker_interface.Image, path: pathlib.Path, max_time: float=MAX_TIME):
    with image.create(networks=None) as container:
        container.copy_into(path, pathlib.Path("/home/nonroot")/path.name)
        start_time = datetime.datetime.now()
        result = container.execute(max_time=max_time)
        end_time = datetime.datetime.now()
        success = False
        if result[0]:
            print(f"{path}: FAIL, OUT OF TIME")
        elif result[1] != 0:
            print(f"{path}: FAIL, ERROR CODE {result[1]}")
        else:
            print(f"{path}: PASS")
            success = True

        with open(path.with_suffix(".result"), "wt") as f:
            ret_code = result[1]-64
            if result[1] == 0:
                ret_code = 0
            f.writelines([
                f"Path: {path}\n",
                f"Ran successfully: {success}\n",
                f"Start time: {start_time}\n",
                f"End time: {end_time}\n",
                f"Run time: {end_time - start_time}\n",
                f"Time limit: {datetime.timedelta(seconds=max_time)}\n",
                f"Ran out of time: {result[0]}\n",
                f"Return code: {ret_code}\n",
                f"Harness code: {result[1]}\n"
            ])
        with open(path.with_suffix(".stdout"), "wb") as f:
            f.write(result[2])
        with open(path.with_suffix(".stderr"), "wb") as f:
            f.write(result[3])

@functools.cache
def get_language_image(
        language: typing.Literal["clips","lisp","prolog","scheme"],
        version: str="latest",
        base_url: str="ghcr.io/the-randalorian/rando-ga-test-harness"
) -> docker_interface.Image:
    return docker_interface.Image(f"{base_url}:{language}-{version}")