import pytest
from unittest.mock import MagicMock, Mock
from boilrpy.file_generators.dockerfile_generator import DockerfileGenerator
from boilrpy.config import Config


@pytest.fixture
def mock_config():
    config = Mock(spec=Config)
    config.get_charset.return_value = "utf-8"
    config.use_camel_case = False
    config.python_version = "3.11"
    return config


@pytest.fixture
def mock_dockerfile_generator():
    return Mock(spec=DockerfileGenerator)


@pytest.fixture
def dockerfile_generator(mock_config):
    return DockerfileGenerator(mock_config)


def test_generate_dockerignore(dockerfile_generator):
    dockerignore_content = dockerfile_generator.generate_dockerignore()
    assert isinstance(dockerignore_content, str)
    expected_entries = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".Python",
        "env",
        "pip-log.txt",
        "pip-delete-this-directory.txt",
        ".tox",
        ".coverage",
        ".coverage.*",
        ".cache",
        "nosetests.xml",
        "coverage.xml",
        "*.cover",
        "*.log",
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".hypothesis",
    ]

    for entry in expected_entries:
        assert entry in dockerignore_content


def test_generate_dockerfile(dockerfile_generator, mock_config):
    project_name = "test_project"
    use_flask = False
    dockerfile_content = dockerfile_generator.generate_dockerfile(
        project_name, use_flask
    )

    assert f"FROM python:{mock_config.python_version}-slim" in dockerfile_content
    assert "WORKDIR /app" in dockerfile_content
    assert "COPY requirements.txt ." in dockerfile_content
    assert "RUN pip install --no-cache-dir -r requirements.txt" in dockerfile_content
    assert "COPY . ." in dockerfile_content
    assert f'CMD ["python", "main.py"]' in dockerfile_content
    use_flask = True
    dockerfile_content = dockerfile_generator.generate_dockerfile(
        project_name, use_flask
    )
    assert f'CMD ["flask", "run"]' in dockerfile_content


def test_generate(dockerfile_generator):
    project_name = "test_project"
    use_flask = False
    dockerfile_generator.generate_dockerfile = MagicMock()
    dockerfile_generator.generate_dockerignore = MagicMock()

    dockerfile_generator.generate(project_name, use_flask)
    dockerfile_generator.generate_dockerfile.assert_called_once_with(
        project_name, use_flask
    )
    dockerfile_generator.generate_dockerignore.assert_called_once()
