from boilrpy.file_generators.base_generator import BaseGenerator


class GitignoreGenerator(BaseGenerator):
    """
    Generator for .gitignore file.
    """

    def generate(self, *args, **kwargs) -> str:
        """
        Generate the content for .gitignore file.

        :return: Content of .gitignore file
        """
        return """# Python
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
.env
.venv
env/

# Poetry
.poetry/
poetry.lock

# PyCharm
.idea/

# VS Code
.vscode/

# Jupyter Notebook
.ipynb_checkpoints

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Pytest
.pytest_cache/

# Coverage reports
htmlcov/
.coverage
.coverage.*
.cache

# Matplotlib
*.png

# macOS
.DS_Store

# Windows
Thumbs.db

# Output folder
output/
"""
