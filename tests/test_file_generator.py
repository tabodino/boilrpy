import pytest
from unittest.mock import Mock, patch
from boilrpy.file_generator import FileGenerator, GeneratorFactory
from boilrpy.config import Config


@pytest.fixture
def mock_config():
    return Mock(spec=Config)


@pytest.fixture
def mock_generator_factory():
    with patch("boilrpy.file_generator.GeneratorFactory") as mock_factory:
        mock_generators = {
            "readme": Mock(),
            "license": Mock(),
            "gitignore": Mock(),
            "changelog": Mock(),
            "dockerfile": Mock(),
            "pylint": Mock(),
            "main_file": Mock(),
            "requirements": Mock(),
            "flask": Mock(),
        }
        mock_factory.create_generator.side_effect = (
            lambda generator_type, config: mock_generators[generator_type]
        )
        for gen_type, generator in mock_generators.items():
            generator.generate.return_value = f"Mock {gen_type} content"
        mock_generators["dockerfile"].generate_dockerfile.return_value = (
            "Mock Dockerfile content"
        )
        mock_generators["dockerfile"].generate_dockerignore.return_value = (
            "Mock .dockerignore content"
        )
        mock_generators["flask"].generate_app_file.return_value = "Mock flask content"
        mock_generators["flask"].generate_base_template.return_value = (
            "Mock flask content"
        )
        mock_generators["flask"].generate_index_template.return_value = (
            "Mock flask content"
        )
        mock_generators["flask"].generate_dot_env_file.return_value = (
            "Mock flask content"
        )
        mock_generators["flask"].generate_style_file.return_value = "Mock flask content"
        mock_generators["flask"].generate_script_file.return_value = (
            "Mock flask content"
        )
        yield mock_factory


@pytest.fixture
def file_generator(mock_config, mock_generator_factory):
    with patch(
        "boilrpy.file_generator.GeneratorFactory", return_value=mock_generator_factory
    ):
        return FileGenerator(mock_config)


def test_generate_readme(file_generator, mock_generator_factory):
    project_info = {"name": "Test Project", "description": "A test project"}
    result = file_generator.generate_readme(project_info)
    assert result == "Mock readme content"
    mock_generator_factory.create_generator.assert_called_once_with(
        "readme", file_generator.config
    )


def test_generate_license(file_generator, mock_generator_factory):
    result = file_generator.generate_license("MIT", "John Doe")
    assert result == "Mock license content"
    mock_generator_factory.create_generator.assert_called_with(
        "license", file_generator.config
    )


def test_generate_gitignore(file_generator, mock_generator_factory):
    result = file_generator.generate_gitignore()
    assert result == "Mock gitignore content"
    mock_generator_factory.create_generator.assert_called_with(
        "gitignore", file_generator.config
    )


def test_generate_changelog(file_generator, mock_generator_factory):
    result = file_generator.generate_changelog("1.0.0")
    assert result == "Mock changelog content"
    mock_generator_factory.create_generator.assert_called_with(
        "changelog", file_generator.config
    )


def test_generate_dockerfile(file_generator, mock_generator_factory):
    result = file_generator.generate_dockerfile("test_project", False)
    assert result == "Mock Dockerfile content"
    mock_generator_factory.create_generator.assert_called_with(
        "dockerfile", file_generator.config
    )


def test_generate_dockerignore(file_generator, mock_generator_factory):
    result = file_generator.generate_dockerignore()
    assert result == "Mock .dockerignore content"
    mock_generator_factory.create_generator.assert_called_with(
        "dockerfile", file_generator.config
    )


def test_generate_pylint(file_generator, mock_generator_factory):
    result = file_generator.generate_pylint()
    assert result == "Mock pylint content"
    mock_generator_factory.create_generator.assert_called_with(
        "pylint", file_generator.config
    )


def test_generate_main_file(file_generator, mock_generator_factory):
    result = file_generator.generate_main_file()
    assert result == "Mock main_file content"
    mock_generator_factory.create_generator.assert_called_with(
        "main_file", file_generator.config
    )


def test_generate_flask_app_file(file_generator, mock_generator_factory):
    result = file_generator.generate_flask_app_file()
    assert result == "Mock flask content"
    mock_generator_factory.create_generator.assert_called_with(
        "flask", file_generator.config
    )


def test_generate_base_template(file_generator, mock_generator_factory):
    project_info = {"name": "Test Project", "description": "A test project"}
    result = file_generator.generate_base_template(project_info)
    assert result == "Mock flask content"
    mock_generator_factory.create_generator.assert_called_with(
        "flask", file_generator.config
    )


def test_generate_index_template(file_generator, mock_generator_factory):
    project_info = {"name": "Test Project", "description": "A test project"}
    result = file_generator.generate_index_template(project_info)
    assert result == "Mock flask content"
    mock_generator_factory.create_generator.assert_called_with(
        "flask", file_generator.config
    )


def test_generate_dot_env_file(file_generator, mock_generator_factory):
    result = file_generator.generate_dot_env_file()
    assert result == "Mock flask content"
    mock_generator_factory.create_generator.assert_called_with(
        "flask", file_generator.config
    )


def test_generate_style_file(file_generator, mock_generator_factory):
    result = file_generator.generate_style_file()
    assert result == "Mock flask content"
    mock_generator_factory.create_generator.assert_called_with(
        "flask", file_generator.config
    )


def test_generate_script_file(file_generator, mock_generator_factory):
    result = file_generator.generate_script_file()
    assert result == "Mock flask content"
    mock_generator_factory.create_generator.assert_called_with(
        "flask", file_generator.config
    )


def test_generate_requirements(file_generator, mock_generator_factory):
    project_info = {"use_flask": False, "use_pylint": False, "create_tests": False}
    result = file_generator.generate_requirements_txt(project_info)
    assert result == "Mock requirements content"
    mock_generator_factory.create_generator.assert_called_with(
        "requirements", file_generator.config
    )


def test_file_generator_initialization(mock_config):
    file_generator = FileGenerator(mock_config)
    assert isinstance(file_generator.config, Config)
    assert isinstance(file_generator.generators, dict)
    assert len(file_generator.generators) == 0


def test_generator_factory():
    config = Mock(spec=Config)
    factory = GeneratorFactory()
    for generator_type in [
        "readme",
        "license",
        "gitignore",
        "changelog",
        "main_file",
        "dockerfile",
        "pylint",
        "requirements",
        "flask",
    ]:
        generator = factory.create_generator(generator_type, config)
        assert hasattr(generator, "generate")

    with pytest.raises(ValueError):
        factory.create_generator("non_existent_type", config)
