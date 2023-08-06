import unittest
from unittest.mock import Mock

from azureml.core.webservice.aci import AciServiceDeploymentConfiguration
from sikriml.webservice import WebserviceConfiguration
from sikriml.webservice.aci import AciWebservice


class AciWebServiceTest(unittest.TestCase):
    def test_get_deploy_config_returns_correct_type(self):
        # Arrange
        workspace_mock = Mock()
        service_config = WebserviceConfiguration(
            "env_name", "scv_name", "src_dir", "src_script"
        )
        # Act
        aks_service = AciWebservice(
            workspace_mock, service_config, AciServiceDeploymentConfiguration()
        )
        result_config = aks_service._get_deploy_config()
        # Assert
        self.assertTrue(isinstance(result_config, AciServiceDeploymentConfiguration))


if __name__ == "__main__":
    unittest.main(verbosity=2)
