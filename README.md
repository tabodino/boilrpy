# ![Logo](https://wesy.fr/img/logo-no-background.svg)


boilrpy is a Python project automation tool that simplifies the process of creating new Python projects. It generates a standardized project structure, including essential files and configurations, allowing developers to quickly start working on their Python projects.

[![PyPI version](https://badge.fury.io/py/boilrpy.svg)](https://badge.fury.io/py/boilrpy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python->3.10-blue.svg)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)
## Installation

You can install boilrpy directly from PyPI:


```bash
pip install boilrpy
```

## Quick Start

Create a new Python project with boilrpy:

```python
from boilrpy import create_project

create_project(
    name="my_awesome_project",
    version="0.1.0",
    license="MIT",
    use_poetry=True
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

Follow the prompts to configure your project. You'll be asked for:

- Project name
- Version
- License type
- Dependency management preference (Poetry or pip)
- And more...

## Project Structure

boilrpy generates the following project structure:

```
your_project/
├── .gitignore
├── LICENSE
├── README.md
├── Dockerfile (if using Docker)
├── .dockerignore (if using Docker)
├── pyproject.toml (if using Poetry)
├── requirements.txt (if using pip)
├── src/
│   └── your_project/
│       └── __init__.py
└── tests/
    └── __init__.py
```

## Configuration

Boilrpy uses sensible defaults, but you can customize the project creation process by answering the prompts during project creation.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.

## Links

- GitHub: [https://github.com/tabodino/boilrpy](https://github.com/tabodino/boilrpy)
- PyPI: [https://pypi.org/project/boilrpy/](https://pypi.org/project/boilrpy/)

