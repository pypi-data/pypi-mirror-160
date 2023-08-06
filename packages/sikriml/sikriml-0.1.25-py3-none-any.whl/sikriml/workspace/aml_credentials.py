import pydash as py_
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from sikriml.workspace.errors.personal_access_token_error import (
    PersonalAccessTokenError,
)

WS_CONNECTION_NAME = "sikriml_connection"


class AMLCredentials:
    def __init__(
        self,
        workspace_name: str,
        resource_group: str,
        subscription_id: str,
        tenant_id: str,
        service_principal_id: str,
        service_principal_password: str,
        pat_token: str = None,
    ):
        self.__workspace_name = workspace_name
        self.__resource_group = resource_group
        self.__subscription_id = subscription_id
        self.__pat_token = pat_token

        self.__spn_credentials = {
            "tenant_id": tenant_id,
            "service_principal_id": service_principal_id,
            "service_principal_password": service_principal_password,
        }

    @property
    def workspace_name(self):
        return self.__workspace_name

    @property
    def resource_group(self):
        return self.__resource_group

    @property
    def subscription_id(self):
        return self.__subscription_id

    @property
    def spn_credentials(self):
        return self.__spn_credentials

    def get_workspace(self, set_feed_connection: bool = False) -> Workspace:
        auth = ServicePrincipalAuthentication(**self.__spn_credentials)
        ws = Workspace(
            workspace_name=self.__workspace_name,
            auth=auth,
            subscription_id=self.__subscription_id,
            resource_group=self.__resource_group,
        )
        if not set_feed_connection:
            return ws

        if py_.is_empty(self.__pat_token):
            raise PersonalAccessTokenError("PAT token wasn't provided")

        ws.set_connection(
            name=WS_CONNECTION_NAME,
            category="PythonFeed",
            target="https://pkgs.dev.azure.com",
            authType="PAT",
            value=self.__pat_token,
        )
        return ws
