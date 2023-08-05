# airflow DAG - need to put these two words here to dagbag recognize this file as file with dags

import logging

from toolkit import current_config
from toolkit.dags.helpers.base import DagCreator
from toolkit.dags.helpers.telemetry import TelemetryOrchestrationTaskGenerator

logger = logging.getLogger(__name__)

if current_config.telemetry.get("generate", True):
    dag__00_Orchestration_bizzflow_telemetry = DagCreator(
        "00_Orchestration_bizzflow_telemetry",
        TelemetryOrchestrationTaskGenerator(),
        tags=["🕛️ orchestration"],
        schedule_interval=current_config.telemetry.get("schedule", "0 1 * * *"),
    ).create()
