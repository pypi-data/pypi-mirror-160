import unittest
from unittest.mock import Mock

from azureml.core.webservice.local import LocalWebserviceDeploymentConfiguration
from sikriml.webservice import WebserviceConfiguration
from sikriml.webservice.local import LocalWebservice


class LocalWebServiceTest(unittest.TestCase):
    def test_get_deploy_config_returns_correct_type(self):
        # Arrange
        workspace_mock = Mock()
        service_config = WebserviceConfiguration(
            "env_name", "scv_name", "src_dir", "src_script"
        )
        # Act
        aks_service = LocalWebservice(
            workspace_mock,
            service_config,
            LocalWebserviceDeploymentConfiguration(port=80),
        )
        result_config = aks_service._get_deploy_config()
        # Assert
        self.assertTrue(
            isinstance(result_config, LocalWebserviceDeploymentConfiguration)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
