"""Azure Worker Manager

Module for managing worker processes.
"""
import json
from logging import getLogger
from subprocess import PIPE, Popen

from toolkit.managers.worker.base import BaseWorkerManager

logger = getLogger(__name__)


class AzureWorkerManager(BaseWorkerManager):
    """Manage worker processes - start, stop, check status"""

    def __init__(self, name, resource_group, host, user, data_path, components_path, config_path, keep_running=False):
        """Initiate Azure Worker Manager"""
        super().__init__(host, user, data_path, components_path, config_path, keep_running)
        self.worker_name = name
        self.resource_group = resource_group

    def start(self):
        """Start worker

        Raises:
            Exception: If problems with starting VM
        """
        fid = Popen(
            f"az vm start --name {self.worker_name} --resource-group {self.resource_group}",
            stdout=PIPE,
            stderr=PIPE,
            shell=True,
        )
        out, err = fid.communicate()
        if fid.returncode == 0:
            logger.info("VM Started successfully")
            return
        logger.error("Problems with starting VM")
        raise Exception(err.decode("utf-8"))

    def stop(self):
        """Stop worker

        Raises:
            Exception: If problems stopping VM
        """
        fid = Popen(
            f"az vm deallocate --name {self.worker_name} --resource-group {self.resource_group}",
            stdout=PIPE,
            stderr=PIPE,
            shell=True,
        )
        out, err = fid.communicate()
        if fid.returncode == 0:
            logger.info("VM stopped successfully")
            return
        logger.error("Problems stopping VM")
        raise Exception(err.decode("utf-8"))

    def get_running(self):
        """Check if worker already running

        Returns:
            boolean -- whether machine is running (True) or not (False), or None on other states (e.g. stopping, pending, terminating)
        Raises:
            Exception: If running state of a VM cannot be queried
        """
        fid = Popen(
            f"az vm show --name {self.worker_name} --resource-group {self.resource_group} --show-details",
            stdout=PIPE,
            stderr=PIPE,
            shell=True,
        )
        out, err = fid.communicate()
        if fid.returncode == 0:
            json_output = json.loads(out)
            if not json_output:
                logger.error("Returned json payload is empty (maybe instance %s does not exist)", self.worker_name)
                raise ValueError(
                    "Returned json payload is empty (maybe instance {} does not exist)".format(self.worker_name)
                )
            state = json_output.get("powerState")
            if state is None:
                logger.error("Returned json payload is empty (maybe instance %s does not exist)", self.worker_name)
                raise ValueError(
                    "Returned json payload is empty (maybe instance {} does not exist)".format(self.worker_name)
                )
            # Return True on running
            if state == "VM running":
                return True
            # Return False on stopped
            if state in ("VM deallocated", "VM stopped"):
                return False
            # Return None on others (pending, stopping, terminating)
            return None
        logger.error("Could not get instances list in json format")
        raise Exception(err.decode("utf-8"))
