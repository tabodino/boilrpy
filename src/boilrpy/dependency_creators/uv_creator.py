import subprocess
from boilrpy.dependency_creators.base_dependency_creator import (
    BaseDependencyCreator,
    DependencyCreatorNotFoundError,
    DependencyCreatorError,
)


class UvCreator(BaseDependencyCreator):
    """Class to create a new uv project."""

    def create_dependency_file(self, project_info: dict) -> None:
        """Create a new uv project with requirements.txt.

        Args:
            project_info (dict): Dictionary containing project information
        """
        try:
            # Check if uv is installed first
            subprocess.run(["uv", "--version"], check=True, capture_output=True)
        except FileNotFoundError as exc:
            raise DependencyCreatorNotFoundError(
                "uv not found. Please install uv and try again.\n"
                "Installation options:\n"
                "  - Using pip: pip install uv\n"
                "  - Using pipx: pipx install uv\n"
                "  - Using cargo: cargo install --git https://github.com/astral-sh/uv uv\n"
                "  - Download from: https://github.com/astral-sh/uv/releases"
            ) from exc
        except subprocess.CalledProcessError as exc:
            raise DependencyCreatorNotFoundError(
                "uv not found or not working properly. Please install uv and try again.\n"
                "Installation options:\n"
                "  - Using pip: pip install uv\n"
                "  - Using pipx: pipx install uv\n"
                "  - Using cargo: cargo install --git https://github.com/astral-sh/uv uv\n"
                "  - Download from: https://github.com/astral-sh/uv/releases"
            ) from exc

        try:
            packages, dev_packages = self._create_packages(project_info)

            # Create virtual environment with uv
            subprocess.run(["uv", "venv"], check=True)

            # Create requirements.txt using base class method
            self._write_requirements_files(
                packages, dev_packages, create_empty_if_no_packages=False
            )

            # Install dependencies
            self.install_dependencies(packages, dev_packages)

        except subprocess.CalledProcessError as e:
            raise DependencyCreatorError(f"uv initialization failed: {e}") from e

    def install_dependencies(self, packages: list, dev_packages: list) -> None:
        """Install dependencies using uv.

        Args:
            packages (list): List of regular packages
            dev_packages (list): List of development packages
        """
        try:
            all_packages = packages + dev_packages
            if all_packages:
                subprocess.run(["uv", "pip", "install"] + all_packages, check=True)
        except subprocess.CalledProcessError as e:
            raise DependencyCreatorError(f"Failed to install dependencies: {e}") from e
