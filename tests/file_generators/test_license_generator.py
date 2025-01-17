import pytest
from datetime import datetime
from boilrpy.file_generators.license_generator import (
    LicenseGenerator,
    LicenseStrategy,
    MITLicenseStrategy,
    ApacheLicenseStrategy,
    GPLLicenseStrategy,
    BSDLicenseStrategy,
)


@pytest.fixture
def license_generator():
    return LicenseGenerator(None)


@pytest.fixture
def license_strategy():
    return LicenseStrategy()


def test_get_template_strategy_instanciation(license_strategy):
    with pytest.raises(NotImplementedError):
        license_strategy._get_template()


def test_generate_mit_license(license_generator):
    license_text = license_generator.generate("MIT", "John Doe")
    assert "MIT License" in license_text
    assert f"Copyright (c) {datetime.now().year} John Doe" in license_text
    assert "Permission is hereby granted" in license_text


def test_generate_apache_license(license_generator):
    license_text = license_generator.generate("Apache", "John Doe")
    assert f"Copyright {datetime.now().year} John Doe" in license_text
    assert "Licensed under the Apache License, Version 2.0" in license_text


def test_generate_gpl_license(license_generator):
    license_text = license_generator.generate("GPL", "John Doe")
    assert f"Copyright {datetime.now().year} John Doe" in license_text
    assert "GNU General Public License" in license_text


def test_generate_bsd_license(license_generator):
    license_text = license_generator.generate("BSD", "John Doe")
    assert "BSD License" in license_text
    assert f"Copyright (c) {datetime.now().year} John Doe" in license_text


def test_unknown_license_defaults_to_mit(license_generator):
    license_text = license_generator.generate("Unknown", "John Doe")
    assert "MIT License" in license_text


def test_mit_license_strategy():
    strategy = MITLicenseStrategy()
    license_text = strategy.generate("John Doe")
    assert "MIT License" in license_text
    assert f"Copyright (c) {datetime.now().year} John Doe" in license_text


def test_apache_license_strategy():
    strategy = ApacheLicenseStrategy()
    license_text = strategy.generate("John Doe")
    assert f"Copyright {datetime.now().year} John Doe" in license_text
    assert "Licensed under the Apache License, Version 2.0" in license_text


def test_gpl_license_strategy():
    strategy = GPLLicenseStrategy()
    license_text = strategy.generate("John Doe")
    assert f"Copyright {datetime.now().year} John Doe" in license_text
    assert "GNU General Public License" in license_text

def test_gpl_license_strategy():
    strategy = BSDLicenseStrategy()
    license_text = strategy.generate("John Doe")
    assert "BSD License" in license_text    
