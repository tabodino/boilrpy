from boilrpy.file_generators.base_generator import BaseGenerator


class DockerfileGenerator(BaseGenerator):
    """
    Generator for Dockerfile and .dockerignore file.
    """

    def generate(self, *args, **kwargs) -> None:
        project_name = args[0] if args else ""
        use_flask = args[1] if len(args) > 1 else False
        self.generate_dockerfile(project_name, use_flask)
        self.generate_dockerignore()

    def generate_dockerfile(self, project_name: str, use_flask: bool) -> str:
        """Generate Dockerfile content."""
        command = '["flask", "run"]' if use_flask else '["python", "main.py"]'
        template = """FROM python:${python_version}-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ${command}
"""
        return self.render_template(
            template,
            project_name=project_name,
            python_version=self.config.python_version,
            command=command,
        )

    def generate_dockerignore(self) -> str:
        """Generate .dockerignore content."""
        return """__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
"""
