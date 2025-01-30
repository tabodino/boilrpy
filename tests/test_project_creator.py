import os
import pytest
from unittest.mock import Mock, patch, mock_open
from boilrpy.project_creator import ProjectCreator
from boilrpy.config import Config
from boilrpy.file_generator import FileGenerator
from boilrpy.file_writer import FileWriter, FileWriterError
from boilrpy.poetry_creator import PoetryCreator


@pytest.fixture
def mock_config():
    config = Mock(spec=Config)
    config.get_charset.return_value = "utf-8"
    config.use_camel_case = False
    config.python_version = "3.11"
    return config


@pytest.fixture
def mock_file_generator():
    return Mock(spec=FileGenerator)


@pytest.fixture
def poetry_creator(mock_config):
    return PoetryCreator(mock_config)


@pytest.fixture
def mock_file_writer():
    return Mock(spec=FileWriter)


@pytest.fixture
def project_creator(mock_config, mock_file_generator, poetry_creator):
    with patch(
        "boilrpy.project_creator.FileGenerator", return_value=mock_file_generator
    ), patch("boilrpy.project_creator.PoetryCreator", return_value=poetry_creator):
        return ProjectCreator(mock_config)


@pytest.fixture
def project_info():
    return {
        "name": "test_project",
        "version": "0.1.0",
        "description": "A test project",
        "author": "Test Author",
        "license": "MIT",
        "use_poetry": True,
        "use_docker": True,
        "create_tests": True,
        "use_pylint": True,
        "use_flask": True,
    }


@patch("boilrpy.project_creator.StringFormatter.format_project_name")
@patch("boilrpy.project_creator.os.chdir")
def test_create_project_success(
    mock_chdir, mock_format_project_name, project_creator, project_info
):
    mock_format_project_name.return_value = "test_project"

    with patch.object(
        project_creator, "_check_directory_exist", return_value=False
    ) as mock_check_dir, patch.object(
        project_creator, "_create_project_directory", return_value="/path/to/project"
    ) as mock_create_dir, patch.object(
        project_creator, "_create_readme"
    ) as mock_create_readme, patch.object(
        project_creator, "_create_license"
    ) as mock_create_license, patch.object(
        project_creator, "_create_gitignore"
    ) as mock_create_gitignore, patch.object(
        project_creator, "_create_changelog"
    ) as mock_create_changelog, patch.object(
        project_creator, "_create_poetry_file"
    ) as mock_create_poetry, patch.object(
        project_creator, "_create_dockerfile"
    ) as mock_create_dockerfile, patch.object(
        project_creator, "_create_linter_file"
    ) as mock_create_pylint, patch.object(
        project_creator, "_create_test_folder"
    ) as mock_create_test, patch.object(
        project_creator, "_create_flask_app"
    ) as mock_create_flask, patch.object(
        project_creator, "_create_main_file"
    ) as mock_create_requirements, patch.object(
        project_creator, "_create_requirements_txt"
    ) as mock_create_main, patch.object(
        project_creator, "_initialize_git_repository"
    ) as mock_init_git:

        project_creator.create_project(project_info)

    mock_format_project_name.assert_called_once_with("test_project", False)
    mock_chdir.assert_called_once_with("/path/to/project")
    mock_check_dir.assert_called_once_with("test_project")
    mock_create_dir.assert_called_once()
    mock_create_readme.assert_called_once_with(project_info)
    mock_create_license.assert_called_once_with(project_info)
    mock_create_gitignore.assert_called_once()
    mock_create_changelog.assert_called_once_with("0.1.0")
    mock_create_poetry.assert_called_once_with(project_info)
    mock_create_dockerfile.assert_called_once_with(project_info)
    mock_create_pylint.assert_called_once_with(project_info["use_pylint"])
    mock_create_test.assert_called_once_with(project_info["create_tests"])
    mock_create_flask.assert_called_once_with(project_info)
    mock_create_requirements.assert_called_once_with(project_info["use_flask"])
    mock_init_git.assert_called_once()


