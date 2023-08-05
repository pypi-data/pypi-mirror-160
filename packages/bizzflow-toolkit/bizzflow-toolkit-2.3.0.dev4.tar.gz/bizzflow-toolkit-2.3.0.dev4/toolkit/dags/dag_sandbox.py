# airflow DAG - need to put these two words here to dagbag recognize this file as file with dags

import logging

from toolkit.dags.helpers.base import DagCreator, SingleTaskGenerator
from toolkit.dags.helpers.sandboxes import SandboxTaskCreator

logger = logging.getLogger(__name__)

dag__90_update_toolkit = DagCreator(
    "80_Sandbox", SingleTaskGenerator(SandboxTaskCreator()), is_paused_upon_creation=False, tags=["🧸 sandbox"]
).create()
