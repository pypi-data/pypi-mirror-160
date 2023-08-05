# airflow DAG - need to put these two words here to dagbag recognize this file as file with dags

import logging

from toolkit.dags.helpers.base import DagCreator, SingleTaskGenerator
from toolkit.dags.helpers.upgrade_project import UpdateProjectTaskCreator

logger = logging.getLogger(__name__)

dag__90_update_project = DagCreator("90_update_project", SingleTaskGenerator(UpdateProjectTaskCreator())).create()
