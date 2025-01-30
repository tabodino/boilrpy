import subprocess
import toml
from boilrpy.config import Config


class PoetryCreator:
    """Class to create a new poetry project."""
    def __init__(self, config: Config):
        self.config = config
        self.charset = self.config.get_charset()

    def create_poetry_file(self, project_info: dict) -> None:
        """Create a new poetry file.

        Args:
            project_info (dict): Dictionary containing project information
        """
        if not project_info["use_poetry"]:
            return
        try:
            packages, dev_packages = self._create_packages(project_info)
            subprocess.run(["poetry", "init", "-n"], check=True)
            self._update_pyproject_toml(project_info)
            if dev_packages:
                subprocess.run(
                    ["poetry", "add", "--group", "dev"] + dev_packages, check=True
                )
            if packages:
                subprocess.run(["poetry", "add"] + packages, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Poetry initialization failed : {e}")

    def _update_pyproject_toml(self, project_info):
        pyproject_file = "pyproject.toml"

        with open(pyproject_file, "r", encoding=self.charset) as file:
            pyproject_data = toml.load(file)

        pyproject_data["tool"]["poetry"]["name"] = project_info["name"]
        pyproject_data["tool"]["poetry"]["version"] = project_info["version"]
        pyproject_data["tool"]["poetry"]["description"] = project_info["description"]
        pyproject_data["tool"]["poetry"]["authors"] = [project_info["author"]]
        pyproject_data["tool"]["poetry"]["license"] = project_info["license"]

        with open(pyproject_file, "w", encoding=self.charset) as file:
            toml.dump(pyproject_data, file)

    def _create_packages(self, project_info: dict) -> list:
        dev_packages = ["pytest"] if project_info["create_tests"] else []
        if project_info["use_pylint"]:
            dev_packages.append("pylint")

        packages = []
        if project_info["use_flask"]:
            packages.append("flask")
            packages.append("python-dotenv")

        return packages, dev_packages
