from abc import ABC, abstractmethod
from boilrpy.config import Config


class BaseDependencyCreator(ABC):
    """Base class for dependency managers creators."""

    def __init__(self, config: Config):
        self.config = config
        self.charset = self.config.get_charset()

    @abstractmethod
    def create_dependency_file(self, project_info: dict) -> None:
        """Create dependency configuration file.

        Args:
            project_info (dict): Dictionary containing project information
        """
        raise NotImplementedError("Subclasses must implement create_dependency_file")

    @abstractmethod
    def install_dependencies(self, packages: list, dev_packages: list) -> None:
        """Install dependencies.

        Args:
            packages (list): List of regular packages
            dev_packages (list): List of development packages
        """
        raise NotImplementedError("Subclasses must implement create_dependency_file")

    def _create_packages(self, project_info: dict) -> tuple[list, list]:
        """Create lists of packages and dev packages.

        Args:
            project_info (dict): Dictionary containing project information

        Returns:
            tuple: (packages, dev_packages)
        """
        dev_packages = ["pytest"] if project_info.get("create_tests") else []
        if project_info.get("use_pylint"):
            dev_packages.append("pylint")

        packages = []
        if project_info.get("use_flask"):
            packages.append("flask")
            packages.append("python-dotenv")

        # Add additional libraries
        additional_libs = project_info.get("libraries", [])
        if additional_libs:
            packages.extend(additional_libs)

        return packages, dev_packages

    def _write_requirements_files(
        self,
        packages: list,
        dev_packages: list,
        create_empty_if_no_packages: bool = True,
    ) -> None:
        """Write requirements.txt and requirements-dev.txt files.

        This is a common implementation used by pip-like dependency managers.

        Args:
            packages (list): List of regular packages
            dev_packages (list): List of development packages
            create_empty_if_no_packages (bool): Whether to create an empty
                requirements.txt if no packages are specified
        """
        # Create requirements.txt
        if packages:
            with open("requirements.txt", "w", encoding=self.charset) as f:
                for package in packages:
                    f.write(f"{package}\n")
        elif create_empty_if_no_packages:
            # Create empty requirements.txt with comment
            with open("requirements.txt", "w", encoding=self.charset) as f:
                f.write("# Add your dependencies here\n")

        # Create requirements-dev.txt
        if dev_packages:
            with open("requirements-dev.txt", "w", encoding=self.charset) as f:
                f.write("-r requirements.txt\n")
                for package in dev_packages:
                    f.write(f"{package}\n")


class DependencyCreatorNotFoundError(Exception):
    """Exception raised when dependency manager is not found."""


class DependencyCreatorError(Exception):
    """Exception raised when dependency manager operation fails."""
