import pytest
from unittest.mock import Mock
from boilrpy.file_generators.requirements_generator import RequirementsGenerator


@pytest.fixture
def mock_base_generator():
    return Mock()


def test_requirements_generator_empty_project_info(mock_base_generator):
    generator = RequirementsGenerator(mock_base_generator)
    result = generator.generate({})
    assert result == ""


def test_requirements_generator_all_options_true(mock_base_generator):
    generator = RequirementsGenerator(mock_base_generator)
    project_info = {"use_pylint": True, "use_flask": True, "create_tests": True}
    result = generator.generate(project_info)
    assert "pylint" in result
    assert "flask" in result
    assert "python-dotenv" in result
    assert "pytest" in result


def test_requirements_generator_some_options_true(mock_base_generator):
    generator = RequirementsGenerator(mock_base_generator)
    project_info = {"use_pylint": True, "use_flask": False, "create_tests": True}
    result = generator.generate(project_info)
    assert "pylint" in result
    assert "pytest" in result
    assert "flask" not in result
    assert "python-dotenv" not in result


def test_requirements_generator_no_options_true(mock_base_generator):
    generator = RequirementsGenerator(mock_base_generator)
    project_info = {"use_pylint": False, "use_flask": False, "create_tests": False}
    result = generator.generate(project_info)
    assert result == ""


def test_requirements_generator_only_flask_true(mock_base_generator):
    generator = RequirementsGenerator(mock_base_generator)
    project_info = {"use_pylint": False, "use_flask": True, "create_tests": False}
    result = generator.generate(project_info)
    assert "flask" in result
    assert "python-dotenv" in result
    assert "pylint" not in result
    assert "pytest" not in result
