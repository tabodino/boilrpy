import subprocess
from boilrpy.dependency_creators.base_dependency_creator import (
    BaseDependencyCreator,
    DependencyCreatorNotFoundError,
    DependencyCreatorError,
)


class PipCreator(BaseDependencyCreator):
    """Class to create a new pip project."""

    def create_dependency_file(self, project_info: dict) -> None:
        """Create a new pip project with requirements.txt.

        Args:
            project_info (dict): Dictionary containing project information
        """
        try:
            packages, dev_packages = self._create_packages(project_info)

            # Create requirements.txt files using base class method
            self._write_requirements_files(packages, dev_packages)

            # Note: We don't auto-install with pip to let user create venv first
            print("\nTo install dependencies:")
            print("1. Create a virtual environment:")
            print("   python -m venv venv")
            print("2. Activate it:")
            print("   source venv/bin/activate  # Linux/macOS")
            print("   venv\\Scripts\\activate     # Windows")
            print("3. Install dependencies:")
            print("   pip install -r requirements.txt")
            if dev_packages:
                print("   pip install -r requirements-dev.txt")

        except Exception as e:
            raise DependencyCreatorError(f"pip initialization failed: {e}") from e

    def install_dependencies(self, packages: list, dev_packages: list) -> None:
        """Install dependencies using pip.

        Note: This assumes pip is available and venv is activated.

        Args:
            packages (list): List of regular packages
            dev_packages (list): List of development packages
        """
        try:
            all_packages = packages + dev_packages
            if all_packages:
                subprocess.run(["pip", "install"] + all_packages, check=True)
        except subprocess.CalledProcessError as e:
            raise DependencyCreatorError(f"Failed to install dependencies: {e}") from e
        except FileNotFoundError as exc:
            raise DependencyCreatorNotFoundError(
                "pip not found. Please ensure Python and pip are installed."
            ) from exc
