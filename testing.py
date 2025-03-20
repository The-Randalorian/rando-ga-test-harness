import functools
import pathlib
import typing
import datetime

import docker_interface

MAX_TIME = 60.0


def run_test(output: pathlib.Path, image: docker_interface.Image, paths: pathlib.Path | list[pathlib.Path], max_time: float=MAX_TIME, count=1, evaluator=""):
    success = False
    with image.create(networks=None, environment={"RANDOGRADER_COUNT": count, "RANDOGRADER_EVAL": evaluator}) as container:
        if paths is pathlib.Path:
            paths = [paths]
        for path in paths:
            container.copy_into(path, pathlib.Path("/home/glados")/path.name)
        start_time = datetime.datetime.now()
        result = container.execute(max_time=max_time)
        end_time = datetime.datetime.now()
        if result[0]:
            print(f"{output}: FAIL, OUT OF TIME")
        elif result[1] != 0:
            print(f"{output}: FAIL, ERROR CODE {result[1]}")
        else:
            print(f"{output}: PASS")
            success = True

        with open(output.with_suffix(f"{output.suffix}.result"), "wt") as f:
            ret_code = result[1]-64
            if result[1] == 0:
                ret_code = 0
            f.writelines([
                f"Paths: {[str(path) for path in paths]}\n",
                f"Ran successfully: {success}\n",
                f"Start time: {start_time}\n",
                f"End time: {end_time}\n",
                f"Run time: {end_time - start_time}\n",
                f"Time limit: {datetime.timedelta(seconds=max_time)}\n",
                f"Ran out of time: {result[0]}\n",
                f"Return code: {ret_code}\n",
                f"Harness code: {result[1]}\n"
            ])
        with open(output.with_suffix(f"{output.suffix}.stdout"), "wb") as f:
            f.write(result[2])
        with open(output.with_suffix(f"{output.suffix}.stderr"), "wb") as f:
            f.write(result[3])
    return success

@functools.cache
def get_language_image(
        language: str,
        version: str="latest",
        base_url: str="ghcr.io/the-randalorian/rando-ga-test-harness"
) -> docker_interface.Image:
    return docker_interface.Image(f"{base_url}:{language}-{version}")