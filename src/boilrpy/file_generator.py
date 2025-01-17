from boilrpy.file_generators.changelog_generator import ChangelogGenerator
from boilrpy.file_generators.dockerfile_generator import DockerfileGenerator
from boilrpy.file_generators.gitignore_generator import GitignoreGenerator
from boilrpy.file_generators.license_generator import LicenseGenerator
from boilrpy.file_generators.main_file_generator import MainFileGenerator
from boilrpy.file_generators.readme_generator import ReadmeGenerator


class FileGenerator:
    """
    Main class for generating project files.
    """

    def __init__(self, config):
        self.config = config
        self.readme_generator = ReadmeGenerator(config)
        self.license_generator = LicenseGenerator(config)
        self.gitignore_generator = GitignoreGenerator(config)
        self.changelog_generator = ChangelogGenerator(config)
        self.main_file_generator = MainFileGenerator(config)
        self.dockerfile_generator = DockerfileGenerator(config)

    def generate_readme(self, project_info: dict) -> str:
        """
        Generate README.md content.

        :param project_info: Dictionary containing project information
        :return: Content of README.md file
        """
        return self.readme_generator.generate(project_info)

    def generate_license(self, license_name: str, author: str) -> str:
        """
        Generate license file content.

        :param license_name: Name of the license
        :param author: Name of the author
        :return: Content of the license file
        """
        return self.license_generator.generate(license_name, author)

    def generate_gitignore(self) -> str:
        """
        Generate .gitignore file content.

        :return: Content of .gitignore file
        """
        return self.gitignore_generator.generate()

    def generate_changelog(self, version: str) -> str:
        """
        Generate CHANGELOG.md content.

        :param version: Version number
        :return: Content of CHANGELOG.md file
        """
        return self.changelog_generator.generate(version)

    def generate_main_file(self) -> str:
        """
        Generate main.py content.

        :return: Content of main.py file
        """
        return self.main_file_generator.generate()

    def generate_dockerfile(self, project_name: str) -> str:
        """
        Generate Dockerfile content.

        :return: Content of Dockerfile
        """
        return self.dockerfile_generator.generate_dockerfile(project_name)

    def generate_dockerignore(self) -> str:
        """
        Generate .dockerignore content.

        :return: Content of .dockerignore
        """
        return self.dockerfile_generator.generate_dockerignore()
