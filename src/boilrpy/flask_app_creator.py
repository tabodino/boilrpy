from boilrpy.config import Config
from boilrpy.file_generator import FileGenerator
from boilrpy.file_writer import FileWriter


class FlaskAppCreator:
    """Class to create a new Flask app."""

    def __init__(self, config: Config):
        self.config = config
        self.file_generator = FileGenerator(config)
        self.file_writer = FileWriter(self.config.get_charset())

    def create_flask_project(self, project_info: dict) -> None:
        """Create a new Flask app.

        Args:
            project_info (dict): Dictionary containing project information
        """
        self._create_flask_folders()
        self._create_flask_app_file()
        self._create_flask_dot_env()
        self._create_flask_template_files(project_info)
        self._create_flask_static_files()

    def _create_flask_folders(self) -> None:
        self.file_writer.create_directory("templates")
        self.file_writer.create_directory("static/css")
        self.file_writer.create_directory("static/js")

    def _create_flask_app_file(self) -> None:
        content = self.file_generator.generate_flask_app_file()
        self.file_writer.write_file("app.py", content)

    def _create_flask_dot_env(self) -> None:
        content = self.file_generator.generate_dot_env_file()
        self.file_writer.write_file(".env", content)

    def _create_flask_template_files(self, project_info: dict) -> None:
        base_content = self.file_generator.generate_base_template(project_info)
        self.file_writer.write_file("templates/base.html", base_content)
        index_content = self.file_generator.generate_index_template(project_info)
        self.file_writer.write_file("templates/index.html", index_content)

    def _create_flask_static_files(self) -> None:
        css_content = self.file_generator.generate_style_file()
        self.file_writer.write_file("static/css/style.css", css_content)
        js_content = self.file_generator.generate_script_file()
        self.file_writer.write_file("static/js/script.js", js_content)
