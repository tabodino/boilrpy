import pytest
from unittest.mock import Mock, patch
from boilrpy.file_generators.readme_generator import ReadmeGenerator
from boilrpy.config import Config


@pytest.fixture
def mock_config():
    return Mock(spec=Config)


@pytest.fixture
def readme_generator(mock_config):
    with patch(
        "boilrpy.file_generators.readme_generator.BaseGenerator.render_template"
    ) as mock_render:
        generator = ReadmeGenerator(mock_config)
        generator._render_template = mock_render
        yield generator


def test_generate_readme_with_poetry_and_tests(readme_generator):
    project_info = {
        "name": "test project",
        "description": "A test project",
        "use_poetry": True,
        "create_tests": True,
        "license": "MIT"
    }

    mock_content = """
# Test Project

A test project

## Setup

### Using Poetry

poetry install

## Usage

poetry run python main.py

## Testing

```poetry run pytest```

## Contributing

...

## License

This project is licensed under the MIT License.
"""

    readme_generator._render_template.return_value = mock_content

    readme = readme_generator.generate(project_info).strip()

    assert readme == mock_content.strip()
    readme_generator._render_template.assert_called_once()
    args, kwargs = readme_generator._render_template.call_args
    assert "name" in kwargs and kwargs["name"] == "Test Project"
    assert "description" in kwargs and kwargs[
        "description"] == "A test project"
    assert "setup_instructions" in kwargs and "Using Poetry" in kwargs[
        "setup_instructions"]
    assert "usage_instructions" in kwargs and (
        "poetry run python main.py" in kwargs[
            "usage_instructions"])
    assert "testing_instructions" in kwargs and "poetry run pytest" in kwargs[
        "testing_instructions"]
    assert "license_info" in kwargs and "MIT License" in kwargs["license_info"]


def test_generate_readme_without_poetry_and_tests(readme_generator):
    project_info = {
        "name": "test project",
        "description": "A test project",
        "use_poetry": False,
        "create_tests": False,
        "license": "None"
    }

    mock_content = """
# Test Project

A test project

## Setup

### Using pip and venv

pip install -r requirements.txt

## Usage

python main.py

## Contributing

...
"""

    readme_generator._render_template.return_value = mock_content

    readme = readme_generator.generate(project_info).strip()

    assert readme == mock_content.strip()
    readme_generator._render_template.assert_called_once()
    args, kwargs = readme_generator._render_template.call_args
    assert "name" in kwargs and kwargs["name"] == "Test Project"
    assert "description" in kwargs and kwargs[
        "description"] == "A test project"
    assert "setup_instructions" in kwargs and "Using pip and venv" in kwargs[
        "setup_instructions"]
    assert "usage_instructions" in kwargs and "python main.py" in kwargs[
        "usage_instructions"]
    assert "testing_instructions" in kwargs and kwargs[
        "testing_instructions"] == ""
    assert "license_info" in kwargs and kwargs["license_info"] == ""
