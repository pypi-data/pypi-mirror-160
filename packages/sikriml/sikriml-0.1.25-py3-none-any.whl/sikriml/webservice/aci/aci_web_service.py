from azureml.core import Workspace
from azureml.core.webservice.aci import AciServiceDeploymentConfiguration
from sikriml.webservice import WebserviceAbstract, WebserviceConfiguration


class AciWebservice(WebserviceAbstract):
    def __init__(
        self,
        workspace: Workspace,
        service_config: WebserviceConfiguration,
        aci_config: AciServiceDeploymentConfiguration,
    ):
        WebserviceAbstract.__init__(self, workspace, service_config)
        self.__aci_config = aci_config

    def _get_deploy_config(self) -> AciServiceDeploymentConfiguration:
        return self.__aci_config
