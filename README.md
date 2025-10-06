# ![Logo](https://wesy.fr/img/logo-no-background.svg)


BoilrPy is a Python project automation tool that simplifies the process of creating new Python projects. It generates a standardized project structure, including essential files and configurations, allowing developers to quickly start working on their Python projects.

[![PyPI version](https://badge.fury.io/py/boilrpy.svg)](https://badge.fury.io/py/boilrpy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python->3.10-blue.svg)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)
## Installation

You can install BoilrPy directly from PyPI:


```bash
pip install boilrpy
```

## 📦 Dependency Managers

Boilrpy supports multiple Python dependency managers, each with its own strengths:

### Supported Managers

| Manager | Speed | Lock File | Use Case | Installation |
|---------|-------|-----------|----------|--------------|
| **pip** | ⭐⭐⭐ | ❌ | Simple projects, beginners | Pre-installed with Python |
| **poetry** | ⭐⭐ | ✅ | Professional projects, teams | `pipx install poetry` |
| **uv** | ⭐⭐⭐⭐⭐ | ✅ | Modern projects, speed-focused | `pip install uv` |
| **conda** | ⭐ | ❌ | Data science, scientific computing | Download from anaconda.com |

### Quick Comparison

- 🐍 **pip**: Traditional, universal, simple
- 📦 **poetry**: Modern, professional, reproducible
- ⚡ **uv**: Blazingly fast (10-100x faster than pip)
- 🔬 **conda**: Best for data science and non-Python dependencies

For detailed information, see [Dependency Managers Guide](docs/dependencies_manager.md).

## Quick Start

Create a new Python project with boilrpy:

```python
from boilrpy import create_project

create_project(
    name="my_awesome_project",
    version="0.1.0",
    license="MIT",
    dependencies_manager="poetry" # or "pip", "uv", "conda"
)
```

Or use the command-line interface:

```python
boilrpy
```


## Features

- Create a new Python project with a standardized structure
- Generate essential files (LICENSE, .gitignore, README.md, etc.)
- Initialize a Git repository
- Set up dependency management (Poetry or pip)
- Create a Dockerfile and .dockerignore
- Support for multiple license types
- Configurable project 

## Usage

To create a new Python project using the CLI, run:

```python
boilrpy
```

```python
# Check installed dependency managers
boilrpy --check-deps
```

Follow the prompts to configure your project. You'll be asked for:

- Project name
- Version
- License type
- Dependency management preference (Poetry or pip)
- And more...

## Project Structure

boilrpy generates the following project structure:

### Without flask

```
your_project/
├── Dockerfile     (if using Docker)
├── .dockerignore  (if using Docker)
├── .pylintrc      (if using pylint)
├── .gitignore
├── LICENSE
├── README.md
├── CHANGELOG.md
├── pyproject.toml (if using Poetry)
├── poetry.lock    (if using Poetry)
├── requirements.txt
├── main.py        (project entrypoint)
└── tests/
    └── __init__.py
```

### With flask

```
your_project/
├── Dockerfile     (if using Docker)
├── .dockerignore  (if using Docker)
├── .pylintrc      (if using pylint)
├── .gitignore
├── .env
├── LICENSE
├── README.md
├── CHANGELOG.md
├── pyproject.toml (if using Poetry)
├── poetry.lock    (if using Poetry)
├── requirements.txt
├── app.py         (flask entrypoint)
├── static/        (assets folder)
│   └── css/
│   |   └── style.css
│   └── js/
│       └── script.js
├── templates/     (html files)
│   └── base.html
|   └── index.html
└── tests/
    └── __init__.py
```

Run this command to launch server:
```
flask run
```
By default your flask app is accessible at this address: http://127.0.0.1:5000 (see app.py)

This configuration is for development

## Configuration

Boilrpy uses sensible defaults, but you can customize the project creation process by answering the prompts during project creation.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.

## Links

- GitHub: [https://github.com/tabodino/boilrpy](https://github.com/tabodino/boilrpy)
- PyPI: [https://pypi.org/project/boilrpy/](https://pypi.org/project/boilrpy/)

