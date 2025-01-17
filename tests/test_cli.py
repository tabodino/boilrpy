from boilrpy.input_validator import InputValidator
import pytest
from unittest.mock import MagicMock, patch, call
from boilrpy.config import Config
from boilrpy.cli import CLI


@pytest.fixture
def mock_config():
    mock = MagicMock(spec=Config)
    mock.get_available_licenses.return_value = Config().available_licenses
    return mock


def test_gather_project_info(mock_config):
    cli = CLI(mock_config)
    with patch("builtins.input", side_effect=[
        "TestProject",
        "A test project",
        "1.0.0",
        "John Doe",
        "1",
        "y",
        "y",
        "n",
    ]):
        project_info = cli.gather_project_info()

    assert project_info["name"] == "TestProject"
    assert project_info["description"] == "A test project"
    assert project_info["version"] == "1.0.0"
    assert project_info["author"] == "John Doe"
    assert "license" in project_info
    assert project_info["use_poetry"] is True
    assert project_info["create_tests"] is False


def test_get_valid_input(mock_config):
    cli = CLI(mock_config)
    with patch("builtins.input", return_value="TestProject"):
        assert cli._get_valid_input(
            "Enter project name: ",
            InputValidator.validate_project_name
        ) == "TestProject"

    with patch("builtins.input", side_effect=["", "test"]) as mocked_input:
        result = cli._get_valid_input(
            "Enter project name: ",
            InputValidator.validate_project_name
        )
        assert result == "test"
        assert mocked_input.call_count == 2
        assert mocked_input.call_args_list == [
            call("Enter project name: "),
            call("Enter project name: ")
        ]


def test_yes_no_question(mock_config):
    cli = CLI(mock_config)

    with patch("builtins.input", return_value="y"):
        assert cli._yes_no_question("Test question?") is True

    with patch("builtins.input", return_value="n"):
        assert cli._yes_no_question("Test question?") is False

    with patch("builtins.input", return_value=""):
        assert cli._yes_no_question(
            "Test question with default?", "n") is False

    with patch("builtins.input", return_value=""):
        assert cli._yes_no_question(
            "Test question with default?", "y") is True

    with patch("builtins.input", side_effect=["", "y"]) as mocked_input:
        result = cli._yes_no_question("Test question with default?")
        assert result is True
        assert mocked_input.call_count == 2
        assert mocked_input.call_args_list == [
            call("Test question with default? (y/n): "),
            call("Test question with default? (y/n): ")
        ]


def test_choose_license(mock_config):
    cli = CLI(mock_config)
    with patch("builtins.input", return_value="2"):
        assert cli._choose_license() == "Apache"

    with patch("builtins.input", side_effect=["", "1"]) as mocked_input:
        result = cli._choose_license()
        assert result == "MIT"
        assert mocked_input.call_count == 2
        assert mocked_input.call_args_list == [
            call("Choose a license (enter the number): "),
            call("Choose a license (enter the number): ")
        ]
