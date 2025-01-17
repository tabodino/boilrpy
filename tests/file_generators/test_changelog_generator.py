import pytest
from boilrpy.file_generators.changelog_generator import ChangelogGenerator


@pytest.fixture
def changelog_generator():
    return ChangelogGenerator(None)


def test_generate_changelog(changelog_generator):
    version = "1.0.0"
    changelog = changelog_generator.generate(version)
    assert "# Changelog" in changelog
    assert f"# {version}" in changelog
    assert "### Added" in changelog
