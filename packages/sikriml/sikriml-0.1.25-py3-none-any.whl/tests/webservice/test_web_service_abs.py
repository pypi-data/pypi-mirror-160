import unittest
from unittest.mock import MagicMock, Mock, patch

from sikriml.webservice import WebserviceAbstract, WebserviceConfiguration

SERVICE_NAME = "scv_name"
config = WebserviceConfiguration(
    "env_name", SERVICE_NAME, "src_dir", "src_script", ["spacy"]
)


class WebserviceAbstractTest(unittest.TestCase):
    @patch.multiple(WebserviceAbstract, __abstractmethods__=set())
    @patch.object(WebserviceAbstract, "_WebserviceAbstract__create_service")
    def test_deploy_should_call_create_service(
        self, create_service_mock: MagicMock
    ):
        # Arrange
        workspace_mock = Mock()
        workspace_mock.webservices.keys.return_value = []
        service_mock = Mock()
        service_mock.state = "Healthy"
        create_service_mock.return_value = service_mock
        self.instance = WebserviceAbstract(workspace_mock, config)  # type: ignore
        # Act
        self.instance.deploy()
        # Assert
        create_service_mock.assert_called_once()
        service_mock.wait_for_deployment.assert_called_once()

    @patch.multiple(WebserviceAbstract, __abstractmethods__=set())
    @patch.object(WebserviceAbstract, "_WebserviceAbstract__update_service")
    def test_deploy_should_call_update_service(
        self, update_service_mock: MagicMock
    ):
        # Arrange
        workspace_mock = Mock()
        workspace_mock.webservices.keys.return_value = [SERVICE_NAME]
        service_mock = Mock()
        service_mock.state = "Healthy"
        update_service_mock.return_value = service_mock
        self.instance = WebserviceAbstract(workspace_mock, config)  # type: ignore
        # Act
        self.instance.deploy()
        # Assert
        update_service_mock.assert_called_once()
        service_mock.wait_for_deployment.assert_called_once()

    @patch.multiple(WebserviceAbstract, __abstractmethods__=set())
    @patch.object(WebserviceAbstract, "_WebserviceAbstract__update_service")
    def test_deploy_update_service_unhealthy_state(
        self, update_service_mock: MagicMock
    ):
        # Arrange
        workspace_mock = Mock()
        workspace_mock.webservices.keys.return_value = [SERVICE_NAME]
        service_mock = Mock()
        service_mock.state = "Unhealthy"
        update_service_mock.return_value = service_mock
        self.instance = WebserviceAbstract(workspace_mock, config)  # type: ignore
        # Assert
        self.assertRaises(Exception, self.instance.deploy)


if __name__ == "__main__":
    unittest.main(verbosity=2)
