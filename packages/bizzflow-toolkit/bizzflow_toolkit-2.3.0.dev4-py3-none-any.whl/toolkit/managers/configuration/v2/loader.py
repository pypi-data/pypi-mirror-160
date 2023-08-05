import logging

from toolkit.managers.configuration.loader import BaseConfigurationLoader
from toolkit.managers.configuration.v2.datamarts import DatamartLoader
from toolkit.managers.configuration.v2.extractor import ExtractorLoader
from toolkit.managers.configuration.v2.orchestration import OrchestrationLoader
from toolkit.managers.configuration.v2.transformations import TransformationsLoader
from toolkit.managers.configuration.v2.validators import ProjectValidator
from toolkit.managers.configuration.v2.writers import WriterLoader
from toolkit.managers.credentials.azure_sql import AzureSQLCredentialManager
from toolkit.managers.credentials.gcp import GcpCredentialsManager
from toolkit.managers.credentials.snowflake import SnowflakeCredentialsManager
from toolkit.managers.file_storage.abs import ABSFileStorageManager
from toolkit.managers.file_storage.gcs import GcsFileStorageManager
from toolkit.managers.file_storage.s3 import S3FileStorageManager
from toolkit.managers.storage.azure_sql import AzureSQLStorageManager
from toolkit.managers.storage.bq_sql import BqStorageManager
from toolkit.managers.storage.snowflake_sql import SnowflakeStorageManager
from toolkit.managers.worker.aws import AwsWorkerManager
from toolkit.managers.worker.azure import AzureWorkerManager
from toolkit.managers.worker.gcp import GcpWorkerManager
from toolkit.managers.worker.local import LocalWorkerManager

logger = logging.getLogger(__name__)


