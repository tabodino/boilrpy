from boilrpy.file_generators.base_generator import BaseGenerator


class MainFileGenerator(BaseGenerator):
    """
    Generator for main.py file.
    """

    def generate(self, *args, **kwargs) -> str:
        """
        Generate the content for main.py file.

        :return: Content of main.py file
        """
        return """def main():
    pass


if __name__ == '__main__':
    main()
"""
