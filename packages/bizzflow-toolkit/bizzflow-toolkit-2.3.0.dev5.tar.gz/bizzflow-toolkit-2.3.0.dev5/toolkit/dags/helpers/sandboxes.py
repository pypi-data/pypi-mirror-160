import logging

from toolkit import current_config
from toolkit.dags.helpers.base import PythonTaskCreator

logger = logging.getLogger(__name__)


class SandboxTaskCreator(PythonTaskCreator):
    def __init__(self):
        super().__init__(
            "sandbox",
            notify=False,
        )

    def get_operator_kwargs(self):
        kwargs = super().get_operator_kwargs()
        kwargs["provide_context"] = True
        return kwargs

    def python_callable(self, **kwargs):
        dag_run_config = kwargs["dag_run"].conf
        transformation_id = dag_run_config.get("transformation_id")
        sandbox_user_email = dag_run_config["sandbox_user_email"]
        clean_sandbox = dag_run_config.get("clean_sandbox", True)
        load_transformation = dag_run_config.get("load_transformation", True)
        additional_kexes = dag_run_config.get("additional_kexes")
        additional_tables = dag_run_config.get("additional_tables")
        dry_run = dag_run_config.get("dry_run", False)
        run_options = dag_run_config.get("run_options", {})

        if transformation_id is None:
            # transformation executor without properly defined component config (input mapping and queries) can just create sandbox
            load_transformation = False
            dry_run = False

        sandbox_manager = current_config.get_sandbox_manager(sandbox_user_email, transformation_id)

        sandbox_manager.create_sandbox()
        if clean_sandbox:
            sandbox_manager.clean_sandbox()
        sandbox_manager.load(
            load_transformation=load_transformation,
            additional_kexes=additional_kexes,
            additional_tables=additional_tables,
        )
        if dry_run:
            sandbox_manager.dry_run(**run_options)
