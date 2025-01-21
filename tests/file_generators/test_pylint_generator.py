import pytest
from boilrpy.file_generators.pylint_generator import PylintGenerator


@pytest.fixture
def pylint_generator():
    return PylintGenerator(None)

def test_generate(pylint_generator):
    result = pylint_generator.generate()
    assert result == "[MASTER]\ndisable=missing-module-docstring, too-few-public-methods \nignore=tests"