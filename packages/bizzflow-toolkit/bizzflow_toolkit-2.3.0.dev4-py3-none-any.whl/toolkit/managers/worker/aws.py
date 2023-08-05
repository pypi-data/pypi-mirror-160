"""AWS Worker Manager

Module for managing worker processes.
"""
import json
from logging import getLogger
from subprocess import PIPE, Popen

from toolkit.managers.worker.base import BaseWorkerManager

logger = getLogger(__name__)


class AwsWorkerManager(BaseWorkerManager):
    """Manage worker processes - start, stop, check status"""

    def __init__(self, id, region, host, user, data_path, components_path, config_path, keep_running=False):
        """Initiate AWS Worker Manager"""
        super().__init__(host, user, data_path, components_path, config_path, keep_running)
        self.aws_worker = id
        self.aws_region = region

    def start(self):
        """Start worker

        Raises:
            Exception: If problems with starting VM
        """
        fid = Popen(
            "aws ec2 start-instances --instance-ids {0} --region {1}".format(self.aws_worker, self.aws_region),
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
            "aws ec2 stop-instances --instance-ids {0} --region {1}".format(self.aws_worker, self.aws_region),
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

    # TODO: Return named constants instead of True / False and None (such as STATE_STOPPED, STATE_RUNNING, STATE_STOPPING, etc.)
    def get_running(self):
        """Check if worker already running

        Returns:
            boolean -- whether machine is running (True) or not (False), or None on other states (e.g. stopping, pending, terminating)
        Raises:
            Exception: If running state of a VM cannot be queried
        """
        fid = Popen(
            "aws ec2 describe-instances --instance-id {0} --query 'Reservations[*].Instances[*].State[].Name[]' --output json".format(
                self.aws_worker
            ),
            stdout=PIPE,
            stderr=PIPE,
            shell=True,
        )
        out, err = fid.communicate()
        if fid.returncode == 0:
            json_output = json.loads(out)
            if not json_output:
                logger.error("Returned json payload is empty (maybe instance %s does not exist)", self.aws_worker)
                raise ValueError(
                    "Returned json payload is empty (maybe instance {} does not exist)".format(self.aws_worker)
                )
            state = json_output[0]
            # Return True on running
            if state == "running":
                return True
            # Return False on stopped
            if state == "stopped":
                return False
            # Return None on others (pending, stopping, terminating)
            return None
        logger.error("Could not get instances list in json format")
        raise Exception(err.decode("utf-8"))
