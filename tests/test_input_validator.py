import pytest
from boilrpy.input_validator import InputValidator


@pytest.mark.parametrize("name, use_camel_case, expected", [
    ("ValidName", True, True),
    ("valid_name", False, True),
    ("invalid name", True, True),
    ("invalid name", False, True),
    ("123InvalidName", True, True),
    ("123_invalid_name", False, True),
    ("", True, False),
    ("", False, False),
])
def test_validate_project_name(name, use_camel_case, expected):
    assert InputValidator.validate_project_name(name) == expected


@pytest.mark.parametrize("version, expected", [
    ("1.0.0", True),
    ("0.1.0", True),
    ("1.0", False),
    ("1.0.0.0", False),
    ("v1.0.0", False),
    ("1.0.0-alpha", True),
    (" 1.0.0-alpha.1", False),
    ("1.0.0-alpha.beta", False),
    ("1.0.0-alpha.beta", False),
    ("1.0.0-beta", True),
    ("1.0.0-beta", True),
    ("1.0.0-beta.11", False),
    ("1.0.0-rc.1", False),
    ("", True),
])
def test_validate_version(version, expected):
    assert InputValidator.validate_version(version) == expected
