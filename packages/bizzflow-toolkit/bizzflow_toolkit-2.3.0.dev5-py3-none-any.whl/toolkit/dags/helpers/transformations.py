import logging

from toolkit import current_config
from toolkit.dags.helpers.base import PythonTaskCreator

logger = logging.getLogger(__name__)


class TransformationTaskCreator(PythonTaskCreator):
    def __init__(self, transformation_id: str, **kwargs) -> None:
        super().__init__(f"tr_{transformation_id}", **kwargs)
        self.transformation_id = transformation_id

    def python_callable(self):
        transformation_executor = current_config.get_transformation_executor(self.transformation_id)
        try:
            transformation_executor.create_environment()
            transformation_executor.create_input_mapping()
            transformation_executor.run()
            transformation_executor.create_output_mapping()
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            raise
        finally:
            transformation_executor.clean_environment()
