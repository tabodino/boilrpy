from colorama import Fore, Style
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
        "y",
    ]):
        project_info = cli.gather_project_info()
    
    assert project_info["name"] == "TestProject"
    assert project_info["description"] == "A test project"
    assert project_info["version"] == "1.0.0"
    assert project_info["author"] == "John Doe"
    assert "license" in project_info
    assert project_info["use_poetry"] is True
    assert project_info["create_tests"] is False
    assert project_info["use_pylint"] is True


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

def mock_input(prompt):
    return prompt

def test_get_valid_input(capsys, mock_config):
    cli = CLI(mock_config)
    with patch.object(cli, "_get_valid_input", return_value="Mocked input"):
        prompt = "Please enter something:" 
        result = cli._get_valid_input("Please enter something:")
        expected_prompt = f"{Fore.GREEN}{prompt}{Style.RESET_ALL}" 
        assert result == "Mocked input"
    
    with patch('builtins.input', side_effect=['', 'test input']):
        result = cli._get_valid_input(prompt, InputValidator.validate_project_name)
    
    assert result == 'test input'    


@patch("builtins.input")
def test_get_valid_input_empty_prompt(mock_input, mock_config):
    cli = CLI(mock_config)
    prompt = ""
    expected_input = "Empty prompt test"
    mock_input.return_value = expected_input

    result = cli._get_valid_input(prompt, InputValidator.validate_project_name)

    mock_input.assert_called_once()
    call_args = mock_input.call_args[0][0]
    assert call_args.startswith(prompt)
    assert call_args.endswith(prompt)
    assert len(call_args) == 0
    assert result == expected_input

@patch("builtins.input")
def test_get_valid_input_original(mock_input, mock_config):
    cli = CLI(mock_config)
    prompt = "Enter something: "
    mock_input.return_value = "test input"
    result = cli._get_valid_input(prompt, InputValidator.validate_project_name)
    
    expected_prompt = f"{Fore.GREEN}Enter something: {Fore.RESET}"
    prompt == expected_prompt
    assert result == mock_input.return_value

@patch("builtins.input", side_effect=KeyboardInterrupt)
def test_get_valid_input_keyboard_interrupt(mock_input, mock_config):
    prompt = "Project name: "
    cli = CLI(mock_config)
    with pytest.raises(KeyboardInterrupt):
        cli._get_valid_input(prompt, InputValidator.validate_project_name)

