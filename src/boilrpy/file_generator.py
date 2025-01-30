from abc import ABC, abstractmethod
from typing import Any, Dict, Type
from boilrpy.file_generators.changelog_generator import ChangelogGenerator
from boilrpy.file_generators.dockerfile_generator import DockerfileGenerator
from boilrpy.file_generators.gitignore_generator import GitignoreGenerator
from boilrpy.file_generators.license_generator import LicenseGenerator
from boilrpy.file_generators.main_file_generator import MainFileGenerator
from boilrpy.file_generators.readme_generator import ReadmeGenerator
from boilrpy.file_generators.pylint_generator import PylintGenerator
from boilrpy.file_generators.flask_generator import FlaskGenerator
from boilrpy.file_generators.requirements_generator import RequirementsGenerator
from boilrpy.config import Config


class Generator(ABC):
    """
    Abstract class for generating project files.
    """

    @abstractmethod
    def generate(self, *args, **kwargs) -> str:
        """Generate the content of the file."""


class GeneratorFactory:
    """
    Factory class for creating generators.
    """

    _generators: Dict[str, Type[Generator]] = {
        "readme": ReadmeGenerator,
        "license": LicenseGenerator,
        "gitignore": GitignoreGenerator,
        "changelog": ChangelogGenerator,
        "main_file": MainFileGenerator,
        "dockerfile": DockerfileGenerator,
        "pylint": PylintGenerator,
        "flask": FlaskGenerator,
        "requirements": RequirementsGenerator,
    }

    @classmethod
    def create_generator(cls, generator_type: str, config: Dict[str, Any]) -> Generator:
        """
        Create a generator instance.

        Args:
            generator_type (str): The type of generator to create.
            config (Dict[str, Any]): The configuration dictionary.

        Returns:
            Generator: The created generator instance.

        Raises:
            ValueError: If the generator type is unknown.
        """
        generator_class = cls._generators.get(generator_type)
        if generator_class is None:
            raise ValueError(f"Unknown generator type: {generator_type}")
        return generator_class(config)


class FileGenerator:
    """
    Main class for generating project files.
    """

    def __init__(self, config: Config):
        self.config = config
        self.generators: Dict[str, Generator] = {}

    def _get_generator(self, generator_type: str) -> Generator:
        if generator_type not in self.generators:
            self.generators[generator_type] = GeneratorFactory.create_generator(
                generator_type, self.config
            )
        return self.generators[generator_type]

    def generate_readme(self, project_info: dict) -> str:
        """
        Generate README.md content.

        :param project_info: Dictionary containing project information
        :return: Content of README.md file
        """
        return self._get_generator("readme").generate(project_info)

    def generate_license(self, license_name: str, author: str) -> str:
        """
        Generate license file content.

        :param license_name: Name of the license
        :param author: Name of the author
        :return: Content of the license file
        """
        return self._get_generator("license").generate(license_name, author)

    def generate_gitignore(self) -> str:
        """
        Generate .gitignore file content.

        :return: Content of .gitignore file
        """
        return self._get_generator("gitignore").generate()

    def generate_changelog(self, version: str) -> str:
        """
        Generate CHANGELOG.md content.

        :param version: Version number
        :return: Content of CHANGELOG.md file
        """
        return self._get_generator("changelog").generate(version)

    def generate_main_file(self) -> str:
        """
        Generate main.py content.

        :return: Content of main.py file
        """
        return self._get_generator("main_file").generate()

    def generate_dockerfile(self, project_name: str, use_flask: bool) -> str:
        """
        Generate Dockerfile content.

        :return: Content of Dockerfile
        """
        return self._get_generator("dockerfile").generate_dockerfile(
            project_name, use_flask
        )

    def generate_dockerignore(self) -> str:
        """
        Generate .dockerignore content.

        :return: Content of .dockerignore
        """
        return self._get_generator("dockerfile").generate_dockerignore()

    def generate_pylint(self) -> str:
        """
        Generate .pylintrc content.

        :return: Content of .pylintrc
        """
        return self._get_generator("pylint").generate()

    def generate_requirements_txt(self, project_info: dict) -> str:
        """
        Generate requirements.txt content.

        :return: Content of requirements.txt
        """
        return self._get_generator("requirements").generate(project_info)

    def generate_flask_app_file(self) -> str:
        """
        Generate flask app file content.

        :return: Content of flask app file
        """
        return self._get_generator("flask").generate_app_file()

    def generate_base_template(self, project_info: dict) -> str:
        """
        Generate base template content.

        :return: Content of base template
        """
        return self._get_generator("flask").generate_base_template(project_info)

    def generate_index_template(self, project_info: dict) -> str:
        """
        Generate index template content.

        :return: Content of index template
        """
        return self._get_generator("flask").generate_index_template(project_info)

    def generate_dot_env_file(self) -> str:
        """
        Generate .env file content.

        :return: Content of .env file
        """
        return self._get_generator("flask").generate_dot_env_file()

    def generate_style_file(self) -> str:
        """
        Generate style file content.

        :return: Content of style file
        """
        return self._get_generator("flask").generate_style_file()

    def generate_script_file(self) -> str:
        """
        Generate script file content.

        :return: Content of script file
        """
        return self._get_generator("flask").generate_script_file()
