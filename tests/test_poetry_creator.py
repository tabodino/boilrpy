import subprocess
import sys
import pytest
from unittest.mock import MagicMock, Mock, patch, mock_open
from boilrpy.poetry_creator import PoetryCreator
from boilrpy.config import Config


@pytest.fixture
def mock_config():
    config = Mock(spec=Config)
    config.get_charset.return_value = "utf-8"
    return config


@pytest.fixture
def poetry_creator(mock_config):
    return PoetryCreator(mock_config)


def test_create_poetry_file_not_using_poetry(poetry_creator):

    project_info = {"use_poetry": False}
    with patch("subprocess.run") as mock_run, patch.object(
        poetry_creator, "_create_packages"
    ) as mock_create_packages, patch.object(
        poetry_creator, "_update_pyproject_toml"
    ) as mock_update:

        poetry_creator.create_poetry_file(project_info)

        mock_run.assert_not_called()
        mock_create_packages.assert_not_called()
        mock_update.assert_not_called()


def test_create_poetry_file_using_poetry(poetry_creator):
    project_info = {
        "use_poetry": True,
        "use_pylint": True,
        "create_tests": False,
        "name": "test_project",
        "version": "0.1.0",
        "description": "A test project",
        "author": "Test Author",
        "license": "MIT",
    }

    with patch("subprocess.run") as mock_run, patch.object(
        poetry_creator,
        "_create_packages",
        return_value=(["package1"], ["dev-package1"]),
    ), patch.object(poetry_creator, "_update_pyproject_toml") as mock_update:

        poetry_creator.create_poetry_file(project_info)

        assert mock_run.call_count == 3
    
        mock_update.assert_called_once_with(project_info)

def test_run_poetry_command_file_not_found_error(poetry_creator):
    with patch('subprocess.run', side_effect=FileNotFoundError()) as mock_run:
        project_info = {
            "use_poetry": True, 
            "create_tests": True, 
            "use_pylint": True, 
            "use_flask": True
        }
        poetry_creator.create_poetry_file(project_info)
        assert mock_run.call_count == 1

def test_create_poetry_file_subprocess_error(poetry_creator):
    project_info = {
        "use_poetry": True,
        "create_tests": False,
        "use_pylint": True,
        "use_flask": True,
    }

    with patch(
        "subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd")
    ) as mock_run, patch("builtins.print") as mock_print:

        poetry_creator.create_poetry_file(project_info)
        mock_run.assert_called_once()
        assert "Poetry initialization failed" in mock_print.call_args[0][0]

def test_check_poetry_version(poetry_creator):
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout="Poetry version 1.8.5\n")
        assert poetry_creator._check_poetry_version() == "1.8.5"

        mock_run.return_value = MagicMock(stdout="Poetry version 2.0.0\n")
        assert poetry_creator._check_poetry_version() == "2.0.0"

def test_update_pyproject_toml_v1(poetry_creator):
    project_info = {
        "name": "test_project",
        "version": "0.1.0",
        "description": "A test project",
        "author": "Test Author",
        "license": "MIT",
    }

    mock_toml_content = {"tool": {"poetry": {}}}


    with patch("builtins.open", mock_open()) as mock_file, patch(
        "toml.load", return_value=mock_toml_content
    ) as mock_load, patch("toml.dump") as mock_dump, patch.object(
        poetry_creator, "_check_poetry_version", return_value="1.8.5"
    ):

        poetry_creator._update_pyproject_toml(project_info)

        mock_file.assert_any_call(
            "pyproject.toml", "r", encoding=poetry_creator.charset
        )
        mock_file.assert_any_call(
            "pyproject.toml", "w", encoding=poetry_creator.charset
        )

        mock_load.assert_called_once()
        mock_dump.assert_called_once()

        updated_toml = mock_dump.call_args[0][0]
        assert updated_toml["tool"]["poetry"]["name"] == "test_project"
        assert updated_toml["tool"]["poetry"]["version"] == "0.1.0"
        assert updated_toml["tool"]["poetry"]["description"] == "A test project"
        assert updated_toml["tool"]["poetry"]["authors"] == ["Test Author"]
        assert updated_toml["tool"]["poetry"]["license"] == "MIT"

def test_update_pyproject_toml_v2(poetry_creator):
    project_info = {
        "name": "test_project",
        "version": "0.1.0",
        "description": "A test project",
        "author": "Test Author",
        "license": "MIT",
    }

    mock_toml_content = {"project": {}}

    with patch("builtins.open", mock_open()) as mock_file, patch(
        "toml.load", return_value=mock_toml_content
    ) as mock_load, patch("toml.dump") as mock_dump, patch.object(
        poetry_creator, "_check_poetry_version", return_value="2.0.1"
    ):

        poetry_creator._update_pyproject_toml(project_info)

        mock_file.assert_any_call(
            "pyproject.toml", "r", encoding=poetry_creator.charset
        )
        mock_file.assert_any_call(
            "pyproject.toml", "w", encoding=poetry_creator.charset
        )

        mock_load.assert_called_once()
        mock_dump.assert_called_once()

        updated_toml = mock_dump.call_args[0][0]
       
        assert updated_toml["project"]["name"] == "test_project"
        assert updated_toml["project"]["version"] == "0.1.0"
        assert updated_toml["project"]["description"] == "A test project"
        assert updated_toml["project"]["authors"] == [{"name": "Test Author"}]
        assert updated_toml["project"]["license"] == {"text": "MIT"}

def test_create_packages(poetry_creator):
    project_info = {"create_tests": True, "use_pylint": True, "use_flask": True}

    packages, dev_packages = poetry_creator._create_packages(project_info)

    assert "flask" in packages
    assert "python-dotenv" in packages
    assert "pytest" in dev_packages
    assert "pylint" in dev_packages
