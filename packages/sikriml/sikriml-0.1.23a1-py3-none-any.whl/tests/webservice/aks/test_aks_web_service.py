import unittest
from unittest.mock import Mock, patch

from azureml.core.compute import AksCompute
from azureml.core.webservice.aks import AksServiceDeploymentConfiguration, AksWebservice
from azureml.exceptions import ComputeTargetException
from sikriml.webservice.aks import AksWebService, AksWebserviceConfiguration

COMPUTE_TARGET_NAME = "target_name"
CLUSTER_NAME = "cluster_name"
CLUSTER_PURPOSE = AksCompute.ClusterPurpose.DEV_TEST
RESOURCE_GROUP = "resource_group"


service_config = AksWebserviceConfiguration(
    "env_name",
    "scv_name",
    "src_dir",
    "src_script",
    CLUSTER_NAME,
    COMPUTE_TARGET_NAME,
    CLUSTER_PURPOSE,
)

deploy_config = AksWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)


class AksWebServiceTest(unittest.TestCase):
    @patch("sikriml.webservice.aks.aks_web_service.ComputeTarget")
    def test_get_deployment_target_returns_existing_target(
        self, compute_target_mock: Mock
    ):
        # Arrange
        workspace_mock = Mock()
        # Act
        aks_service = AksWebService(workspace_mock, service_config, deploy_config)
        result_target = aks_service._get_deployment_target()
        # Assert
        compute_target_mock.assert_called_once_with(workspace_mock, COMPUTE_TARGET_NAME)
        self.assertEqual(result_target, compute_target_mock())

    @patch("sikriml.webservice.aks.aks_web_service.ComputeTarget")
    @patch("sikriml.webservice.aks.aks_web_service.AksCompute")
    def test_get_deployment_target_attaches_new_target(
        self, aks_compute_mock: Mock, compute_target_mock: Mock
    ):
        # Arrange
        workspace_mock = Mock()
        workspace_mock.resource_group = RESOURCE_GROUP
        compute_target_mock.side_effect = ComputeTargetException("not found")
        attach_config_mock = Mock()
        aks_compute_mock.attach_configuration = Mock(return_value=attach_config_mock)
        aks_target_mock = Mock()
        compute_target_mock.attach = Mock(return_value=aks_target_mock)
        # Act
        aks_service = AksWebService(workspace_mock, service_config, deploy_config)
        result = aks_service._get_deployment_target()
        # Assert
        aks_compute_mock.attach_configuration.assert_called_once_with(
            resource_group=RESOURCE_GROUP,
            cluster_name=CLUSTER_NAME,
            cluster_purpose=CLUSTER_PURPOSE,
        )
        compute_target_mock.attach.assert_called_once_with(
            workspace_mock, COMPUTE_TARGET_NAME, attach_config_mock
        )
        aks_target_mock.wait_for_completion.assert_called_once()
        self.assertEqual(result, aks_target_mock)

    def test_get_deploy_config_returns_correct_type(self):
        # Arrange
        workspace_mock = Mock()
        # Act
        aks_service = AksWebService(workspace_mock, service_config, deploy_config)
        result_config = aks_service._get_deploy_config()
        # Assert

        self.assertTrue(isinstance(result_config, AksServiceDeploymentConfiguration))


if __name__ == "__main__":
    unittest.main(verbosity=2)
