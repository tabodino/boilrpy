"""
Dependency Creators Module

This module provides creators for different Python dependency managers.
Each creator implements the BaseDependencyCreator interface and handles
the specifics of setting up projects with that dependency manager.

Available Creators:
    - PoetryCreator: For Poetry (professional projects)
    - PipCreator: For pip (simple projects)
    - UvCreator: For uv (fast modern projects)
    - CondaCreator: For Conda (data science projects)

Example:
    >>> from boilrpy.dependency_creators import DependencyCreatorFactory
    >>> from boilrpy.config import Config
    >>>
    >>> config = Config()
    >>> creator = DependencyCreatorFactory.create("poetry", config)
    >>> creator.create_dependency_file(project_info)
"""

# Base classes and exceptions
from boilrpy.dependency_creators.base_dependency_creator import (
    BaseDependencyCreator,
    DependencyCreatorNotFoundError,
    DependencyCreatorError,
)

# Concrete creators
from boilrpy.dependency_creators.poetry_creator import PoetryCreator
from boilrpy.dependency_creators.pip_creator import PipCreator
from boilrpy.dependency_creators.uv_creator import UvCreator
from boilrpy.dependency_creators.conda_creator import CondaCreator

# Factory
from boilrpy.dependency_creators.factory import DependencyCreatorFactory

# Utilities
from boilrpy.dependency_creators.checker import DependencyManagerChecker

# Public API
__all__ = [
    # Base
    "BaseDependencyCreator",
    "DependencyCreatorNotFoundError",
    "DependencyCreatorError",
    # Creators
    "PoetryCreator",
    "PipCreator",
    "UvCreator",
    "CondaCreator",
    # Factory
    "DependencyCreatorFactory",
    # Utilities
    "DependencyManagerChecker",
]
