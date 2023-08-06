from azureml.core.workspace import Workspace
from azureml.pipeline.core import Pipeline

from ..experiment_abs import ExperimentAbstract


class PipelineExperiment(ExperimentAbstract[Pipeline]):
    def __init__(
        self, experiment_name: str, workspace: Workspace, steps: list = None
    ) -> None:
        """
        Initialize Pipeline.

        :param experiment_name: The name of the experiment
        :type experiment_name: str
        :param workspace: The workspace to submit the Pipeline on.
        :type workspace: azureml.core.workspace.Workspace
        :param steps: The list of steps to execute as part of a Pipeline.
        :type steps: builtin.list
        """
        self.__steps = steps or []
        super().__init__(experiment_name, workspace)

    def get_config(self) -> Pipeline:
        return Pipeline(self.workspace, self.__steps)

    def append_step(self, step):
        self.__steps.append(step)
