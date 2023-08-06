"""Class for Google Cloud Platform service account credentials management.
"""

import json
import logging
import os
from subprocess import PIPE, Popen
from typing import List

from toolkit.base.kex import Kex
from toolkit.managers.credentials.base import BaseCredentialsManager
from toolkit.managers.vault.base import BaseVaultManager

logger = logging.getLogger(__name__)

try:
    import googleapiclient.discovery
    from google.cloud import bigquery
    from google.oauth2 import service_account
except ImportError:
    logger.info("Google Cloud Platform libraries are not installed.")


class GcpCredentialsManager(BaseCredentialsManager):
    """Class for Google Cloud Platform service account credentials management."""

    def __init__(self, vault_manager: BaseVaultManager, project_id: str):
        self.vault_manager = vault_manager
        self.project_id = project_id
        self._credentials = None
        self.__google_api_service = None

    def clean_user_name(self, user_name):
        return user_name.replace("_", "-")

    @property
    def _google_api_service(self):
        if self.__google_api_service is None:
            try:
                with open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"], "r", encoding="utf-8") as fid:
                    credentials_info = json.load(fid)
            except KeyError:
                credentials_info = json.loads(self.vault_manager.get_credentials("google_application_credentials"))
            credentials = service_account.Credentials.from_service_account_info(credentials_info)
            self.__google_api_service = googleapiclient.discovery.build(
                "iam", "v1", credentials=credentials, cache_discovery=False
            )
        return self.__google_api_service

    def create_kex_user(self, kex: Kex, user_name: str):
        """Create service account.
        Create service account with given service account id and get service account info in dictionary.

        Arguments:
            service_account_id {str} -- service account name (part of the sa email before '@')

        Returns:
            {dict} -- service account dict with keys: 'name', 'projectId', 'uniqueId', 'email', 'displayName', 'etag', 'oauth2ClientId'
        """
        service_account_id = self.clean_user_name(user_name)
        logger.info("Creating service account '%s'", service_account_id)
        sa = (
            self._google_api_service.projects()
            .serviceAccounts()
            .create(
                name="projects/" + self.project_id,
                body={"accountId": service_account_id, "serviceAccount": {"displayName": service_account_id}},
            )
            .execute()
        )
        sa_email = sa["email"]
        self._store_credentials(sa_email, user_name)
        return sa

    def grant_kex_permission_to_user(self, kex: Kex, user_name: str, read_only: bool = False):
        # update dateset permissions ("OWNER" ~ BigQuery Data Owner on the dataset level)
        if read_only:
            role = "READER"
        else:
            role = "OWNER"
        service_account_id = self.clean_user_name(user_name)
        sa_email = self._get_service_account(service_account_id)["email"]
        self._grant_dataset_role(kex=kex, sa_email=sa_email, role=role)
        # TODO!!! check permissions get-iam-policy, remove-iam-policy-binding???
        # set permissions: bigquery.jobUser
        self._grant_roles(sa_email=sa_email, roles=["bigquery.jobUser"])

    def delete_user(self, user_name: str):
        logger.info("Skipping deleting user (service account) in GCP")

    def user_exists(self, user_name: str) -> bool:
        service_account_id = self.clean_user_name(user_name)

        service_accounts = self._list_service_accounts()
        for account in service_accounts:
            if service_account_id == account["email"].rsplit("@", 1)[0]:
                return True
        return False

    def get_user_credentials(self, user_name: str):
        """Get service account credentials for corresponding kex (sandbox relevant).

        Returns:
            {dict} -- service account credentials in dictionary
        """
        return json.loads(self.vault_manager.get_credentials(user_name))

    def _list_service_accounts(self) -> List[dict]:
        """Get list of service accounts for given project.

        Returns:
            {lit} -- list of service account dicts with keys: 'name', 'projectId', 'uniqueId', 'email', 'displayName', 'etag', 'oauth2ClientId'
        """

        request = self._google_api_service.projects().serviceAccounts().list(name="projects/{}".format(self.project_id))
        service_accounts = []
        while True:
            response = request.execute()
            service_accounts.extend([sa for sa in response.get("accounts", [])])
            request = (
                self.__google_api_service.projects()
                .serviceAccounts()
                .list_next(previous_request=request, previous_response=response)
            )
            if request is None:
                break
        return service_accounts

    def _get_service_account(self, service_account_id: str):
        """Get service account for given service account id.
        Create service account if not already exists and get service account info in dictionary.

        Arguments:
            service_account_id {str} -- Service account id (name, string before '@')

        Returns:
            {dict} -- service account with keys: 'name', 'projectId', 'uniqueId', 'email', 'displayName', 'etag', 'oauth2ClientId'
        """

        # # list service accounts
        service_accounts = self._list_service_accounts()
        for account in service_accounts:
            if account["email"].rsplit("@", 1)[0] == service_account_id:
                return account

    def _grant_dataset_role(self, kex: Kex, sa_email: str, role: str):
        """Grant role on a dataset level to service account.

        Arguments:
            kex {Kex} -- Kex to grant the role to

            sa_email {str} -- service account email

            role {str} -- role on a dataset level, e.g. 'OWNER', 'READER'
        """

        bq_client = bigquery.Client()
        bq_dataset = bq_client.get_dataset(kex.get_id())
        entries = list(bq_dataset.access_entries)
        if role not in [e.role.lower() for e in entries if e.entity_id == sa_email]:
            entry = bigquery.AccessEntry(
                role=role,
                entity_type="userByEmail",
                entity_id=sa_email,
            )
            entries = list(bq_dataset.access_entries)
            entries.append(entry)
            bq_dataset.access_entries = entries

            bq_dataset = bq_client.update_dataset(bq_dataset, ["access_entries"])
            logger.info("Updated dataset '%s' with modified user permissions, added %s.", bq_dataset.dataset_id, role)
        else:
            logger.info("Service account '%s' already has role '%s' for '%s'.", sa_email, role, bq_dataset.dataset_id)

    def _grant_roles(self, sa_email: str, roles: list):
        """Grant roles on a project level to service account.

        Arguments:
            sa_email {str} -- service account email

            role {list} -- list of strings with roles on a dataset level, e.g. roles = ["bigquery.jobUser"]
        """

        for role in roles:
            f = Popen(
                "gcloud projects add-iam-policy-binding {0} --member serviceAccount:{1} --role roles/{2}".format(
                    self.project_id, sa_email, role
                ),
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
            )
            err, out = f.communicate()
            if f.returncode == 0:
                logger.info("Service account '%s' was granted '%s'", sa_email, role)
            else:
                logger.error(err.decode("utf-8"))
                logger.error(out.decode("utf-8"))
                logger.error("Could not grant '%s' role to '%s'", role, sa_email)
                return False

    def _get_credentials_json(self, sa_email: str, outfile_path: str):
        """Get service account credentials.
        Save credentials to json file.

        Arguments:
            sa_email {str} -- service account email

            outfile_path {str} -- output json file path (including `file_name.json`)
        """

        f = Popen(
            "gcloud iam service-accounts keys create --iam-account {0} {1}".format(sa_email, outfile_path),
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        err, out = f.communicate()
        if f.returncode == 0:
            logger.info("Credentials for '%s' saved to '%s'", sa_email, outfile_path)
        else:
            logger.error(err.decode("utf-8"))
            logger.error(out.decode("utf-8"))
            logger.error("Could not save credentials for '%s' to '%s'", sa_email, outfile_path)
            return False

    def _store_credentials(self, sa_email: str, user_name: str):
        """Store credentials to valut manager.
        Create credentials if not exists and store them to vault manager.

        Arguments:
            sa_email {str} -- service account email
        """

        # store credentials to vault manager if not stored yet
        sa_key = self.vault_manager.get_credentials(user_name)
        if sa_key is None:
            out_credentials = os.path.join("/tmp", "{}.json".format(user_name))
            self._get_credentials_json(sa_email=sa_email, outfile_path=out_credentials)
            logger.info("Creating credentials from gcloud.")
            with open(out_credentials) as fid:
                self.vault_manager.store_credentials(user_name, fid.read())
            os.remove(out_credentials)
        else:
            logger.info("Credentials already in vault manager.")
