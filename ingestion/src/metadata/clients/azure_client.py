#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
Module containing Azure Client
"""

from metadata.generated.schema.security.credentials.azureCredentials import (
    AzureCredentials,
)
from metadata.utils.logger import utils_logger

logger = utils_logger()


class AzureClient:
    """
    AzureClient based on AzureCredentials.
    """

    def __init__(self, credentials: "AzureCredentials"):
        self.credentials = credentials
        if not isinstance(credentials, AzureCredentials):
            self.credentials = AzureCredentials.parse_obj(credentials)

    def create_client(
        self,
    ):
        from azure.identity import (
            ClientSecretCredential,
            DefaultAzureCredential,
            UsernamePasswordCredential,
        )

        try:
            if (
                getattr(self.credentials, "tenantId", None)
                and getattr(self.credentials, "clientId", None)
                and getattr(self.credentials, "clientSecret", None)
            ):
                logger.info("Using Client Secret Credentials")
                return ClientSecretCredential(
                    tenant_id=self.credentials.tenantId,
                    client_id=self.credentials.clientId,
                    client_secret=self.credentials.clientSecret.get_secret_value(),
                )
            elif (
                getattr(self.credentials, "username", None)
                and getattr(self.credentials, "password", None)
                and getattr(self.credentials, "clientId", None)
            ):
                logger.info("Using Username Password Credentials")
                return UsernamePasswordCredential(
                    username=self.credentials.username,
                    password=self.credentials.password,
                    client_id=self.credentials.clientId,
                )
            else:
                logger.info("Using Default Azure Credentials")
                return DefaultAzureCredential()
        except Exception as e:
            logger.error(f"Error creating Azure Client: {e}")
            raise e

    def create_blob_client(self):
        from azure.storage.blob import BlobServiceClient

        try:
            logger.info("Creating Blob Service Client")
            return BlobServiceClient(
                account_url=f"https://{self.credentials.accountName}.blob.core.windows.net/",
                credential=self.create_client(),
            )
        except Exception as e:
            logger.error(f"Error creating Blob Service Client: {e}")
            raise e

    def create_secret_client(self):
        from azure.keyvault.secrets import SecretClient

        try:
            logger.info("Creating Secret Client")
            return SecretClient(
                vault_url=f"https://{self.credentials.vaultName}.vault.azure.net/",
                credential=self.create_client(),
            )
        except Exception as e:
            logger.error(f"Error creating Secret Client: {e}")
            raise e


# from unittest.mock import Mock
# from azure.identity import ClientSecretCredential

# def test_client_secret_credential():
#     mock_send = Mock(return_value=mock_response(json_payload=token_payload))
#     transport = Mock(send=wrap_in_future(mock_send))
#     scope = "scope"
#     credential = ClientSecretCredential("tenant-id", "client-id", "secret", transport=transport)
