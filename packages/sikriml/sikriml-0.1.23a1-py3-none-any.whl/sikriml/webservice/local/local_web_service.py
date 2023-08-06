from azureml.core import Workspace
from azureml.core.webservice.local import LocalWebserviceDeploymentConfiguration
from sikriml.webservice import WebserviceAbstract, WebserviceConfiguration


class LocalWebservice(WebserviceAbstract):
    def __init__(
        self,
        workspace: Workspace,
        service_config: WebserviceConfiguration,
        local_config: LocalWebserviceDeploymentConfiguration,
    ):
        WebserviceAbstract.__init__(self, workspace, service_config)
        self.__local_config = local_config

    def _get_deploy_config(self) -> LocalWebserviceDeploymentConfiguration:
        return self.__local_config
