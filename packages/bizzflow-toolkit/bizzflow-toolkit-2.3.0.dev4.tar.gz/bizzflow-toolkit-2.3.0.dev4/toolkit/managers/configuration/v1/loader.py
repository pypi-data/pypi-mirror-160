from toolkit.managers.configuration.loader import BaseConfigurationLoader
from toolkit.managers.configuration.v1.datamarts import DatamartLoader
from toolkit.managers.configuration.v1.extractor import ExtractorLoader
from toolkit.managers.configuration.v1.orchestration import OrchestrationLoader
from toolkit.managers.configuration.v1.sharing import SharingLoader
from toolkit.managers.configuration.v1.step import StepLoader
from toolkit.managers.configuration.v1.transformations import TransformationsLoader
from toolkit.managers.configuration.v1.validators import ProjectValidator
from toolkit.managers.configuration.v1.writers import WriterLoader
from toolkit.managers.credentials import PostgreSQLCredentialManager
from toolkit.managers.credentials.azure_sql import AzureSQLCredentialManager
from toolkit.managers.credentials.gcp import GcpCredentialsManager
from toolkit.managers.credentials.redshift_sql import RedshiftCredentialManager
from toolkit.managers.credentials.snowflake import SnowflakeCredentialsManager
from toolkit.managers.file_storage.abs import ABSFileStorageManager
from toolkit.managers.file_storage.gcs import GcsFileStorageManager
from toolkit.managers.file_storage.local import LocalFileStorageManager
from toolkit.managers.file_storage.s3 import S3FileStorageManager
from toolkit.managers.storage import PostgreSQLStorageManager
from toolkit.managers.storage.azure_sql import AzureSQLStorageManager
from toolkit.managers.storage.bq_sql import BqStorageManager
from toolkit.managers.storage.redshift_sql import RedshiftStorageManager
from toolkit.managers.storage.snowflake_sql import SnowflakeStorageManager
from toolkit.managers.worker.aws import AwsWorkerManager
from toolkit.managers.worker.azure import AzureWorkerManager
from toolkit.managers.worker.gcp import GcpWorkerManager
from toolkit.managers.worker.local import LocalWorkerManager



