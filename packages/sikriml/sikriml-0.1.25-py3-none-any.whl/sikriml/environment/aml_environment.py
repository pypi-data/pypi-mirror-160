from time import sleep
from typing import List

from azureml.core import Workspace
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.environment import Environment
from sikriml.environment.errors import AMLBuildImageError

FAILED_STATUS = ["Failed"]


class AmlEnvironment:
    def __init__(
        self,
        ws: Workspace,
        aml_env_name: str,
        python_version: str = "3.8.10",
        base_image: str = "mcr.microsoft.com/azureml/minimal-ubuntu20.04-py38-cpu-inference:latest",
    ) -> None:
        self.__workspace = ws
        self.__aml_env = Environment(name=aml_env_name)
        self.__conda_dep = CondaDependencies()
        self.__conda_dep.set_python_version(python_version)
        self.__aml_env.docker.base_image = base_image

    # getter method
    def get_base_image(self):
        return self.__aml_env.docker.base_image

    # setter method
    def set_base_image(self, base_image):
        self.__aml_env.docker.base_image = base_image

    def add_pip_packages(self, pip_packages: List[str]):
        for pip_package in pip_packages:
            self.__conda_dep.add_pip_package(pip_package)

    def add_conda_packages(self, conda_packages: List[str]):
        for conda_package in conda_packages:
            self.__conda_dep.add_conda_package(conda_package)

    def set_pip_option(self, pip_option):
        self.__conda_dep.set_pip_option(pip_option)

    def __wait_for_succeeded_build(self, build, timeout):
        waited_sec = 0
        completed = False
        while waited_sec < (timeout * 60) and not completed:
            status = build.status
            waited_sec += 5
            if status in FAILED_STATUS:
                raise AMLBuildImageError("Build of image failed with status", status)
            if status == "Succeeded":
                completed = True
            print("The build image has status :", status)
            sleep(5)
        if completed:
            print("Build status", status)
            return True
        raise AMLBuildImageError("Build of image Timed out")

    def register_and_build(self, timeout: int = 10):
        # Create and register environment
        self.__aml_env.python.conda_dependencies = self.__conda_dep
        self.__aml_env.docker.enabled = True
        self.__aml_env.register(self.__workspace)
        build = self.__aml_env.build(self.__workspace)
        build.wait_for_completion(build)
        self.__wait_for_succeeded_build(build, timeout)
        print("Build succeded")
