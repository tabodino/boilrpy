from boilrpy.file_generators.base_generator import BaseGenerator


class ChangelogGenerator(BaseGenerator):
    """
    Generator for CHANGELOG.md file.
    """

    def generate(self, *args, **kwargs) -> str:
        """
        Generate the content for CHANGELOG.md file.

        :param version: Version number
        :return: Content of CHANGELOG.md file
        """
        version = args[0] if args else "0.0.1"
        template = """# Changelog

# ${version}

### Added
"""
        return self.render_template(template, version=version)