def test_create_project_directory_exists(project_creator, project_info):
    with patch.object(
        project_creator, "_check_directory_exist", return_value=True
    ), patch(
        "boilrpy.project_creator.StringFormatter.format_project_name",
        return_value="test_project",
    ):
        with pytest.raises(
            FileExistsError, match="Directory test_project already exists."
        ):
            project_creator.create_project(project_info)


def test_create_project_no_version(project_creator, project_info):
    project_info.pop("version")
    with patch.object(
        project_creator, "_check_directory_exist", return_value=False
    ), patch.object(project_creator, "_create_project_directory"), patch.object(
        project_creator, "_create_changelog"
    ) as mock_create_changelog, patch.object(
        project_creator, "_create_readme"
    ), patch.object(
        project_creator, "_create_license"
    ), patch.object(
        project_creator, "_create_gitignore"
    ), patch.object(
        project_creator, "_create_poetry_file"
    ), patch.object(
        project_creator, "_create_dockerfile"
    ), patch.object(
        project_creator, "_create_linter_file"
    ), patch.object(
        project_creator, "_create_test_folder"
    ), patch.object(
        project_creator, "_create_flask_app"
    ), patch.object(
        project_creator, "_create_requirements_txt"
    ), patch.object(
        project_creator, "_create_main_file"
    ), patch.object(
        project_creator, "_initialize_git_repository"
    ), patch(
        "boilrpy.project_creator.StringFormatter.format_project_name"
    ), patch(
        "boilrpy.project_creator.os.chdir"
    ):

        project_creator.create_project(project_info)

    mock_create_changelog.assert_called_once_with("0.1.0")


@patch("builtins.print")
def test_create_project_print_message(mock_print, project_creator, project_info):
    with patch.object(
        project_creator, "_check_directory_exist", return_value=False
    ), patch.object(project_creator, "_create_project_directory"), patch.object(
        project_creator, "_create_readme"
    ), patch.object(
        project_creator, "_create_license"
    ), patch.object(
        project_creator, "_create_gitignore"
    ), patch.object(
        project_creator, "_create_changelog"
    ), patch.object(
        project_creator, "_create_poetry_file"
    ), patch.object(
        project_creator, "_create_dockerfile"
    ), patch.object(
        project_creator, "_create_test_folder"
    ), patch.object(
        project_creator, "_create_flask_app"
    ), patch.object(
        project_creator, "_create_requirements_txt"
    ), patch.object(
        project_creator, "_create_linter_file"
    ), patch.object(
        project_creator, "_create_main_file"
    ), patch.object(
        project_creator, "_initialize_git_repository"
    ), patch(
        "boilrpy.project_creator.StringFormatter.format_project_name",
        return_value="test_project",
    ), patch(
        "boilrpy.project_creator.os.chdir"
    ):

        project_creator.create_project(project_info)

    mock_print.assert_called_once_with("Creating project test_project...")


def test_create_readme(project_creator, project_info):
    project_creator.file_generator.generate_readme.return_value = "README content"

    with patch("builtins.open", mock_open()) as mock_file:
        project_creator._create_readme(project_info)

    mock_file.assert_called_once_with("README.md", "w", encoding="utf-8")
    mock_file().write.assert_called_once_with("README content")


def test_create_license(project_creator, project_info):
    project_creator.file_generator.generate_license.return_value = "LICENSE content"

    with patch("builtins.open", mock_open()) as mock_file:
        project_creator._create_license(project_info)

    mock_file.assert_called_once_with("LICENSE", "w", encoding="utf-8")
    mock_file().write.assert_called_once_with("LICENSE content")


def test_create_license_none(project_creator, project_info):
    project_info["license"] = "None"

    with patch("builtins.open", mock_open()) as mock_file:
        project_creator._create_license(project_info)

    mock_file.assert_not_called()


def test_create_gitignore(project_creator):
    project_creator.file_generator.generate_gitignore.return_value = (
        ".gitignore content"
    )

    with patch("builtins.open", mock_open()) as mock_file:
        project_creator._create_gitignore()

    mock_file.assert_called_once_with(".gitignore", "w", encoding="utf-8")
    mock_file().write.assert_called_once_with(".gitignore content")


