# airflow DAG - need to put these two words here to dagbag recognize this file as file with dags

import logging

from toolkit.dags.helpers.base import DagCreator, SingleTaskGenerator
from toolkit.dags.helpers.refresh_sharing import RefreshSharingTaskCreator

logger = logging.getLogger(__name__)

dag__80_refresh_sharing = DagCreator("80_Refresh_sharing", SingleTaskGenerator(RefreshSharingTaskCreator())).create()
