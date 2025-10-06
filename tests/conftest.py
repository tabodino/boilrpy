
import pytest
from unittest.mock import MagicMock
from boilrpy.config import Config


@pytest.fixture
def mock_config():
    """Create a mock Config object."""
    config = MagicMock(spec=Config)
    config.get_charset.return_value = "utf-8"
    config.get_available_licenses.return_value = [
        "MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "None"
    ]
    return config

@pytest.fixture
def base_project_info():
    """Base project information dictionary."""
    return {
        "name": "test-project",
        "description": "A test project",
        "author": "Test Author",
        "version": "0.1.0",
        "license": "MIT",
        "use_flask": False,
        "create_tests": True,
        "use_pylint": True,
        "libraries": []
    }

@pytest.fixture
def project_info_with_flask(base_project_info):
    """Project info with Flask enabled."""
    info = base_project_info.copy()
    info["use_flask"] = True
    return info


@pytest.fixture
def project_info_with_libraries(base_project_info):
    """Project info with additional libraries."""
    info = base_project_info.copy()
    info["libraries"] = ["requests", "pandas", "numpy"]
    return info


@pytest.fixture
def project_info_minimal(base_project_info):
    """Minimal project info without tests or linting."""
    info = base_project_info.copy()
    info["create_tests"] = False
    info["use_pylint"] = False
    return info
