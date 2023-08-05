"""Worker Manager

Module for managing all worker managers on different platforms.
"""
import socket
from logging import getLogger
from typing import TextIO, Union

import paramiko
from fabric import Connection as SSH
from retry_helper import RetryManager

logger = getLogger(__name__)


class BaseWorkerManager:
    """Abstract class for all worker managers on different platforms, e.g. GcpWorkerManager.

    Raises:
        NotImplementedError: If any of methods is not implemented in the child class.
    """

    def __init__(self, host, user, data_path, components_path, config_path, keep_running=False):
        """Initiate Worker Manager."""
        self.data_path = data_path
        self.components_path = components_path
        self.config_path = config_path or "~/.config"
        self.keep_running = keep_running
        self._ssh = SSH(
            host,
            user,
            connect_kwargs={"password": ""},
        )

    def start(self, *args, **kwargs):
        """Start worker."""
        raise NotImplementedError("This method must be overridden")

    def stop(self):
        """Stop worker."""
        raise NotImplementedError("This method must be overridden")

    def get_running(self, *args, **kwargs):
        """Check if worker already running."""
        raise NotImplementedError("This method must be overridden")

    def put(self, source: Union[str, TextIO], destination: str):
        """Put a local file {source} (a file-like object or path) into worker's destination"""
        return self._ssh.put(source, destination, preserve_mode=False)

    def run(self, command, show_command_in_logs=True, **kwargs):
        """Run command in the worker's shell"""
        # TODO: Create subset of methods such as docker_build, docker_run, etc.
        # that will be used instead of running directly any command
        with RetryManager(
            max_attempts=10,
            wait_seconds=5,
            exceptions=(paramiko.ssh_exception.NoValidConnectionsError, TimeoutError, socket.timeout, EOFError),
            reset_func=self.ensure_virtual_machine_is_running,
        ) as retry:
            while retry:
                with retry.attempt:
                    if show_command_in_logs:
                        logger.info(f"Running command '{command}' by ssh")
                    else:
                        logger.info("Running command '********' by ssh")
                    return self._ssh.run(command, **kwargs)

    @RetryManager(max_attempts=60, wait_seconds=5, exceptions=TimeoutError)
    def ensure_virtual_machine_is_running(self):
        logger.info("Ensuring VM is running...")
        running_worker = self.get_running()
        if running_worker is None:
            logger.warning(
                "Virtual Machine is not in either of acceptable states (stopped nor running), we will try to wait before finding out again."
            )
            raise TimeoutError("Virtual Machine cool-down timed out.")
        elif not running_worker:
            logger.info("Starting VM...")
            self.start()
        logger.info("VM is running")