def test_create_changelog(project_creator):
    project_creator.file_generator.generate_changelog.return_value = "CHANGELOG content"

    with patch("builtins.open", mock_open()) as mock_file:
        project_creator._create_changelog("1.0.0")

    mock_file.assert_called_once_with("CHANGELOG.md", "w", encoding="utf-8")
    mock_file().write.assert_called_once_with("CHANGELOG content")


def test_create_changelog_empty_version(project_creator):
    project_creator.file_generator.generate_changelog.return_value = "CHANGELOG content"

    with patch("builtins.open", mock_open()):
        project_creator._create_changelog("")

    project_creator.file_generator.generate_changelog.assert_called_once_with("")


def test_create_poetry_file_when_not_using_poetry(project_creator):
    project_info = {"use_poetry": False}
    with patch("boilrpy.project_creator.PoetryCreator") as MockPoetryCreator:
        project_creator._create_poetry_file(project_info)
        MockPoetryCreator.assert_not_called()


def test_create_poetry_file_when_using_poetry(project_creator):
    project_info = {"use_poetry": True}
    with patch("boilrpy.project_creator.PoetryCreator") as MockPoetryCreator:
        mock_poetry_creator = Mock()
        MockPoetryCreator.return_value = mock_poetry_creator

        project_creator._create_poetry_file(project_info)

        MockPoetryCreator.assert_called_once_with(project_creator.config)
        mock_poetry_creator.create_poetry_file.assert_called_once_with(project_info)


def test_create_test_folder(project_creator):
    with patch("boilrpy.project_creator.os"):
        with patch("builtins.open", mock_open()) as mock_file:
            project_creator._create_test_folder(True)

    mock_file.assert_called_once_with("tests/__init__.py", "w", encoding="utf-8")


def test_create_test_folder_no_tests(project_creator):
    with patch("boilrpy.project_creator.os") as mock_os:
        with patch("builtins.open", mock_open()) as mock_file:
            project_creator._create_test_folder(False)

    mock_os.makedirs.assert_not_called()
    mock_file.assert_not_called()


def test_create_main_file(project_creator, project_info):
    project_creator.file_generator.generate_main_file.return_value = "main content"

    with patch("builtins.open", mock_open()) as mock_file:
        project_creator._create_main_file(project_info)
    mock_file.assert_not_called()


def test_create_main_file_when_using_flask(project_creator):
    mock_file_writer = Mock(spec=FileWriter)
    project_creator.file_writer = mock_file_writer
    project_creator._create_main_file(use_flask=True)
    project_creator.file_generator.generate_main_file.assert_not_called()
    mock_file_writer.write_file.assert_not_called()


def test_create_main_file_when_not_using_flask(project_creator):
    mock_file_writer = Mock(spec=FileWriter)
    project_creator.file_writer = mock_file_writer
    project_creator._create_main_file(use_flask=False)
    project_creator.file_generator.generate_main_file.assert_called_once()
    mock_file_writer.write_file.assert_called_once_with(
        "main.py", project_creator.file_generator.generate_main_file.return_value
    )


def test_create_flask_app_when_not_using_flask(project_creator):
    project_info = {"use_flask": False}
    with patch("boilrpy.project_creator.FlaskAppCreator") as MockFlaskAppCreator:
        project_creator._create_flask_app(project_info)
        MockFlaskAppCreator.assert_not_called()


def test_create_flask_app_when_using_flask(project_creator):
    project_info = {"use_flask": True}
    with patch("boilrpy.project_creator.FlaskAppCreator") as MockFlaskAppCreator:
        mock_flask_creator = Mock()
        MockFlaskAppCreator.return_value = mock_flask_creator

        project_creator._create_flask_app(project_info)

        MockFlaskAppCreator.assert_called_once_with(project_creator.config)
        mock_flask_creator.create_flask_project.assert_called_once_with(project_info)


@patch("boilrpy.project_creator.os")
def test_initialize_git_repository(mock_os, project_creator):
    mock_os.getcwd.return_value = "/test"
    mock_os.path.join.return_value = "/test/.git"

    project_creator._initialize_git_repository()
    mock_os.chmod.assert_called_once_with("/test/.git", 0o775)
    mock_os.system.assert_called_once_with("git init")


