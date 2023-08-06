import logging

from toolkit import current_config
from toolkit.dags.helpers.base import PythonTaskCreator

logger = logging.getLogger(__name__)


class ExtractorTaskCreator(PythonTaskCreator):
    def __init__(self, extractor_id: str, **kwargs) -> None:
        super().__init__(f"ex_{extractor_id}", **kwargs)
        self.extractor_id = extractor_id

    def python_callable(self):
        extractor_executor = current_config.get_extractor_executor(self.extractor_id)
        try:
            extractor_executor.create_environment()
            extractor_executor.run()
            extractor_executor.create_output_mapping()
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            raise
        finally:
            extractor_executor.clean_environment()
