# Changelog

## [0.8.0] - 2025-10-06

### ✨ Added
- Added Ruff as an optional linting tool
- **Multi-Dependency Manager Support**: Added support for multiple Python dependency managers
  - `pip`: Traditional Python package installer with venv
  - `poetry`: Modern dependency management with lock files
  - `uv`: Ultra-fast Python package installer (10-100x faster than pip)
  - `conda`: Cross-platform package manager for data science
- **Dependency Manager Checker**: Added utility to detect installed dependency managers
  - `DependencyManagerChecker`: Check which managers are available on the system
  - CLI integration with `--check-deps` flag to verify installations
  - Automatic fallback to pip when selected manager is not available

### 🔄 Changes
- **Refactored Dependency Management**:
  - Replaced `use_poetry` boolean with `dependencies_manager` string for flexibility
  - Centralized requirements file writing in `BaseDependencyCreator._write_requirements_files()`
  - Removed code duplication between pip and uv creators
  - Improved error handling with custom exceptions (`DependencyCreatorNotFoundError`, `DependencyCreatorError`)
  - Better separation of concerns with abstract base class
- **Improved Project Creator**:
  - Updated `ProjectCreator` to use new dependency creator system
  - Automatic fallback mechanism when selected manager is unavailable

## [0.7.0] - 2025-02-01

### 🚀 Stable release
- Version 0.7.0-beta1 promoted to 0.7.0 with no functional changes.
- Removed -beta1 suffix for official release via pip install boilrpy.

## [0.7.0-beta1] - 2025-02-01

### ✨ Added
- Add virtual environment instructions on readme text generator 

### 🔄 Changes
- Improve project snake case name formatting regex
- Replace capitalize text in flask templates

## [0.7.0-beta] - 2025-01-31

### 🔄 Changes 
- Improve project name formatting for poetry version >= 2.x

### ⚠️ Notes  
- This is a **beta release** and may contain bugs.  

## [0.6.2] - 2025-01-31
### 🔧 Fixed
- Handle new major version of poetry pyproject.toml
- Handle no git installed on OS
- Handle no poetry package found

## [0.6.1] - 2025-01-30
### 🔧 Fixed
- Error autoformat string with black

## [0.6.0] - 2025-01-28
### ✨ Added
- Add flask generation templates and structure
- Separate poetry generation in a dedicated concern

## [0.5.0] - 2025-01-21
### ✨ Added
- Add pylint generation file
- Upate file generator script with Factory pattern

## [0.4.0] - 2025-01-19
### ✨ Added
- Add color in CLI

## [0.3.2] - 2025-01-17
### 🔧 Fixed
- Remove debug print method 

## [0.3.1] - 2025-01-17
### 🔧 Fixed
- Fix path on generate Dockerfile

## [0.3.0] - 2025-01-13
### ✨ Added
- Handle BSD license
- Generate docker files
- Update README.md

## [0.2.0] - 2025-01-06
### ✨ Added
- Separate file writer concerns
- Add a config default version

## [0.1.0] - 2024-12-31
### ✨ Added
- Generate python project folder
- Prepare a development environment for python.
- Handle pip and poetry dependencies