def test_create_project_directory(project_creator):
    project_creator.project_name = "test_project"
    mock_file_writer = Mock(spec=FileWriter)
    project_creator.file_writer = mock_file_writer

    with patch("os.getcwd", return_value="/current/dir"):
        result = project_creator._create_project_directory()

    expected_path = os.path.join("/current/dir", "test_project")
    mock_file_writer.create_directory.assert_called_once_with(
        expected_path, exist_ok=False
    )
    assert result == expected_path


def test_create_project_directory_error(project_creator):
    project_creator.project_name = "test_project"
    mock_file_writer = Mock(spec=FileWriter)
    mock_file_writer.create_directory.side_effect = FileWriterError(
        "Failed to create directory"
    )
    project_creator.file_writer = mock_file_writer

    with patch("os.getcwd", return_value="/current/dir"), pytest.raises(
        FileWriterError, match="Failed to create directory"
    ):
        project_creator._create_project_directory()


@patch("os.path.exists")
@patch("os.path.isdir")
def test_check_directory_exist_true(mock_isdir, mock_exists, project_creator):
    mock_exists.return_value = True
    mock_isdir.return_value = True

    result = project_creator._check_directory_exist("test_directory")

    assert result is True
    mock_exists.assert_called_once_with("test_directory")
    mock_isdir.assert_called_once_with("test_directory")


@patch("os.path.exists")
@patch("os.path.isdir")
def test_check_directory_exist_false_not_exists(
    mock_isdir, mock_exists, project_creator
):
    mock_exists.return_value = False
    mock_isdir.return_value = True

    result = project_creator._check_directory_exist("test_directory")

    assert result is False
    mock_exists.assert_called_once_with("test_directory")
    mock_isdir.assert_not_called()


@patch("os.path.exists")
@patch("os.path.isdir")
def test_check_directory_exist_false_not_dir(mock_isdir, mock_exists, project_creator):
    mock_exists.return_value = True
    mock_isdir.return_value = False

    result = project_creator._check_directory_exist("test_directory")

    assert result is False
    mock_exists.assert_called_once_with("test_directory")
    mock_isdir.assert_called_once_with("test_directory")


def test_create_dockerfile_with_docker(project_creator):
    project_info = {"name": "test_project", "use_docker": True, "use_flask": True}

    with patch("builtins.open", mock_open()) as mock_file:
        project_creator._create_dockerfile(project_info)

    assert mock_file.call_count == 2
    project_creator.file_generator.generate_dockerfile.assert_called_once()
    project_creator.file_generator.generate_dockerignore.assert_called_once()

    mock_file.assert_any_call("Dockerfile", "w", encoding="utf-8")
    mock_file.assert_any_call(".dockerignore", "w", encoding="utf-8")


def test_create_dockerfile_early_return(project_creator):
    project_info = {"name": "test_project", "use_docker": False}

    # Spy on the method to check if it returns early
    with patch.object(
        project_creator, "_create_dockerfile", wraps=project_creator._create_dockerfile
    ) as spy:
        result = project_creator._create_dockerfile(project_info)

    assert result is None
    spy.assert_called_once_with(project_info)

    project_creator.file_generator.generate_dockerfile.assert_not_called()
    project_creator.file_generator.generate_dockerignore.assert_not_called()


def test_create_pylintrc(project_creator):
    project_creator.file_generator.generate_pylint.return_value = "Pylintrc content"

    with patch("builtins.open", mock_open()) as mock_file:
        project_creator._create_linter_file(True)
        mock_file.assert_called_once_with(".pylintrc", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with("Pylintrc content")

def test_not_create_pylintrc(project_creator):
    project_creator.file_generator.generate_pylint.return_value = "Pylintrc content"

    with patch("builtins.open", mock_open()) as mock_file:
        project_creator._create_linter_file(False)
    assert mock_file.call_count == 0


def test_create_requirments_txt(project_creator):
    project_info = {"name": "test_project", "use_flask": False}
    project_creator.file_generator.generate_requirements_txt.return_value = (
        "Requirements content"
    )

    with patch("builtins.open", mock_open()) as mock_file:
        project_creator._create_requirements_txt(project_info)

    mock_file.assert_called_once_with("requirements.txt", "w", encoding="utf-8")
    mock_file().write.assert_called_once_with("Requirements content")
