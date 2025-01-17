import pytest
from unittest.mock import Mock, patch
from boilrpy.file_generator import FileGenerator
from boilrpy.config import Config


@pytest.fixture
def mock_config():
    return Mock(spec=Config)


@pytest.fixture
def file_generator(mock_config):
    with patch("boilrpy.file_generator.ReadmeGenerator") as mock_readme, \
            patch("boilrpy.file_generator.LicenseGenerator") as mock_license, \
            patch("boilrpy.file_generator.GitignoreGenerator") as mock_gitignore, \
            patch("boilrpy.file_generator.ChangelogGenerator") as mock_changelog, \
            patch("boilrpy.file_generator.DockerfileGenerator") as mock_docker, \
            patch("boilrpy.file_generator.MainFileGenerator") as mock_main:

        mock_readme.return_value.generate.return_value = "Mock README content"
        mock_license.return_value.generate.return_value = "Mock LICENSE content"
        mock_gitignore.return_value.generate.return_value = "Mock .gitignore content"
        mock_changelog.return_value.generate.return_value = "Mock CHANGELOG content"
        mock_docker.return_value.generate_dockerfile.return_value = "Mock Dockerfile content"
        mock_docker.return_value.generate_dockerignore.return_value = "Mock .dockerignore content"
        mock_main.return_value.generate.return_value = "Mock main.py content"

        yield FileGenerator(mock_config)


def test_generate_readme(file_generator):
    project_info = {"name": "Test Project", "description": "A test project"}
    result = file_generator.generate_readme(project_info)
    assert result == "Mock README content"
    file_generator.readme_generator.generate.assert_called_once_with(
        project_info)


def test_generate_license(file_generator):
    result = file_generator.generate_license("MIT", "John Doe")
    assert result == "Mock LICENSE content"
    file_generator.license_generator.generate.assert_called_once_with(
        "MIT", "John Doe")


def test_generate_gitignore(file_generator):
    result = file_generator.generate_gitignore()
    assert result == "Mock .gitignore content"
    file_generator.gitignore_generator.generate.assert_called_once()


def test_generate_changelog(file_generator):
    result = file_generator.generate_changelog("1.0.0")
    assert result == "Mock CHANGELOG content"
    file_generator.changelog_generator.generate.assert_called_once_with(
        "1.0.0")


def test_generate_dockerfile(file_generator):
    result = file_generator.generate_dockerfile("test_project")
    assert result == "Mock Dockerfile content"
    file_generator.dockerfile_generator.generate_dockerfile.assert_called_once_with(
        "test_project")


def test_generate_dockerignore(file_generator):
    result = file_generator.generate_dockerignore()
    assert result == "Mock .dockerignore content"
    file_generator.dockerfile_generator.generate_dockerignore.assert_called_once()


def test_generate_main_file(file_generator):
    result = file_generator.generate_main_file()
    assert result == "Mock main.py content"
    file_generator.main_file_generator.generate.assert_called_once()


def test_file_generator_initialization(mock_config):
    with patch("boilrpy.file_generator.ReadmeGenerator") as mock_readme, \
            patch("boilrpy.file_generator.LicenseGenerator") as mock_license, \
            patch("boilrpy.file_generator.GitignoreGenerator") as mock_gitignore, \
            patch("boilrpy.file_generator.ChangelogGenerator") as mock_changelog, \
            patch("boilrpy.file_generator.DockerfileGenerator") as mock_docker, \
            patch("boilrpy.file_generator.MainFileGenerator") as mock_main:

        file_generator = FileGenerator(mock_config)

        assert isinstance(file_generator.config, Mock)
        assert isinstance(file_generator.readme_generator, Mock)
        assert isinstance(file_generator.license_generator, Mock)
        assert isinstance(file_generator.gitignore_generator, Mock)
        assert isinstance(file_generator.changelog_generator, Mock)
        assert isinstance(file_generator.dockerfile_generator, Mock)
        assert isinstance(file_generator.main_file_generator, Mock)

        mock_readme.assert_called_once_with(mock_config)
        mock_license.assert_called_once_with(mock_config)
        mock_gitignore.assert_called_once_with(mock_config)
        mock_changelog.assert_called_once_with(mock_config)
        mock_docker.assert_called_once_with(mock_config)
        mock_main.assert_called_once_with(mock_config)
