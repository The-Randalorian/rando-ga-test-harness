import contextlib
import pathlib
import subprocess
import random
import typing

# minimal amount of code needed to driver docker for this project.

MAX_TIME = 60.0
INSTANCE_CODE_LENGTH = 32
Empty = object()

class Container:
    def __init__(self, container_id: str, name: str):
        self.container_id = container_id
        self.name = name

    def copy_into(self, src: pathlib.Path, dst: pathlib.Path):
        subprocess.run(["docker", "cp", "-q", src, f"{self.name}:{dst}"])

    def start(self):
        subprocess.run(["docker", "container", "start", "-a", self.container_id])

    def execute(self, max_time = MAX_TIME) -> (bool, int, bytes, bytes):
        con_proc = subprocess.Popen(
            args=["docker", "container", "start", "-a", self.container_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        timeout = True
        try:
            return_code = con_proc.wait(timeout=max_time)
            timeout = False
        except subprocess.TimeoutExpired:
            con_proc.kill()
            return_code = con_proc.wait()
        return timeout, return_code, con_proc.stdout.read(), con_proc.stderr.read()

class Image:
    def __init__(self, url):
        self.url = url
        self.instance_code = ""
        self.counter = 0
        self.reset_instance_code()

    def reset_instance_code(self):
        self.instance_code = "".join(
            random.choices("0123456789abcdefghijklmnopqrstuv", k=INSTANCE_CODE_LENGTH)
        )
        self.counter = 0

    @contextlib.contextmanager
    def create(self, name: str="", networks: object | None | list=Empty) -> Container:
        if len(name) <= 0:
            name = f"test-harness-{self.instance_code}-{self.counter:04}"
            self.counter += 1

        command_args = ["docker", "create"]

        command_args.extend(["--name", name])

        if networks is Empty:
            pass
        elif networks is None:
            command_args.extend(["--network", "none"])
        else:
            for network in networks:
                command_args.extend(["--network", network])

        command_args.append(self.url)

        container_result = subprocess.run(command_args, text=True, stdout=subprocess.PIPE)
        assert container_result.returncode == 0
        container_id = container_result.stdout.strip()
        container = Container(container_id, name)
        try:
            yield container
        finally:
            subprocess.run(["docker", "rm", "-f", container_id], stdout=subprocess.DEVNULL)

    def pull(self):
        subprocess.run(["docker", "pull", "-q", self.url])
        # make a new instance code, just to make clashes or running out less likely
        self.reset_instance_code()