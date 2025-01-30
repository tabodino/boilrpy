import pytest
from unittest.mock import Mock, patch
from boilrpy.config import Config
from boilrpy.flask_app_creator import FlaskAppCreator
from boilrpy.file_generator import FileGenerator
from boilrpy.file_writer import FileWriter


@pytest.fixture
def mock_config():
    return Mock(spec=Config)


@pytest.fixture
def mock_file_generator():
    return Mock(spec=FileGenerator)


@pytest.fixture
def mock_file_writer():
    return Mock(spec=FileWriter)


@pytest.fixture
def flask_app_creator(mock_config, mock_file_generator, mock_file_writer):
    with patch(
        "boilrpy.flask_app_creator.FileGenerator", return_value=mock_file_generator
    ), patch("boilrpy.flask_app_creator.FileWriter", return_value=mock_file_writer):
        return FlaskAppCreator(mock_config)


def test_create_flask_project(flask_app_creator):
    project_info = {"name": "Test Project", "description": "A test Flask project"}
    flask_app_creator.create_flask_project(project_info)

    assert flask_app_creator.file_writer.create_directory.call_count == 3
    flask_app_creator.file_writer.create_directory.assert_any_call("templates")
    flask_app_creator.file_writer.create_directory.assert_any_call("static/css")
    flask_app_creator.file_writer.create_directory.assert_any_call("static/js")

    assert flask_app_creator.file_writer.write_file.call_count == 6
    flask_app_creator.file_writer.write_file.assert_any_call(
        "app.py", flask_app_creator.file_generator.generate_flask_app_file()
    )
    flask_app_creator.file_writer.write_file.assert_any_call(
        ".env", flask_app_creator.file_generator.generate_dot_env_file()
    )
    flask_app_creator.file_writer.write_file.assert_any_call(
        "templates/base.html",
        flask_app_creator.file_generator.generate_base_template(project_info),
    )
    flask_app_creator.file_writer.write_file.assert_any_call(
        "templates/index.html",
        flask_app_creator.file_generator.generate_index_template(project_info),
    )
    flask_app_creator.file_writer.write_file.assert_any_call(
        "static/css/style.css", flask_app_creator.file_generator.generate_style_file()
    )
    flask_app_creator.file_writer.write_file.assert_any_call(
        "static/js/script.js", flask_app_creator.file_generator.generate_script_file()
    )


def test_create_flask_folders(flask_app_creator):
    flask_app_creator._create_flask_folders()
    flask_app_creator.file_writer.create_directory.assert_any_call("templates")
    flask_app_creator.file_writer.create_directory.assert_any_call("static/css")
    flask_app_creator.file_writer.create_directory.assert_any_call("static/js")


def test_create_flask_app_file(flask_app_creator):
    flask_app_creator._create_flask_app_file()
    flask_app_creator.file_writer.write_file.assert_called_once_with(
        "app.py", flask_app_creator.file_generator.generate_flask_app_file()
    )


def test_create_flask_dot_env(flask_app_creator):
    flask_app_creator._create_flask_dot_env()
    flask_app_creator.file_writer.write_file.assert_called_once_with(
        ".env", flask_app_creator.file_generator.generate_dot_env_file()
    )


def test_create_flask_template_files(flask_app_creator):
    project_info = {"name": "Test Project", "description": "A test Flask project"}
    flask_app_creator._create_flask_template_files(project_info)
    flask_app_creator.file_writer.write_file.assert_any_call(
        "templates/base.html",
        flask_app_creator.file_generator.generate_base_template(project_info),
    )
    flask_app_creator.file_writer.write_file.assert_any_call(
        "templates/index.html",
        flask_app_creator.file_generator.generate_index_template(project_info),
    )


def test_create_flask_static_files(flask_app_creator):
    flask_app_creator._create_flask_static_files()
    flask_app_creator.file_writer.write_file.assert_any_call(
        "static/css/style.css", flask_app_creator.file_generator.generate_style_file()
    )
    flask_app_creator.file_writer.write_file.assert_any_call(
        "static/js/script.js", flask_app_creator.file_generator.generate_script_file()
    )
