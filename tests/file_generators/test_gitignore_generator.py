import pytest
from boilrpy.file_generators.gitignore_generator import GitignoreGenerator


@pytest.fixture
def gitignore_generator():
    return GitignoreGenerator(None)


def test_gitignore_generator(gitignore_generator):
    gitignore = gitignore_generator.generate()
    assert isinstance(gitignore, str)
    assert "# Python" in gitignore
    assert "# Virtual environments" in gitignore
    assert "# Poetry" in gitignore
    assert "# PyCharm" in gitignore
    assert "# VS Code" in gitignore
    assert "# Jupyter Notebook" in gitignore
    assert "# Distribution / packaging" in gitignore
    assert "# Pytest" in gitignore
    assert "# Coverage reports" in gitignore
    assert "# Matplotlib" in gitignore
    assert "# macOS" in gitignore
    assert "# Windows" in gitignore
    assert "# Output folder" in gitignore
