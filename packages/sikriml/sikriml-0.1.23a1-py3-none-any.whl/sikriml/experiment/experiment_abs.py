from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from azureml.core import Experiment, Run
from azureml.core.workspace import Workspace

T = TypeVar("T")


class ExperimentAbstract(Generic[T], ABC):
    def __init__(self, experiment_name: str, workspace: Workspace) -> None:
        self.experiment_name = experiment_name
        self.workspace = workspace

    def get_experiment(self) -> Experiment:
        return Experiment(self.workspace, self.experiment_name)

    @abstractmethod
    def get_config(self) -> T:
        pass

    def run(self) -> Run:
        experiment = self.get_experiment()
        run: Run = experiment.submit(config=self.get_config())
        run.wait_for_completion(show_output=True)
        return run
