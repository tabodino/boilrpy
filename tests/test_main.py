import pytest
import sys
from unittest.mock import Mock, patch
from boilrpy.__main__ import run_cli, main

class DummyArgs:
    def __init__(self, check_deps=False):
        self.check_deps = check_deps

# ✅ Test du chemin --check-deps
def test_run_cli_check_deps(monkeypatch):
    called = {}

    def mock_print_status():
        called["status"] = True

    monkeypatch.setattr(
        "boilrpy.dependency_creators.checker.DependencyManagerChecker.print_status",
        mock_print_status
    )

    args = DummyArgs(check_deps=True)
    run_cli(args)

    assert called.get("status") is True

# ✅ Test du chemin principal avec mocks
@patch("boilrpy.__main__.Config")
@patch("boilrpy.__main__.CLI")
@patch("boilrpy.__main__.ProjectCreator")
def test_run_cli_main_path(MockProjectCreator, MockCLI, MockConfig):
    mock_config = MockConfig.return_value
    mock_cli = MockCLI.return_value
    mock_project_creator = MockProjectCreator.return_value

    mock_cli.gather_project_info.return_value = {
        "name": "test_project",
        "description": "Test description",
    }

    args = DummyArgs(check_deps=False)
    run_cli(args)

    MockConfig.assert_called_once()
    MockCLI.assert_called_once_with(mock_config)
    mock_cli.gather_project_info.assert_called_once()
    MockProjectCreator.assert_called_once_with(mock_config)
    mock_project_creator.create_project.assert_called_once_with(
        mock_cli.gather_project_info.return_value
    )

# ✅ Test du cas d’exception dans create_project
@patch("boilrpy.__main__.Config")
@patch("boilrpy.__main__.CLI")
@patch("boilrpy.__main__.ProjectCreator")
def test_run_cli_exception(MockProjectCreator, MockCLI, MockConfig):
    mock_config = MockConfig.return_value
    mock_cli = MockCLI.return_value
    mock_project_creator = MockProjectCreator.return_value

    mock_cli.gather_project_info.return_value = {
        "name": "test_project",
        "description": "Test description",
    }

    mock_project_creator.create_project.side_effect = Exception("Test exception")

    args = DummyArgs(check_deps=False)
    with pytest.raises(Exception, match="Test exception"):
        run_cli(args)

# ✅ Test du bloc main() avec argparse simulé
@patch("boilrpy.__main__.run_cli")
def test_main_invocation(mock_run_cli, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["boilrpy"])
    main()
    mock_run_cli.assert_called_once()
