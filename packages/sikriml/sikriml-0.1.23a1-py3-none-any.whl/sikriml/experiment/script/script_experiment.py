from abc import abstractmethod

from azureml.core import ScriptRunConfig
from azureml.core.workspace import Workspace

from ..experiment_abs import ExperimentAbstract


class ScriptExperiment(ExperimentAbstract[ScriptRunConfig]):
    def __init__(
        self,
        experiment_name: str,
        workspace: Workspace,
    ) -> None:
        """
        Initialize Pipeline.

        :param experiment_name: The name of the experiment
        :type experiment_name: str
        :param workspace: The workspace to submit the Pipeline on.
        :type workspace: azureml.core.workspace.Workspace
        """
        super().__init__(experiment_name, workspace)

    @abstractmethod
    def get_config(self) -> ScriptRunConfig:
        pass
