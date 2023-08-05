import logging

from toolkit import current_config
from toolkit.dags.helpers.base import PythonTaskCreator

logger = logging.getLogger(__name__)


class WriterTaskCreator(PythonTaskCreator):
    def __init__(self, writer_id: str, **kwargs) -> None:
        super().__init__(f"wr_{writer_id}", **kwargs)
        self.writer_id = writer_id

    def python_callable(self):
        writer_executor = current_config.get_writer_executor(self.writer_id)
        try:
            writer_executor.create_environment()
            writer_executor.create_input_mapping()
            writer_executor.run()
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            raise
        finally:
            writer_executor.clean_environment()