class V1ConfigurationLoader(BaseConfigurationLoader):
    validatorClass = ProjectValidator
    TransformationLoaderClass = TransformationsLoader
    ExtractorLoaderClass = ExtractorLoader
    WriterLoaderClass = WriterLoader
    DatamartLoaderClass = DatamartLoader
    OrchestrationLoaderClass = OrchestrationLoader
    StepLoaderClass = StepLoader
    SharingLoaderClass = SharingLoader

    @property
    def notification_emails(self):
        return self.project_config["notification_email"]

    def get_storage_manager(self):
        if self._storage_manager is None:
            storage_manager = self.project_config["classes"]["storage_manager"]
            if storage_manager == "SnowflakeStorageManager":
                self._storage_manager = SnowflakeStorageManager(
                    vault_manager=self.get_vault_manager(),
                    account=self.project_config["storage"]["account"],
                    warehouse=self.project_config["storage"]["warehouse"],
                    database=self.project_config["storage"]["database"],
                )
            elif storage_manager == "BqStorageManager":
                self._storage_manager = BqStorageManager(
                    project_id=self.project_id,
                    dataset_location=self.project_config["dataset_location"],
                )
            elif storage_manager == "AzureSQLStorageManager":
                vault_manager = self.get_vault_manager()
                self._storage_manager = AzureSQLStorageManager(
                    host=self.project_config["storage"]["host"],
                    database=self.project_config["storage"]["database"],
                    username="ORCHESTRATOR",
                    password=vault_manager.get_credentials("azure-sql-ORCHESTRATOR"),
                    port=self.project_config["storage"].get("port", 1433),
                    timeout=self.project_config.get("query_timeout", 30),
                    sharing=self.sharing_loader.get_azure_sharing(),
                )
            elif storage_manager == "PostgreSQLStorageManager":
                vault_manager = self.get_vault_manager()
                self._storage_manager = PostgreSQLStorageManager(
                    host=self.project_config["storage"]["host"],
                    database=self.project_config["storage"]["database"],
                    username="ORCHESTRATOR",
                    password=vault_manager.get_credentials("postgresql-ORCHESTRATOR"),
                    port=self.project_config["storage"].get("port", 5432),
                    timeout=self.project_config.get("query_timeout", 30),
                )
            elif storage_manager == "RedshiftStorageManager":
                vault_manager = self.get_vault_manager()
                self._storage_manager = RedshiftStorageManager(
                    database=self.project_config["storage"]["database"],
                    db_user=self.project_config["storage"]["user"],
                    cluster_identifier=self.project_config["storage"]["cluster_identifier"],
                    aws_access_key_id=vault_manager.get_credentials("redshift-aws-access-key-id"),
                    aws_secret_access_key=vault_manager.get_credentials("redshift-aws-secret-access-key"),
                    session_token=vault_manager.get_credentials("redshift-session-token"),
                    region=self.project_config["storage"]["region"],
                )
            else:
                raise NotImplementedError(f"Unsupported storage: {storage_manager}")
        return self._storage_manager

    def get_credentials_manager(self):
        if self._credential_manager is None:
            credential_manager = self.project_config["classes"]["credentials_manager"]
            if credential_manager == "SnowflakeCredentialsManager":
                return SnowflakeCredentialsManager(
                    vault_manager=self.get_vault_manager(),
                    account=self.project_config["storage"]["account"],
                    warehouse=self.project_config["storage"]["warehouse"],
                    database=self.project_config["storage"]["database"],
                )
            elif credential_manager == "GcpCredentialsManager":
                return GcpCredentialsManager(vault_manager=self.get_vault_manager(), project_id=self.project_id)
            elif credential_manager == "AzureSQLCredentialManager":
                return AzureSQLCredentialManager(
                    vault_manager=self.get_vault_manager(),
                    host=self.project_config["storage"]["host"],
                    database=self.project_config["storage"]["database"],
                    port=self.project_config["storage"].get("port", 1433),
                    timeout=self.project_config.get("query_timeout", 30),
                )
            elif credential_manager == "PostgreSQLCredentialManager":
                vault_manager = self.get_vault_manager()
                return PostgreSQLCredentialManager(
                    vault_manager=vault_manager,
                    host=self.project_config["storage"]["host"],
                    database=self.project_config["storage"]["database"],
                    port=self.project_config["storage"].get("port", 5432),
                    timeout=self.project_config.get("query_timeout", 30),
                    user_manager_user="USER_MANAGER",
                    user_manager_password=vault_manager.get_credentials("postgresql-USER_MANAGER"),
                    schema_manager_user="ORCHESTRATOR",
                    schema_manager_password=vault_manager.get_credentials("postgresql-ORCHESTRATOR"),
                )
            elif credential_manager == "RedshiftCredentialManager":
                vault_manager = self.get_vault_manager()
                return RedshiftCredentialManager(
                    vault_manager=vault_manager,
                    database=self.project_config["storage"]["database"],
                    db_user=self.project_config["storage"]["user"],
                    cluster_identifier=self.project_config["storage"]["cluster_identifier"],
                    aws_access_key_id=vault_manager.get_credentials("redshift-aws-access-key-id"),
                    aws_secret_access_key=vault_manager.get_credentials("redshift-aws-secret-access-key"),
                    session_token=vault_manager.get_credentials("redshift-session-token"),
                    region=self.project_config["storage"]["region"],
                )
            else:
                raise NotImplementedError(f"Unsupported storage: {credential_manager}")
        return self._credential_manager

    def get_worker_manager(self):
        if self._worker_manager is None:
            worker_manager = self.project_config["classes"]["worker_manager"]
            worker_machine_config = self.project_config["worker_machine"][0]
            if worker_manager == "GcpWorkerManager":
                self._worker_manager = GcpWorkerManager(
                    name=worker_machine_config["name"],
                    zone=self.project_config["compute_zone"],
                    project_id=self.project_id,
                    host=worker_machine_config["host"],
                    user=worker_machine_config["user"],
                    data_path=worker_machine_config["data_path"],
                    components_path=worker_machine_config["components_path"],
                    config_path=worker_machine_config["config_path"],
                    keep_running=worker_machine_config.get("keep_running", False),
                )
            elif worker_manager == "AwsWorkerManager":
                self._worker_manager = AwsWorkerManager(
                    id=worker_machine_config["id"],
                    region=self.project_config["compute_region"],
                    host=worker_machine_config["host"],
                    user=worker_machine_config["user"],
                    data_path=worker_machine_config["data_path"],
                    components_path=worker_machine_config["components_path"],
                    config_path=worker_machine_config["config_path"],
                    keep_running=worker_machine_config.get("keep_running", False),
                )
            elif worker_manager == "AzureWorkerManager":
                self._worker_manager = AzureWorkerManager(
                    name=worker_machine_config["name"],
                    resource_group=self.project_config["resource_group"],
                    host=worker_machine_config["host"],
                    user=worker_machine_config["user"],
                    data_path=worker_machine_config["data_path"],
                    components_path=worker_machine_config["components_path"],
                    config_path=worker_machine_config["config_path"],
                    keep_running=worker_machine_config.get("keep_running", False),
                )
            elif worker_manager == "LocalWorkerManager":
                self._worker_manager = LocalWorkerManager(
                    data_path=worker_machine_config["data_path"],
                    components_path=worker_machine_config["components_path"],
                    config_path=worker_machine_config["config_path"],
                )
            else:
                raise NotImplementedError(f"Unsupported platform: {worker_manager}")
        return self._worker_manager

    def get_file_storage_manager(self, prefix=""):
        file_storage_manager = self.project_config["classes"]["file_storage_manager"]
        if file_storage_manager == "GcsFileStorageManager":
            return GcsFileStorageManager(
                live_bucket=self.project_config["live_bucket"],
                archive_bucket=self.project_config["archive_bucket"],
                prefix=prefix,
            )
        elif file_storage_manager == "S3FileStorageManager":
            return S3FileStorageManager(
                live_bucket=self.project_config["live_bucket"],
                archive_bucket=self.project_config["archive_bucket"],
                aws_access_key_id=self.get_vault_manager().get_credentials("aws_access_key_id"),
                aws_secret_access_key=self.get_vault_manager().get_credentials("aws_secret_access_key"),
                aws_iam_role=self.project_config["aws_iam_role"],
                prefix=prefix,
            )
        elif file_storage_manager == "ABSFileStorageManager":
            access_key = self.get_vault_manager().get_credentials("blob_storage_account_key")
            return ABSFileStorageManager(
                account_name=self.project_config["azure_blob_account_name"],
                live_container=self.project_config["live_bucket"],
                archive_container=self.project_config["archive_bucket"],
                access_key=access_key,
                blob_storage_credential=self.project_config["storage"].get(
                    "blob_storage_credential", "LIVE_BLOB_STORAGE"
                ),
                prefix=prefix,
            )
        elif file_storage_manager == "LocalFileStorageManager":
            return LocalFileStorageManager(
                live_folder=self.project_config["live_bucket"],
                archive_folder=self.project_config["archive_bucket"],
                prefix=prefix,
            )
        else:
            raise NotImplementedError(f"Unsupported file storage type: {file_storage_manager}")
