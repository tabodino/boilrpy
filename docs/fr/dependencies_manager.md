# 🧰 Guide des gestionnaires de dépendances

Boilrpy prend en charge plusieurs gestionnaires de dépendances Python. Ce guide vous aidera à choisir et installer celui qui convient le mieux à votre projet.

---

## 📦 Gestionnaires pris en charge

### 1. pip (par défaut)

**Idéal pour** : Projets simples, débutants, configuration minimale  
**Installation** : Inclus par défaut avec Python

**Avantages** :
- ✅ Préinstallé avec Python  
- ✅ Facile à utiliser  
- ✅Support universel  

**Inconvénients** :
- ❌ Pas de gestion automatique des environnements virtuels  
- ❌ Pas de fichier de verrouillage pour des builds reproductibles  
- ❌ Résolution manuelle des dépendances  

**💻 Utilisation** :
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

### 2. Poetry

**Idéal pour** : Projets professionnels, travail en équipe, publication de packages 

**Installation** :
```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -

# Alternative : via pipx
pipx install poetry
```

**Avantages** :
- ✅ Gestion automatique des environnements virtuels
- ✅ Fichier de verrouillage (poetry.lock) pour la reproductibilité
- ✅ Publication de packages intégrée
- ✅ Résolution des dépendances intégrée

**Inconvénients** :
- ❌ Plus lent que pip
- ❌ Courbe d’apprentissage
- ❌ Installation supplémentaire requise

**Utilisation** :

```bash
poetry install
poetry env activate
poetry run python main.py
```

---

### 3. uv (⚡ Le plus rapide)

**Idéal pour** : Projets modernes, workflows axés sur la rapidité.

**Installation** :

```bash
# Avec pip
pip install uv

# Avec pipx (recommandé)
pipx install uv

# Avec cargo (Rust)
cargo install --git https://github.com/astral-sh/uv uv

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS (curl)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Avantages** :

- ✅ Extrêmement rapide (10 à 100x plus rapide que pip)
- ✅ Écrit en Rust
- ✅ Remplacement direct de pip
- ✅ Moderne et activement maintenu

**Inconvénients** :

- ❌ Relativement nouveau
- ❌ Installation séparée requise

**Utilisation** :

```bash
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
uv pip install -r requirements.txt
```

---

### 4. Conda

**Idéal pour** : Science des données, calcul scientifique, dépendances non Python 

**Installation** : 

Téléchargez Anaconda ou Miniconda :

- Anaconda: https://www.anaconda.com/download
- Miniconda: https://docs.conda.io/en/latest/miniconda.html

**Avantages** :
- ✅ Gestion de packages multi-langages
- ✅ Binaires précompilés pour les packages scientifiques
- ✅ Excellent pour la data science
- ✅ Gestion d’environnement intégrée

**Inconvénients** :
- ❌ Résolution des dépendances lente
- ❌ Taille d’installation importante
- ❌ Risque de conflit avec le Python système

**Utilisation** :

```bash
conda env create -f environment.yml
conda activate myproject
```

---

## Comparaison rapide

| Feature                    | pip | poetry | uv | conda |
|----------------------------|-----|--------|-------|-------|
| Vitesse                    | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| Fichier de verrouillage    | ❌ | ✅ | ✅ | ❌ |
| Gestion des environnements | Manuelle | Auto | Manuelle | Auto |
| Courbe d’apprentissage     | Facile | Moyenne | Facile | Moyenne |
| Taille d’installation      | Petite | Petite | Petite | Grande |
| Préinstallé                | ✅ | ❌ | ❌ | ❌ |

---

## Vérification de l’installation

```bash
pip --version
poetry --version
uv --version
conda --version
```

---

## Dépannage

### Erreurs "commande introuvable"

**pip**
- Vérifiez que Python est installé et dans le PATH
- Essayez `python -m pip` au lieu de `pip`

**Poetry**
- Redémarrez le terminal après installation
- Vérifiez que le dossier bin de Poetry est dans le PATH

**uv**
- Redémarrez le terminal
- Sous Windows, ajoutez manuellement au PATH si nécessaire

**Conda**
- Redémarrez le terminal
- Sourcez le script d’initialisation de conda

### Erreurs de permission

**Linux/macOS** :
```bash
pip install --user uv
```

**Windows** :
- Exécutez le terminal en tant qu’administrateur (non recommandé)
- Ou utilisez des environnements virtuels

---

## Changer de gestionnaire

### De pip vers Poetry
```bash
poetry init
poetry add $(cat requirements.txt | grep -v '^#' | grep -v '^$')
```

### De Poetry vers pip
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### De pip vers uv
```bash
uv pip install -r requirements.txt
```

---

## Recommandations

- 🚀 **Pour la vitesse** : utilisez uv
- 📦 **Pour publier des packages** : utilisez Poetry
- 🎓 **Pour apprendre Python** : utilisez pip
- 🔬 **Pour la data science** : utilisez Conda
- 🏢 **Pour les projets d’entreprise** : utilisez Poetry ou uv

---

## Besoin d’aide

En cas de problème :

1. Consultez la documentation officielle
2. Vérifiez l’installation avec `--version`
3. Réinstallez le gestionnaire si nécessaire
4. Utilisez pip comme solution de secours (toujours disponible)

Pour les problèmes spécifiques à Boilrpy, ouvrez un ticket sur GitHub.