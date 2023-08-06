from azureml.core import Workspace
from azureml.core.compute import AksCompute, ComputeTarget
from azureml.core.webservice.aks import AksServiceDeploymentConfiguration
from azureml.exceptions import ComputeTargetException
from sikriml.webservice import WebserviceAbstract

from .aks_web_service_config import AksWebserviceConfiguration


class AksWebService(WebserviceAbstract):
    def __init__(
        self,
        workspace: Workspace,
        service_config: AksWebserviceConfiguration,
        aks_config: AksServiceDeploymentConfiguration,
    ):
        WebserviceAbstract.__init__(self, workspace, service_config)
        self.__service_config = service_config
        self.__aks_config = aks_config

    def _get_deploy_config(self) -> AksServiceDeploymentConfiguration:
        return self.__aks_config

    def __attach_compute_target(self) -> ComputeTarget:
        attach_config = AksCompute.attach_configuration(
            resource_group=self._workspace.resource_group,
            cluster_name=self.__service_config.cluster_name,
            cluster_purpose=self.__service_config.cluster_purpose,
        )
        aks_target: ComputeTarget = ComputeTarget.attach(
            self._workspace,
            self.__service_config.compute_target_name,
            attach_config,
        )
        # Wait for the attach process to complete
        aks_target.wait_for_completion(show_output=True)
        return aks_target

    def _get_deployment_target(self) -> ComputeTarget:
        try:
            return ComputeTarget(
                self._workspace,
                self.__service_config.compute_target_name,
            )
        except ComputeTargetException:
            return self.__attach_compute_target()
