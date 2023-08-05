"""Local Worker Manager

Module for managing worker containers within onprem Bizzflow instance
"""

from logging import getLogger
from subprocess import PIPE, Popen
from typing import Any, TextIO, Union

from retry_helper import RetryManager

from toolkit.managers.worker.base import BaseWorkerManager

logger = getLogger(__name__)


class PopenError(Exception):
    """Raised on piped processes errors"""

    def __init__(self, returncode: int, stderr: bytes, stdout: bytes, command: str):
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = stdout
        self.command = command
        super().__init__(str(self))

    def __repr__(self) -> str:
        return (
            f"PopenError: Command exited with {self.returncode} code.\n\n"
            f"stdout:\n{self.stdout.decode('utf-8')}\n\n"
            f"stderr:\n{self.stderr.decode('utf-8')}"
        )

    def __str__(self) -> str:
        return self.__repr__()


class PopenResultWrapper:
    """Wraps around Popen to provide interface common with Fabric's Result"""

    def __init__(self, popen: Popen):
        self.popen = popen

    @property
    def ok(self) -> bool:
        """Returns whether the returncode was ok (0) or not (1-255)"""
        return self.popen.returncode == 0

    def __getattr__(self, attr: str) -> Any:
        return getattr(self.popen, attr)


class LocalWorkerManager(BaseWorkerManager):
    """LocalWorkerManager"""

    def __init__(self, data_path, components_path, config_path):
        """Initiate Worker Manager."""
        self.data_path = data_path
        self.components_path = components_path
        self.config_path = config_path or "~/.config"
        self.keep_running = True

    def start(self, *args, **kwargs):
        """Local worker runs all the time"""
        return

    def stop(self):
        """Local worker runs all the time"""
        return

    def get_running(self, *args, **kwargs):
        """Local worker runs all the time"""
        return True

    def put(self, source: Union[str, TextIO], destination: str):
        """Copy a {source} file into {destination}"""
        if isinstance(source, str):
            fid = open(source, "r", encoding="utf-8")
        else:
            fid = source
        with open(destination, "w", encoding="utf-8") as dest_fid:
            dest_fid.write(fid.read())
        fid.close()

    @RetryManager(
        max_attempts=10,
        wait_seconds=5,
        exceptions=(EOFError, OSError, PopenError),
    )
    def run(self, command, show_command_in_logs=True, **kwargs) -> PopenResultWrapper:
        # This is ugly... but I prefer it over installing sudo for bizzflow user
        # For solution, see TODO in base class
        command = command.replace("sudo ", "")
        logger.info(f"Running command '{command if show_command_in_logs else '*****'}' locally")
        with Popen(command, stdout=PIPE, stderr=PIPE, shell=True) as fid:
            out, err = fid.communicate()
            if fid.returncode != 0:
                raise PopenError(fid.returncode, err, out, command)
        return PopenResultWrapper(fid)

    def ensure_virtual_machine_is_running(self):
        """Local worker runs all the time"""
        logger.info("Using local worker for this task")
