from boilrpy.file_generators.base_generator import BaseGenerator


class DockerfileGenerator(BaseGenerator):
    """
    Generator for Dockerfile and .dockerignore file.
    """

    def generate(self, *args, **kwargs) -> None:
        project_name = args[0] if args else ""
        self.generate_dockerfile(project_name)
        self.generate_dockerignore()

    def generate_dockerfile(self, project_name: str) -> str:
        """ Generate Dockerfile content. """
        template = """FROM python:${python_version}-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
"""
        return self.render_template(
            template,
            project_name=project_name,
            python_version=self.config.python_version,
        )

    def generate_dockerignore(self) -> str:
        """ Generate .dockerignore content. """
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
