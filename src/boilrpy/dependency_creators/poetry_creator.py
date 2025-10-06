import subprocess
import toml
from boilrpy.dependency_creators.base_dependency_creator import (
    BaseDependencyCreator,
    DependencyCreatorNotFoundError,
    DependencyCreatorError,
)


class PoetryCreator(BaseDependencyCreator):
    """Class to create a new poetry project."""

    def create_dependency_file(self, project_info: dict) -> None:
        """Create a new poetry file.

        Args:
            project_info (dict): Dictionary containing project information
        """
        try:
            packages, dev_packages = self._create_packages(project_info)
            subprocess.run(["poetry", "init", "-n"], check=True)
            self._update_pyproject_toml(project_info)
            self.install_dependencies(packages, dev_packages)
        except FileNotFoundError as exc:
            raise DependencyCreatorNotFoundError(
                "Poetry not found. Please install Poetry and try again."
            ) from exc
        except subprocess.CalledProcessError as e:
            raise DependencyCreatorError(f"Poetry initialization failed: {e}") from e

    def install_dependencies(self, packages: list, dev_packages: list) -> None:
        """Install dependencies using Poetry.

        Args:
            packages (list): List of regular packages
            dev_packages (list): List of development packages
        """
        try:
            if dev_packages:
                subprocess.run(
                    ["poetry", "add", "--group", "dev"] + dev_packages, check=True
                )
            if packages:
                subprocess.run(["poetry", "add"] + packages, check=True)
        except subprocess.CalledProcessError as e:
            raise DependencyCreatorError(f"Failed to install dependencies: {e}") from e

    def _update_pyproject_toml(self, project_info):
        """Update pyproject.toml with project information."""
        pyproject_file = "pyproject.toml"

        with open(pyproject_file, "r", encoding=self.charset) as file:
            pyproject_data = toml.load(file)

        poetry_version = self._check_poetry_version()

        if poetry_version.startswith("1."):
            pyproject_data["tool"]["poetry"]["name"] = project_info["name"]
            pyproject_data["tool"]["poetry"]["version"] = project_info["version"]
            pyproject_data["tool"]["poetry"]["description"] = project_info[
                "description"
            ]
            pyproject_data["tool"]["poetry"]["authors"] = [project_info["author"]]
            pyproject_data["tool"]["poetry"]["license"] = project_info["license"]

        if poetry_version.startswith("2."):
            pyproject_data["project"]["name"] = project_info["name"]
            pyproject_data["project"]["version"] = project_info["version"]
            pyproject_data["project"]["description"] = project_info["description"]
            if project_info["author"]:
                pyproject_data["project"]["authors"] = [
                    {"name": project_info["author"]}
                ]
            pyproject_data["project"]["license"] = {"text": project_info["license"]}

        with open(pyproject_file, "w", encoding=self.charset) as file:
            toml.dump(pyproject_data, file)

    def _check_poetry_version(self):
        """Check Poetry version."""
        result = subprocess.run(
            ["poetry", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        version_output = result.stdout.strip()
        return version_output.split()[-1]
