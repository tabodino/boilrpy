import io
import sys
import unittest
import pytest
import importlib
from unittest.mock import Mock, patch
from boilrpy.__main__ import main


@pytest.fixture
def mock_main():
    with patch("boilrpy.__main__.main") as mock_main:
        yield mock_main


@pytest.fixture
def mock_config():
    return Mock()


@pytest.fixture
def mock_cli():
    cli = Mock()
    cli.gather_project_info.return_value = {
        "name": "test_project",
        "version": "0.1.0",
        "description": "A test project",
        "author": "Test Author",
        "license": "MIT",
        "use_poetry": True,
        "create_tests": True
    }
    return cli


@pytest.fixture
def mock_project_creator():
    return Mock()

def test_main_method():

    with patch("boilrpy.__name__", "__main__"):
        with patch("boilrpy.__main__.main") as mock_main:
            from boilrpy.__main__ import main  # Re-import the script
            if __name__ == "__main__":
                mock_main.assert_called_once()


@patch("boilrpy.__main__.Config")
@ patch("boilrpy.__main__.CLI")
@ patch("boilrpy.__main__.ProjectCreator")
def test_main(MockProjectCreator, MockCLI, MockConfig):
    mock_config = MockConfig.return_value
    mock_cli = MockCLI.return_value
    mock_project_creator = MockProjectCreator.return_value
    mock_cli.gather_project_info.return_value = {
        "name": "test_project", "description": "Test description"}
    with patch("builtins.print") as mock_print:
        print("********Calling main()")
        main()
        print("**********Finished calling main()")

    MockConfig.assert_called_once()
    MockCLI.assert_called_once_with(mock_config)
    mock_cli.gather_project_info.assert_called_once()
    MockProjectCreator.assert_called_once_with(mock_config)
    mock_project_creator.create_project.assert_called_once_with(
        mock_cli.gather_project_info.return_value)


def import_module(module_name):
    return importlib.import_module(module_name)

@patch("boilrpy.__main__.Config")
@patch("boilrpy.__main__.CLI")
@patch("boilrpy.__main__.ProjectCreator")
def test_main_exception_handling(
        MockProjectCreator,
        MockCLI,
        MockConfig,
        mock_config,
        mock_cli,
        mock_project_creator):
    MockConfig.return_value = mock_config
    MockCLI.return_value = mock_cli
    MockProjectCreator.return_value = mock_project_creator
    mock_project_creator.create_project.side_effect = Exception(
        "Test exception")

    with pytest.raises(Exception):
        main()

    MockConfig.assert_called_once()
    MockCLI.assert_called_once_with(mock_config)
    mock_cli.gather_project_info.assert_called_once()
    MockProjectCreator.assert_called_once_with(mock_config)
