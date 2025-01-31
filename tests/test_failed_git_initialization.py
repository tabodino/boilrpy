from unittest.mock import patch, MagicMock
from subprocess import CalledProcessError
import pytest
from boilrpy.project_creator import ProjectCreator


@pytest.fixture
def project_creator():
    config = MagicMock()
    return ProjectCreator(config)


@pytest.fixture
def mock_run():
    with patch('subprocess.run', new_callable=MagicMock) as mock:
        yield mock

def test_git_not_found(mock_run, project_creator):
    with patch('subprocess.run', side_effect=FileNotFoundError()) as mock_run:
        project_creator._initialize_git_repository()
        assert mock_run.call_count == 1
        mock_run.assert_called_once_with(["git", "--version"], check=True, capture_output=True)

def test_git_initialization_error(mock_run, project_creator):
    with patch('subprocess.run', side_effect=CalledProcessError(0, "git", output="Git init failded")) as mock_run:
        project_creator._initialize_git_repository()
    
        assert mock_run.call_count == 1