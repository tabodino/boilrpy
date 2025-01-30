from boilrpy.file_generators.base_generator import BaseGenerator


class RequirementsGenerator(BaseGenerator):
    """Generate the requirements.txt file."""

    def generate(self, *args, **kwargs) -> str:
        project_info = args[0] if args else {}
        package_map = {
            "pylint": "use_pylint",
            "flask": "use_flask",
            "python-dotenv": "use_flask",
            "pytest": "create_tests",
        }
        packages = [
            pkg for pkg, key in package_map.items() if project_info.get(key, False)
        ]
        return "\n".join(packages)
