"""Dummy task to test orchestrations easily
"""
import logging
import time

from toolkit.dags.helpers.base import PythonTaskCreator

logger = logging.getLogger(__name__)


class DummyTaskException(Exception):
    ...


class DummyTaskCreator(PythonTaskCreator):
    def __init__(self, dummy_id: str, **kwargs) -> None:
        self.duration = kwargs.pop("duration", 1)
        self.success = kwargs.pop("success", True)
        super().__init__(f"dummy_{dummy_id}", **kwargs)

    def python_callable(self):
        logger.info("Starting Bizzflow dummy task")
        if self.duration:
            logger.info("Sleeping for %d", self.duration)
            time.sleep(self.duration)
        logger.info(f"Task is designed to {'succeed' if self.success else 'fail'}, so that's what we will do")
        if not self.success:
            raise DummyTaskException("Task was designed to fail and so it did")
