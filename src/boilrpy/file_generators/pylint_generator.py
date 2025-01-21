from boilrpy.file_generators.base_generator import BaseGenerator


class PylintGenerator(BaseGenerator):
    """
    Generator for .pylintrc rules
    """

    def generate(self, *args, **kwargs) -> str:
        """
        Generate the content for .pylintrc file.

        :return: Content of .pylintrc file
        """
        return """[MASTER]
disable=missing-module-docstring, too-few-public-methods 
ignore=tests"""
