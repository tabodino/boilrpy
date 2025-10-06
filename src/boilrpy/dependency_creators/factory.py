"""Factory for creating dependency manager creators."""

from typing import Type
from boilrpy.dependency_creators.base_dependency_creator import BaseDependencyCreator
from boilrpy.dependency_creators.poetry_creator import PoetryCreator
from boilrpy.dependency_creators.pip_creator import PipCreator
from boilrpy.dependency_creators.uv_creator import UvCreator
from boilrpy.dependency_creators.conda_creator import CondaCreator


class DependencyCreatorFactory:
    """Factory to create the appropriate dependency creator.

    This factory uses the Strategy pattern to instantiate the correct
    dependency creator based on the user's choice.

    Example:
        >>> factory = DependencyCreatorFactory()
        >>> creator = factory.create("poetry", config)
        >>> creator.create_dependency_file(project_info)
    """

    # Registry of available creators
    _creators: dict[str, Type[BaseDependencyCreator]] = {
        "poetry": PoetryCreator,
        "pip": PipCreator,
        "uv": UvCreator,
        "conda": CondaCreator,
    }

    @classmethod
    def create(cls, dep_manager: str, config) -> BaseDependencyCreator:
        """Create a dependency creator instance.

        Args:
            dep_manager: Name of the dependency manager (case-insensitive)
            config: Configuration object

        Returns:
            Instance of the appropriate dependency creator

        Raises:
            ValueError: If dependency manager is not supported

        Example:
            >>> creator = DependencyCreatorFactory.create("poetry", config)
            >>> isinstance(creator, PoetryCreator)
            True
        """
        dep_manager = dep_manager.lower()
        creator_class = cls._creators.get(dep_manager)

        if creator_class is None:
            supported = ", ".join(cls.get_supported_managers())
            raise ValueError(
                f"Unsupported dependency manager: '{dep_manager}'. "
                f"Supported managers: {supported}"
            )

        return creator_class(config)

    @classmethod
    def get_supported_managers(cls) -> list[str]:
        """Get list of supported dependency managers.

        Returns:
            Sorted list of supported dependency manager names

        Example:
            >>> managers = DependencyCreatorFactory.get_supported_managers()
            >>> "poetry" in managers
            True
        """
        return sorted(cls._creators.keys())

    @classmethod
    def register_creator(
        cls, name: str, creator_class: Type[BaseDependencyCreator]
    ) -> None:
        """Register a new dependency creator.

        This allows for dynamic registration of new creators without
        modifying the factory class.

        Args:
            name: Name of the dependency manager
            creator_class: Class of the creator (must inherit from BaseDependencyCreator)

        Raises:
            TypeError: If creator_class doesn't inherit from BaseDependencyCreator

        Example:
            >>> class PipenvCreator(BaseDependencyCreator):
            ...     pass
            >>> DependencyCreatorFactory.register_creator("pipenv", PipenvCreator)
        """
        if not issubclass(creator_class, BaseDependencyCreator):
            raise TypeError(
                f"{creator_class.__name__} must inherit from BaseDependencyCreator"
            )
        cls._creators[name.lower()] = creator_class

    @classmethod
    def is_supported(cls, dep_manager: str) -> bool:
        """Check if a dependency manager is supported.

        Args:
            dep_manager: Name of the dependency manager

        Returns:
            True if supported, False otherwise

        Example:
            >>> DependencyCreatorFactory.is_supported("poetry")
            True
            >>> DependencyCreatorFactory.is_supported("unknown")
            False
        """
        return dep_manager.lower() in cls._creators
