from boilrpy.file_generators.base_generator import BaseGenerator


class ReadmeGenerator(BaseGenerator):
    """
    Generator for README.md file.
    """

    def generate(self, *args, **kwargs) -> str:
        """
        Generate the content for README.md file.

        :param project_info: Dictionary containing project information
        :param kwargs: Additional keyword arguments
        :return: Content of README.md file
        """
        project_info = args[0] if args else {}
        template = """
# ${name}

${description}

## Setup

${setup_instructions}

## Usage

To run the project, use the following comand:

${usage_instructions}

${testing_instructions}

${pylint_instructions}

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Create a new Pull Request

${license_info}
"""
        setup_instructions = (
            "### Using Poetry\n\n```poetry install```"
            if project_info["use_poetry"]
            else "### Using pip and venv\n\npip install -r requirements.txt"
        )
        usage_instructions = (
            "```flask run```"
            if project_info.get("use_flask")
            else "```poetry run python main.py```"
            if project_info.get("use_poetry")
            else "```python main.py```"
        )
        testing_instructions = (
            "\n## Testing\n\n```poetry run pytest```"
            if project_info["create_tests"] and project_info["use_poetry"]
            else "\n## Testing\n\n```pytest```" if project_info["create_tests"] else ""
        )
        pylint_instructions = (
            "\n## Pylint\n\n```pylint .```" if project_info["use_pylint"] else ""
        )
        license_info = (
            f"\n## License\n\nThis project is licensed under the "
            f"{project_info['license']} License."
            if project_info["license"] != "None"
            else ""
        )
        return self.render_template(
            template,
            name=project_info["name"].title(),
            description=project_info["description"],
            setup_instructions=setup_instructions,
            usage_instructions=usage_instructions,
            testing_instructions=testing_instructions,
            pylint_instructions=pylint_instructions,
            license_info=license_info,
        ).lstrip()
