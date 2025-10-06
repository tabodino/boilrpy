from boilrpy.file_generators.base_generator import BaseGenerator


class ReadmeGenerator(BaseGenerator):
    """
    Generator for README.md file.
    """

    DEP_MANAGER_CONFIG = {
        "poetry": {
            "setup": (
                "### Using Poetry\n\n"
                "Install dependencies:\n\n"
                "```bash\n"
                "poetry install\n"
                "```\n\n"
                "Activate the virtual environment:\n\n"
                "```bash\n"
                "poetry env activate\n"
                "```"
            ),
            "run_command": "poetry run python main.py",
            "flask_command": "poetry run flask run",
            "test_command": "poetry run pytest",
        },
        "pip": {
            "setup": (
                "### Using pip and venv\n\n"
                "Create a virtual environment:\n\n"
                "On Linux and macOS:\n\n"
                "```bash\n"
                "python3 -m venv venv\n"
                "```\n\n"
                "On Windows:\n\n"
                "```bash\n"
                "python -m venv venv\n"
                "```\n\n"
                "Activate the virtual environment:\n\n"
                "On Linux and macOS:\n\n"
                "```bash\n"
                "source venv/bin/activate\n"
                "```\n\n"
                "On Windows:\n\n"
                "```bash\n"
                "venv\\Scripts\\activate\n"
                "```\n\n"
                "Install dependencies:\n\n"
                "```bash\n"
                "pip install -r requirements.txt\n"
                "```"
            ),
            "run_command": "python main.py",
            "flask_command": "flask run",
            "test_command": "pytest",
        },
        "uv": {
            "setup": (
                "### Using uv\n\n"
                "Create a virtual environment and install dependencies:\n\n"
                "```bash\n"
                "uv venv\n"
                "```\n\n"
                "Activate the virtual environment:\n\n"
                "On Linux and macOS:\n\n"
                "```bash\n"
                "source .venv/bin/activate\n"
                "```\n\n"
                "On Windows:\n\n"
                "```bash\n"
                ".venv\\Scripts\\activate\n"
                "```\n\n"
                "Install dependencies:\n\n"
                "```bash\n"
                "uv pip install -r requirements.txt\n"
                "```"
            ),
            "run_command": "uv run python main.py",
            "flask_command": "uv run flask run",
            "test_command": "uv run pytest",
        },
        "conda": {
            "setup": (
                "### Using Conda\n\n"
                "Create a conda environment:\n\n"
                "```bash\n"
                "conda create -n myproject python=3.11\n"
                "```\n\n"
                "Activate the environment:\n\n"
                "```bash\n"
                "conda activate myproject\n"
                "```\n\n"
                "Install dependencies:\n\n"
                "```bash\n"
                "conda install --file requirements.txt\n"
                "```"
            ),
            "run_command": "python main.py",
            "flask_command": "flask run",
            "test_command": "pytest",
        },
    }

    def generate(self, *args, **kwargs) -> str:
        """
        Generate the content for README.md file.

        :param project_info: Dictionary containing project information
        :param kwargs: Additional keyword arguments
        :return: Content of README.md file
        """
        project_info = args[0] if args else {}

        dep_manager = project_info.get("dependencies_manager", "pip").lower()
        manager_config = self.DEP_MANAGER_CONFIG.get(
            dep_manager,
            self.DEP_MANAGER_CONFIG["pip"],  # Fallback on pip if unknown
        )

        setup_instructions = manager_config["setup"]

        if project_info.get("use_flask"):
            usage_instructions = manager_config["flask_command"]
        else:
            usage_instructions = manager_config["run_command"]

        testing_instructions = ""
        if project_info.get("create_tests"):
            testing_instructions = (
                f"\n## Testing\n\n```bash\n{manager_config['test_command']}\n```"
            )

        pylint_instructions = ""
        if project_info.get("use_pylint"):
            pylint_instructions = "\n## Pylint\n\n```bash\npylint .\n```"

        license_info = ""
        if project_info.get("license") and project_info["license"] != "None":
            license_info = (
                f"\n## License\n\nThis project is licensed under the "
                f"{project_info['license']} License."
            )

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
