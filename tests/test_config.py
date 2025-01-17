import pytest
from boilrpy.config import Config


@pytest.fixture
def config():
    return Config


def test_get_available_licenses(config):
    licenses = config().get_available_licenses()
    assert isinstance(licenses, list)
    assert len(licenses) > 0
    assert "MIT" in licenses
    assert "Apache" in licenses
    assert "GPL" in licenses
    assert "BSD" in licenses
    assert "None" in licenses


def test_get_charset(config):
    charset = config().get_charset()
    assert isinstance(charset, str)


def test_get_use_camel_case(config):
    use_camel_case = config().get_use_camel_case()
    assert isinstance(use_camel_case, bool)


def test_get_default_vrsion(config):
    default_version = config().get_default_version()
    assert isinstance(default_version, str)
