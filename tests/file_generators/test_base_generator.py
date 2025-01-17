from abc import ABC
import pytest
from boilrpy.file_generators.base_generator import BaseGenerator


class TestBaseGenerator:
    class ConcreteGenerator(BaseGenerator):

        def generate(self, *args, **kwargs):
            return "Test content"

    @pytest.fixture
    def generator(self):
        return self.ConcreteGenerator(None)

    def test_abstract_class_instantiation(self):
        with pytest.raises(TypeError):
            BaseGenerator(ABC)

        assert BaseGenerator.generate(None) is None

    def test_render_template(self, generator):
        template = "Hello, ${name}!"
        result = generator.render_template(template, name="World")
        assert result == "Hello, World!"

    def test_generate_method(self, generator):
        result = generator.generate()
        assert result == "Test content"
