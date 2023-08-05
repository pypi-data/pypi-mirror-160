"""Google Cloud Platform Worker Manager

Module for managing worker processes.
"""
import json
from logging import getLogger
from subprocess import PIPE, Popen

from toolkit.managers.worker.base import BaseWorkerManager

logger = getLogger(__name__)


class GcpWorkerManager(BaseWorkerManager):
    """Manage worker processes - start, stop, check status"""

    def __init__(self, name, zone, project_id, host, user, data_path, components_path, config_path, keep_running=False):
        """Initiate GCP Worker Manager"""
        super().__init__(host, user, data_path, components_path, config_path, keep_running)
        self.gcp_worker = name
        self.gcp_zone = zone
        self.gcp_project_id = project_id

    def start(self):
        """Start worker

        Raises:
            Exception: If problems with starting VM
        """
        fid = Popen(
            f"gcloud compute instances start {self.gcp_worker} --zone {self.gcp_zone} --project {self.gcp_project_id}",
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
            f"gcloud compute instances stop {self.gcp_worker} --zone {self.gcp_zone} --project {self.gcp_project_id}",
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
            boolean -- whether machine is running (True) or not (False)
        Raises:
            Exception: If running state of a VM cannot be queried
        """
        fid = Popen(
            f"gcloud compute instances list --format json --project {self.gcp_project_id}",
            stdout=PIPE,
            stderr=PIPE,
            shell=True,
        )
        out, err = fid.communicate()
        if fid.returncode == 0:
            json_output = json.loads(out)
            for o in json_output:
                if o["name"] == self.gcp_worker:
                    return o["status"] == "RUNNING"
        logger.error("Could not get instances list in json format")
        raise Exception(err.decode("utf-8"))
