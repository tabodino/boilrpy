import os
import subprocess
import toml
from boilrpy.config import Config
from boilrpy.file_generator import FileGenerator
from boilrpy.file_writer import FileWriter
from boilrpy.utils.string_formatter import StringFormatter


class ProjectCreator:
    """
    Class to create a new project.
    """
    def __init__(self, config: Config):
        self.project_name = None
        self.config = config
        self.charset = config.get_charset()
        self.file_generator = FileGenerator(config)
        self.file_writer = FileWriter(self.charset)

    def create_project(self, project_info: dict) -> None:
        """
        Create a new project.

        Args:
            project_info (dict): Dictionary containing project information
        
        Returns:
            None
        """
        self.project_name = StringFormatter.format_project_name(
            project_info["name"],
            self.config.use_camel_case)

        project_info["version"] = project_info.get(
            "version") or "0.1.0"

        if self._check_directory_exist(self.project_name):
            raise FileExistsError(
                f"Directory {self.project_name} already exists.")

        print(f"Creating project {self.project_name}...")
        project_path = self._create_project_directory()
        os.chdir(project_path)

        self._create_readme(project_info)

        self._create_license(project_info)

        self._create_gitignore()

        self._create_changelog(project_info["version"])

        self._create_poetry_file(project_info)

        self._create_dockerfile(project_info)

        self._create_test_folder(project_info["create_tests"])

        self._create_main_file()

        self._create_empty_requirements_txt()

        self._create_linter_file(project_info["use_pylint"])

        self._initialize_git_repository()


    def _create_project_directory(self) -> str:
        """
        Create a new project directory.

        Returns:
            str: The path to the new project directory.
        """
        project_path = os.path.join(os.getcwd(), self.project_name)
        self.file_writer.create_directory(project_path, exist_ok=False)
        return project_path

    def _create_readme(self, project_info: dict) -> None:
        """
        Create a new README.md file.

        Args:
            project_info (dict): Dictionary containing project information
        
        Returns:
            None
        """
        content = self.file_generator.generate_readme(project_info)
        self.file_writer.write_file("README.md", content)

    def _create_license(self, project_info: dict) -> None:
        if project_info["license"] == "None":
            return
        content = self.file_generator.generate_license(
            project_info["license"], project_info["author"])
        self.file_writer.write_file("LICENSE", content)

    def _create_gitignore(self) -> None:
        content = self.file_generator.generate_gitignore()
        self.file_writer.write_file(".gitignore", content)

    def _create_changelog(self, version: str) -> None:
        content = self.file_generator.generate_changelog(version)
        self.file_writer.write_file("CHANGELOG.md", content)

    def _create_poetry_file(self, project_info: dict) -> None:
        if not project_info["use_poetry"]:
            return
        try:
            subprocess.run(["poetry", "init", "-n"], check=True)
            self._update_pyproject_toml(project_info)
            dev_packages = ["pytest"] if project_info["create_tests"] else []
            if project_info["use_pylint"]:
                dev_packages.append("pylint")
            if dev_packages:
                subprocess.run(["poetry", "add", "--group",
                            "dev"] + dev_packages, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Poetry initialization failed : {e}")

    def _update_pyproject_toml(self, project_info):
        pyproject_file = "pyproject.toml"

        with open(pyproject_file, "r", encoding=self.charset) as file:
            pyproject_data = toml.load(file)

        pyproject_data["tool"]["poetry"]["name"] = project_info["name"]
        pyproject_data["tool"]["poetry"]["version"] = project_info["version"]
        pyproject_data["tool"]["poetry"]["description"] =\
            project_info["description"]
        pyproject_data["tool"]["poetry"]["authors"] = [project_info["author"]]
        pyproject_data["tool"]["poetry"]["license"] = project_info["license"]

        with open(pyproject_file, "w", encoding=self.charset) as file:
            toml.dump(pyproject_data, file)

    def _create_dockerfile(self, project_info: dict) -> None:
        if not project_info["use_docker"]:
            return
        content = self.file_generator.generate_dockerfile(self.project_name)
        self.file_writer.write_file("Dockerfile", content)
        ignore_content = self.file_generator.generate_dockerignore()
        self.file_writer.write_file(".dockerignore", ignore_content)

    def _create_test_folder(self, create_tests: bool) -> None:
        if not create_tests:
            return
        self.file_writer.create_directory("tests")
        self.file_writer.write_file("tests/__init__.py", "")

    def _create_main_file(self) -> None:
        content = self.file_generator.generate_main_file()
        self.file_writer.write_file("main.py", content)

    def _create_empty_requirements_txt(self) -> None:
        self.file_writer.write_file("requirements.txt", '')

    def _create_linter_file(self, use_pylint: bool) -> None:
        if not use_pylint:
            return
        content = self.file_generator.generate_pylint()
        self.file_writer.write_file(".pylintrc", content)

    def _initialize_git_repository(self) -> None:
        git_dir = os.path.join(os.getcwd(), ".git")
        self.file_writer.create_directory(git_dir)
        os.chmod(git_dir, 0o775)
        os.system("git init")

    def _check_directory_exist(self, directory: str) -> bool:
        return os.path.exists(directory) and os.path.isdir(directory)
