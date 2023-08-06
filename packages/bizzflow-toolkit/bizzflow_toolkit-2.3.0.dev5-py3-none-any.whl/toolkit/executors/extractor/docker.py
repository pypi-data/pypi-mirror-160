from logging import getLogger

from toolkit.executors.base.docker import DockerExecutor, DockerOutputMixin

logger = getLogger(__name__)


class DockerExtractorExecutor(DockerOutputMixin, DockerExecutor):
    should_delete_working_kex = False

    def _create_working_kex_name(self):
        norm_component_name = self.storage_manager.normalize_string(self.component_manager.component_name)
        norm_component_id = self.storage_manager.normalize_string(self.component_manager.component_id)
        return "raw_{}_{}".format(norm_component_name, norm_component_id)

    def _create_output_kex_name(self):
        norm_component_name = self.storage_manager.normalize_string(self.component_manager.component_name)
        norm_component_id = self.storage_manager.normalize_string(self.component_manager.component_id)
        return "in_{}_{}".format(norm_component_name, norm_component_id)