class V2ConfigurationLoader(BaseConfigurationLoader):
    validatorClass = ProjectValidator
    TransformationLoaderClass = TransformationsLoader
    ExtractorLoaderClass = ExtractorLoader
    WriterLoaderClass = WriterLoader
    DatamartLoaderClass = DatamartLoader
    OrchestrationLoaderClass = OrchestrationLoader
    StepLoaderClass = NotImplemented

    @property
    def notification_emails(self):
        return self.project_config["notification_emails"]

    def get_storage_manager(self):
        if self._storage_manager is None:
            # TODO refactor storage managers
            storage_backend = self.project_config["storage"]["backend"]
            if storage_backend == "snowflake":
                self._storage_manager = SnowflakeStorageManager(
                    vault_manager=self.get_vault_manager(),
                    account=self.project_config["storage"]["account"],
                    warehouse=self.project_config["storage"]["warehouse"],
                    database=self.project_config["storage"]["database"],
                )
            elif storage_backend == "bigquery":
                self._storage_manager = BqStorageManager(
                    project_id=self.project_id,
                    dataset_location=self.project_config["storage"]["dataset_location"],
                )
            elif storage_backend == "azuresql":
                vault_manager = self.get_vault_manager()
                self._storage_manager = AzureSQLStorageManager(
                    host=self.project_config["storage"]["host"],
                    database=self.project_config["storage"]["database"],
                    username=self.project_config["storage"].get("username", "ORCHESTRATOR"),
                    password=vault_manager.get_credentials(
                        self.project_config["storage"].get("password", "azure-sql-ORCHESTRATOR")
                    ),
                    port=self.project_config["storage"].get("port", 1433),
                    timeout=self.project_config["storage"].get("timeout", 30),
                )
            else:
                NotImplementedError(f"Unsupported storage: {storage_backend}")
        return self._storage_manager

    def get_credentials_manager(self):
        if self._credential_manager is None:
            storage_backend = self.project_config["storage"]["backend"]
            if storage_backend == "snowflake":
                return SnowflakeCredentialsManager(
                    vault_manager=self.get_vault_manager(),
                    account=self.project_config["storage"]["account"],
                    warehouse=self.project_config["storage"]["warehouse"],
                    database=self.project_config["storage"]["database"],
                )
            elif storage_backend == "bigquery":
                return GcpCredentialsManager(vault_manager=self.get_vault_manager(), project_id=self.project_id)
            elif storage_backend == "azuresql":
                return AzureSQLCredentialManager(
                    vault_manager=self.get_vault_manager(),
                    host=self.project_config["storage"]["host"],
                    database=self.project_config["storage"]["database"],
                    port=self.project_config["storage"].get("port", 1433),
                    timeout=self.project_config["storage"].get("timeout", 30),
                )
            else:
                NotImplementedError(f"Unsupported storage: {storage_backend}")
        return self._credential_manager

    def get_worker_manager(self):
        if self._worker_manager is None:
            worker_machine_config = self.project_config["worker_machine"]
            platform = worker_machine_config["platform"]
            if platform == "gcp":
                self._worker_manager = GcpWorkerManager(
                    name=worker_machine_config["name"],
                    zone=worker_machine_config["zone"],
                    project_id=self.project_id,
                    host=worker_machine_config["host"],
                    user=worker_machine_config["user"],
                    data_path=worker_machine_config["data_path"],
                    components_path=worker_machine_config["components_path"],
                    config_path=worker_machine_config["config_path"],
                    keep_running=worker_machine_config["keep_running"],
                )
            elif platform == "aws":
                self._worker_manager = AwsWorkerManager(
                    id=worker_machine_config["id"],
                    region=worker_machine_config["region"],
                    host=worker_machine_config["host"],
                    user=worker_machine_config["user"],
                    data_path=worker_machine_config["data_path"],
                    components_path=worker_machine_config["components_path"],
                    config_path=worker_machine_config["config_path"],
                    keep_running=worker_machine_config["keep_running"],
                )
            elif platform == "azure":
                self._worker_manager = AzureWorkerManager(
                    name=worker_machine_config["name"],
                    resource_group=worker_machine_config["resource_group"],
                    host=worker_machine_config["host"],
                    user=worker_machine_config["user"],
                    data_path=worker_machine_config["data_path"],
                    components_path=worker_machine_config["components_path"],
                    config_path=worker_machine_config["config_path"],
                    keep_running=worker_machine_config["keep_running"],
                )
            elif platform == "onprem":
                self._worker_manager = LocalWorkerManager(
                    data_path=worker_machine_config["data_path"],
                    components_path=worker_machine_config["components_path"],
                    config_path=worker_machine_config["config_path"],
                )
            else:
                NotImplementedError(f"Unsupported platform: {platform}")
        return self._worker_manager

    def get_file_storage_manager(self, prefix=""):
        file_storage_config = self.project_config["file_storage"]
        storage_type = file_storage_config["type"]
        if storage_type == "google_cloud_storage":
            return GcsFileStorageManager(
                live_bucket=file_storage_config["live_bucket"],
                archive_bucket=file_storage_config["archive_bucket"],
                prefix=prefix,
            )
        elif storage_type == "aws_s3":
            return S3FileStorageManager(
                live_bucket=file_storage_config["live_bucket"],
                archive_bucket=file_storage_config["archive_bucket"],
                aws_access_key_id=self.get_vault_manager().get_credentials("aws_access_key_id"),
                aws_secret_access_key=self.get_vault_manager().get_credentials("aws_secret_access_key"),
                aws_iam_role=file_storage_config["aws_iam_role"],
                prefix=prefix,
            )
        elif storage_type == "azure_blob_storage":
            access_key = self.get_vault_manager().get_credentials(
                file_storage_config.get("access_key", "blob_storage_account_key")
            )
            return ABSFileStorageManager(
                account_name=file_storage_config["account_name"],
                live_container=file_storage_config["live_container"],
                archive_container=file_storage_config["archive_container"],
                access_key=access_key,
                blob_storage_credential=self.project_config["storage"].get(
                    "blob_storage_credential", "LIVE_BLOB_STORAGE"
                ),
                prefix=prefix,
            )
        else:
            NotImplementedError(f"Unsupported file storage type: {storage_type}")
