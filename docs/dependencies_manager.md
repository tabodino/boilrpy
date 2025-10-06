# Dependency Managers Guide

Boilrpy supports multiple Python dependency managers. This guide will help you choose and install the right one for your project.

## Supported Dependency Managers

### 1. pip (Default)
**Best for**: Simple projects, beginners, minimal setup

**Installation**: Comes with Python by default

**Pros**:
- ✅ Pre-installed with Python
- ✅ Simple to use
- ✅ Universal support

**Cons**:
- ❌ No automatic virtual environment management
- ❌ No lock file for reproducible builds
- ❌ Manual dependency resolution

**Usage**:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
\`\`\`

---

### 2. Poetry
**Best for**: Professional projects, teams, package publishing

**Installation**:
\`\`\`bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -

# Alternative: using pipx
pipx install poetry
\`\`\`

**Pros**:
- ✅ Automatic virtual environment management
- ✅ Lock file (poetry.lock) for reproducibility
- ✅ Built-in package publishing
- ✅ Dependency resolver

**Cons**:
- ❌ Slower than pip
- ❌ Learning curve
- ❌ Additional installation required

**Usage**:
\`\`\`bash
poetry install
poetry shell
poetry run python main.py
\`\`\`

---

### 3. uv (⚡ Fastest)
**Best for**: Modern projects, speed-focused workflows, developers who want fast installs

**Installation**:
\`\`\`bash
# Using pip
pip install uv

# Using pipx (recommended)
pipx install uv

# Using cargo (Rust)
cargo install --git https://github.com/astral-sh/uv uv

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS (curl)
curl -LsSf https://astral.sh/uv/install.sh | sh
\`\`\`

**Pros**:
- ✅ **Extremely fast** (10-100x faster than pip)
- ✅ Written in Rust
- ✅ Drop-in replacement for pip
- ✅ Modern and actively maintained

**Cons**:
- ❌ Relatively new (less ecosystem maturity)
- ❌ Requires separate installation

**Usage**:
\`\`\`bash
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
uv pip install -r requirements.txt
\`\`\`

---

### 4. Conda
**Best for**: Data science, scientific computing, non-Python dependencies

**Installation**:
Download Anaconda or Miniconda from:
- Anaconda: https://www.anaconda.com/download
- Miniconda: https://docs.conda.io/en/latest/miniconda.html

**Pros**:
- ✅ Cross-language package management
- ✅ Pre-built binaries for scientific packages
- ✅ Excellent for data science
- ✅ Built-in environment management

**Cons**:
- ❌ Slow dependency resolution
- ❌ Large installation size
- ❌ Can conflict with system Python

**Usage**:
\`\`\`bash
conda env create -f environment.yml
conda activate myproject
\`\`\`

---

## Quick Comparison

| Feature                | pip | poetry | uv | conda |
|------------------------|-----|--------|-------|-------|
| Speed                  | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| Lock File              | ❌ | ✅ | ✅ | ❌ |
| Virtual Env Management | Manual | Auto | Manual | Auto |
| Learning Curve         | Easy | Medium | Easy | Medium |
| Install Size           | Small | Small | Small | Large |
| Pre-installed          | ✅ | ❌ | ❌ | ❌ |

---

## Installation Verification

After installing a dependency manager, verify it's working:

### pip
\`\`\`bash
pip --version
\`\`\`

### Poetry
\`\`\`bash
poetry --version
\`\`\`

### uv
\`\`\`bash
uv --version
\`\`\`

### Conda
\`\`\`bash
conda --version
\`\`\`

---

## Troubleshooting

### "Command not found" errors

**For pip**:
- Ensure Python is installed and added to PATH
- Try `python -m pip` instead of `pip`

**For Poetry**:
- Restart your terminal after installation
- Check if Poetry's bin directory is in PATH

**For uv**:
- Restart your terminal after installation
- On Windows, you may need to add to PATH manually

**For Conda**:
- Restart your terminal after installation
- Source the conda initialization script

### Permission errors

**Linux/macOS**:
\`\`\`bash
# Use --user flag or virtual environment
pip install --user uv
\`\`\`

**Windows**:
- Run terminal as Administrator (not recommended)
- Or use virtual environments

---

## Switching Dependency Managers

You can convert between dependency managers:

### From pip to Poetry
\`\`\`bash
poetry init
# Answer the prompts, then:
poetry add $(cat requirements.txt | grep -v '^#' | grep -v '^$')
\`\`\`

### From Poetry to pip
\`\`\`bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
\`\`\`

### From pip to uv
\`\`\`bash
# uv is compatible with pip, just use uv instead
uv pip install -r requirements.txt
\`\`\`

---

## Recommendations

- 🚀 **For speed**: Use **uv**
- 📦 **For publishing packages**: Use **Poetry**
- 🎓 **For learning Python**: Use **pip**
- 🔬 **For data science**: Use **Conda**
- 🏢 **For enterprise projects**: Use **Poetry** or **uv**

---

## Getting Help

If you encounter issues with dependency managers:

1. Check the official documentation
2. Verify installation with `--version` command
3. Try reinstalling the dependency manager
4. Use pip as a fallback (it's always available)

For Boilrpy-specific issues, please open an issue on GitHub.
