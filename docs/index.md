# ![Logo](https://wesy.fr/img/logo-no-background.svg)

_A Python development boilerplate generator_

[![PyPI version](https://badge.fury.io/py/boilrpy.svg)](https://pypi.org/project/boilrpy/)
[![GitHub stars](https://img.shields.io/github/stars/tabodino/boilrpy?style=social)](https://github.com/tabodino/boilrpy)

> 🇬🇧 This page is in English.  
> 🇫🇷 Pour la version française, cliquez ici : [Français](fr/index.md)

---
## 🚀 Introduction

**Boilrpy** is an automation tool that generates a complete Python project structure, ready to use.  
Perfect for starting new Python projects quickly, with a clean modular design and full documentation.

- [PyPI](https://pypi.org/project/boilrpy/)
- [Code source](https://github.com/tabodino/boilrpy)

---

## ⚡ Main Features

- Rapid generation of Python project structure
- Automatic creation of essential files: `LICENSE`, `.gitignore`, `README.md`, etc.
- Optional git repository initialization (`git init`)
- Dependency management (Poetry or pip)
- Docker files (`Dockerfile`, `.dockerignore`) if requested
- Support for multiple license types
- Templates for classic Python or Flask projects

---

## 🛠️ Installation

```bash
pip install boilrpy
```

---

## 🚦 Quickstart

**Command-line:**

```bash
boilrpy
```
...follow the interactive prompts!

**Python code:**

```bash
from boilrpy import create_project

create_project(
  name="my_awesome_project",
  version="0.1.0",
  license="MIT",
  use_poetry=True
)
```

---

## 📁 Example Generated Structure

<details>
<summary><b>Classic Python project</b></summary>

<pre>
your_project/
├── Dockerfile (if requested)
├── .dockerignore (if requested)
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml / requirements.txt
├── main.py
└── tests/
└── init.py
</pre>

</details>

<details>
<summary><b>Flask project</b></summary>

<pre>
your_project/
├── Dockerfile (if requested)
├── .dockerignore (if requested)
├── .gitignore
├── .env
├── LICENSE
├── README.md
├── pyproject.toml / requirements.txt
├── app.py
├── static/
│ ├── css/
│ └── js/
├── templates/
│ └── base.html
│ └── index.html
└── tests/
└── init.py
</pre>

</details>

---

## 🎥 Demo

[See demo on video](https://tabodino.github.io/boilrpy/docs/assets/demo-boirlpy.mp4)


---

## 🙌 Contributing

Want to improve boilrpy or suggest new templates? Open an issue or pull request on [GitHub](https://github.com/tabodino/boilrpy).

---

## 💬 Support

For questions or suggestions, use the [issue tracker](https://github.com/tabodino/boilrpy/issues).

---

## 📄 License

This project is licensed under the MIT License.  
See the [LICENSE](../LICENSE) file for details.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
