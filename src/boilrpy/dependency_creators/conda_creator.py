import subprocess
from boilrpy.dependency_creators.base_dependency_creator import (
    BaseDependencyCreator,
    DependencyCreatorNotFoundError,
    DependencyCreatorError,
)


class CondaCreator(BaseDependencyCreator):
    """Class to create a new conda project."""

    def create_dependency_file(self, project_info: dict) -> None:
        """Create a new conda project with environment.yml.

        Args:
            project_info (dict): Dictionary containing project information
        """
        try:
            packages, dev_packages = self._create_packages(project_info)

            # Create environment.yml
            self._create_environment_file(project_info, packages, dev_packages)

            print("\nTo create and activate the conda environment:")
            print("1. conda env create -f environment.yml")
            print(f"2. conda activate {project_info['name']}")

        except Exception as e:
            raise DependencyCreatorError(f"conda initialization failed: {e}") from e

    def install_dependencies(self, packages: list, dev_packages: list) -> None:
        """Install dependencies using conda.

        Args:
            packages (list): List of regular packages
            dev_packages (list): List of development packages
        """
        try:
            all_packages = packages + dev_packages
            if all_packages:
                subprocess.run(["conda", "install", "-y"] + all_packages, check=True)
        except subprocess.CalledProcessError as e:
            raise DependencyCreatorError(f"Failed to install dependencies: {e}") from e
        except FileNotFoundError as exc:
            raise DependencyCreatorNotFoundError(
                "conda not found. Please install Anaconda or Miniconda."
            ) from exc

    def _create_environment_file(
        self, project_info: dict, packages: list, dev_packages: list
    ) -> None:
        """Create environment.yml file.

        Args:
            project_info (dict): Dictionary containing project information
            packages (list): List of regular packages
            dev_packages (list): List of development packages
        """
        all_packages = packages + dev_packages

        environment_content = f"""name: {project_info["name"]}
channels:
  - conda-forge
  - defaults
dependencies:
  - python={project_info.get("python_version", "3.11")}
"""

        if all_packages:
            for package in all_packages:
                environment_content += f"  - {package}\n"

        environment_content += """
  - pip
  - pip:
    # Add pip-only packages here
"""

        with open("environment.yml", "w", encoding=self.charset) as f:
            f.write(environment_content)
