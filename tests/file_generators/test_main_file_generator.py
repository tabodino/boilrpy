import pytest
from boilrpy.file_generators.main_file_generator import MainFileGenerator


@pytest.fixture
def main_file_generator():
    return MainFileGenerator(None)


def test_generate_main_file(main_file_generator):
    main_file = main_file_generator.generate()
    assert "def main():" in main_file
    assert "if __name__ == '__main__':" in main_file
    assert "main()" in main_file
