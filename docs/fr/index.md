# ![Logo](https://wesy.fr/img/logo-no-background.svg)

_A Python development boilerplate generator_

[![PyPI version](https://badge.fury.io/py/boilrpy.svg)](https://pypi.org/project/boilrpy/)
[![GitHub stars](https://img.shields.io/github/stars/tabodino/boilrpy?style=social)](https://github.com/tabodino/boilrpy)

> 🇫🇷 Cette page est en français.  
> 🇬🇧 For the English version, click here: [English](/index.md)

---

## 🚀 Introduction

**Boilrpy** est un outil d’automatisation qui génère une structure de projet Python complète, prête à l’emploi.  
Idéal pour lancer rapidement un projet Python propre, modulaire, et bien documenté.

- [PyPI](https://pypi.org/project/boilrpy/)
- [Sources GitHub](https://github.com/tabodino/boilrpy)

---

## ⚡ Fonctionnalités principales

- Génération rapide de structure de projet Python
- Création automatique des fichiers essentiels : `LICENSE`, `.gitignore`, `README.md`, etc.
- Initialisation facultative d’un dépôt Git (`git init`)
- Gestion des dépendances optimisée (Poetry ou pip)
- Fichiers Docker (`Dockerfile`, `.dockerignore`) si demandé
- Prise en charge de plusieurs types de licences
- Templates pour projet classique ou Flask

---

## 🛠️ Installation

```bash
pip install boilrpy
```

---

## 🚦 Quickstart

**Via la ligne de commande :**

```bash
boilrpy
```

...et laissez-vous guider par les prompts interactifs !

**En Python :**

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

## 📁 Exemple de structure générée

<details>
<summary><b>Projet Python classique</b></summary>

```
your_project/
├── Dockerfile (si demandé)
├── .dockerignore (si demandé)
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml / requirements.txt
├── main.py
└── tests/
└── init.py
```

</details>

<details>
<summary><b>Projet Flask</b></summary>

```
your_project/
├── Dockerfile (si demandé)
├── .dockerignore (si demandé)
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
```

</details>

---

## 🙌 Contribution

Vous souhaitez améliorer boilrpy ou proposer de nouveaux templates ?  
Ouvrez une issue ou une pull request sur [GitHub](https://github.com/tabodino/boilrpy).

---

## 💬 Support

Pour toute question ou suggestion, utilisez l’[issue tracker](https://github.com/tabodino/boilrpy/issues).

---

## 📄 Licence

Ce projet est sous licence MIT.  
Voir le fichier [LICENSE](../../LICENSE) pour le texte complet.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)


