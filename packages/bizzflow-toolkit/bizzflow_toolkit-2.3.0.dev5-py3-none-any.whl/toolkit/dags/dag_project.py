# airflow DAG - need to put these two words here to dagbag recognize this file as file with dags

import logging

from toolkit import current_config
from toolkit.dags.helpers.base import DagCreator, SingleTaskGenerator
from toolkit.dags.helpers.datamarts import DatamartTaskCreator
from toolkit.dags.helpers.extractors import ExtractorTaskCreator
from toolkit.dags.helpers.orchestrations import OrchestrationTaskGenerator
from toolkit.dags.helpers.transformations import TransformationTaskCreator
from toolkit.dags.helpers.writers import WriterTaskCreator

logger = logging.getLogger(__name__)

logger.info("Creating orchestrations and tasks")


for extractor_id in current_config.get_extractors_ids():
    extractor_name = current_config.get_extractor_name(extractor_id)
    globals()[f"dag__20_Extractor_{extractor_name}_{extractor_id}"] = DagCreator(
        f"20_Extractor_{extractor_name}_{extractor_id}",
        SingleTaskGenerator(ExtractorTaskCreator(extractor_id, notify=False, type="extractor")),
        tags=["🛻 extractor"],
    ).create()

for transformation_id in current_config.get_transformations_ids():
    globals()[f"dag__40_Transformation_{transformation_id}"] = DagCreator(
        f"40_Transformation_{transformation_id}",
        SingleTaskGenerator(
            TransformationTaskCreator(
                transformation_id,
                notify=False,
                type="transformation",
            )
        ),
        tags=["🔁 transformation"],
    ).create()

for datamart_id in current_config.get_datamarts_ids():
    globals()[f"dag__60_Datamart_{datamart_id}"] = DagCreator(
        f"60_Datamart_{datamart_id}",
        SingleTaskGenerator(
            DatamartTaskCreator(
                datamart_id,
                notify=False,
                type="datamart",
            )
        ),
        tags=["📦️ datamart"],
    ).create()

for writer_id in current_config.get_writers_ids():
    writer_name = current_config.get_writer_name(writer_id)
    globals()[f"dag__60_Writer_{writer_name}_{writer_id}"] = DagCreator(
        f"60_Writer_{writer_name}_{writer_id}",
        SingleTaskGenerator(
            WriterTaskCreator(
                writer_id,
                notify=False,
                type="writer",
            )
        ),
        tags=["📄 writer"],
    ).create()

# Orchestration dags needs to be created last so we already know that all tasks pools are created
for orchestration_id in current_config.get_orchestrations_ids():
    orchestration = current_config.get_orchestration(orchestration_id)
    catchup = False
    dag_options = {
        "tags": ["🕛️ orchestration"],
        "schedule_interval": orchestration.schedule,
    }
    globals()[f"dag__00_Orchestration_{orchestration_id}"] = DagCreator(
        f"00_Orchestration_{orchestration_id}",
        OrchestrationTaskGenerator(orchestration.tasks),
        **dag_options,
    ).create()
