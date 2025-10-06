"""Tests for BaseDependencyCreator."""

import pytest
from abc import ABC
from unittest.mock import MagicMock
from boilrpy.config import Config
from boilrpy.dependency_creators.base_dependency_creator import (
    BaseDependencyCreator,
    DependencyCreatorNotFoundError,
    DependencyCreatorError
)

@pytest.fixture
def mock_config():
    """Create a mock Config object."""
    config = MagicMock(spec=Config)
    config.get_charset.return_value = "utf-8"
    config.get_available_licenses.return_value = [
        "MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "None"
    ]
    return config


class ConcreteDependencyCreator(BaseDependencyCreator):
    """Concrete implementation for testing abstract base class."""
    
    def create_dependency_file(self, project_info: dict) -> None:
        """Implement abstract method."""
        pass
    
    def install_dependencies(self, packages: list, dev_packages: list) -> None:
        """Implement abstract method."""
        pass


class MinimalConcreteDependencyCreator(BaseDependencyCreator):
    """Minimal concrete implementation that actually calls the methods."""
    
    def create_dependency_file(self, project_info: dict) -> None:
        """Implement abstract method with actual logic."""
        packages, dev_packages = self._create_packages(project_info)
        self.install_dependencies(packages, dev_packages)
    
    def install_dependencies(self, packages: list, dev_packages: list) -> None:
        """Implement abstract method with actual logic."""
        # Just store for testing
        self.installed_packages = packages
        self.installed_dev_packages = dev_packages


class TestBaseDependencyCreator:
    """Tests for BaseDependencyCreator abstract class."""
    
    def test_cannot_instantiate_abstract_class(self, mock_config):
        """Test that BaseDependencyCreator cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseDependencyCreator(mock_config)
    
    def test_concrete_class_can_be_instantiated(self, mock_config):
        """Test that concrete implementation can be instantiated."""
        creator = ConcreteDependencyCreator(mock_config)
        assert creator is not None
        assert creator.config == mock_config
        assert creator.charset == "utf-8"

    def test_abstract_methods_are_called(self, mock_config):
        """Test that abstract methods can be called on concrete implementations."""
        creator = MinimalConcreteDependencyCreator(mock_config)
        
        project_info = {
            "create_tests": True,
            "use_pylint": True,
            "use_flask": True,
            "libraries": ["requests"]
        }
        
        # Call create_dependency_file which calls install_dependencies internally
        creator.create_dependency_file(project_info)
        
        # Verify the methods were called and worked
        assert hasattr(creator, 'installed_packages')
        assert hasattr(creator, 'installed_dev_packages')
        assert "flask" in creator.installed_packages
        assert "python-dotenv" in creator.installed_packages
        assert "requests" in creator.installed_packages
        assert "pytest" in creator.installed_dev_packages
        assert "pylint" in creator.installed_dev_packages
    
    def test_abstract_method_create_dependency_file_signature(self, mock_config):
        """Test create_dependency_file method signature and call."""
        creator = ConcreteDependencyCreator(mock_config)
        project_info = {"name": "test"}
        
        # Should not raise an error (even though it does nothing)
        result = creator.create_dependency_file(project_info)
        assert result is None
    
    def test_abstract_method_install_dependencies_signature(self, mock_config):
        """Test install_dependencies method signature and call."""
        creator = ConcreteDependencyCreator(mock_config)
        packages = ["flask"]
        dev_packages = ["pytest"]
        
        # Should not raise an error (even though it does nothing)
        result = creator.install_dependencies(packages, dev_packages)
        assert result is None
    
    def test_create_packages_no_features(self, mock_config):
        """Test _create_packages with no features enabled."""
        creator = ConcreteDependencyCreator(mock_config)
        project_info = {
            "create_tests": False,
            "use_pylint": False,
            "use_flask": False,
            "libraries": []
        }
        
        packages, dev_packages = creator._create_packages(project_info)
        
        assert packages == []
        assert dev_packages == []
    
    def test_create_packages_with_tests(self, mock_config):
        """Test _create_packages with tests enabled."""
        creator = ConcreteDependencyCreator(mock_config)
        project_info = {
            "create_tests": True,
            "use_pylint": False,
            "use_flask": False,
            "libraries": []
        }
        
        packages, dev_packages = creator._create_packages(project_info)
        
        assert packages == []
        assert dev_packages == ["pytest"]
    
    def test_create_packages_with_pylint(self, mock_config):
        """Test _create_packages with pylint enabled."""
        creator = ConcreteDependencyCreator(mock_config)
        project_info = {
            "create_tests": False,
            "use_pylint": True,
            "use_flask": False,
            "libraries": []
        }
        
        packages, dev_packages = creator._create_packages(project_info)
        
        assert packages == []
        assert dev_packages == ["pylint"]
    
    def test_create_packages_with_tests_and_pylint(self, mock_config):
        """Test _create_packages with both tests and pylint."""
        creator = ConcreteDependencyCreator(mock_config)
        project_info = {
            "create_tests": True,
            "use_pylint": True,
            "use_flask": False,
            "libraries": []
        }
        
        packages, dev_packages = creator._create_packages(project_info)
        
        assert packages == []
        assert dev_packages == ["pytest", "pylint"]
    
    def test_create_packages_with_flask(self, mock_config):
        """Test _create_packages with Flask enabled."""
        creator = ConcreteDependencyCreator(mock_config)
        project_info = {
            "create_tests": False,
            "use_pylint": False,
            "use_flask": True,
            "libraries": []
        }
        
        packages, dev_packages = creator._create_packages(project_info)
        
        assert "flask" in packages
        assert "python-dotenv" in packages
        assert dev_packages == []
    
    def test_create_packages_with_additional_libraries(self, mock_config):
        """Test _create_packages with additional libraries."""
        creator = ConcreteDependencyCreator(mock_config)
        project_info = {
            "create_tests": False,
            "use_pylint": False,
            "use_flask": False,
            "libraries": ["requests", "pandas", "numpy"]
        }
        
        packages, dev_packages = creator._create_packages(project_info)
        
        assert "requests" in packages
        assert "pandas" in packages
        assert "numpy" in packages
        assert dev_packages == []
    
    def test_create_packages_all_features(self, mock_config):
        """Test _create_packages with all features enabled."""
        creator = ConcreteDependencyCreator(mock_config)
        project_info = {
            "create_tests": True,
            "use_pylint": True,
            "use_flask": True,
            "libraries": ["requests", "pandas"]
        }
        
        packages, dev_packages = creator._create_packages(project_info)
        
        assert "flask" in packages
        assert "python-dotenv" in packages
        assert "requests" in packages
        assert "pandas" in packages
        assert "pytest" in dev_packages
        assert "pylint" in dev_packages
    
    def test_create_packages_with_get_method(self, mock_config):
        """Test _create_packages uses .get() for optional keys."""
        creator = ConcreteDependencyCreator(mock_config)
        # Missing keys should default to False/empty
        project_info = {}
        
        packages, dev_packages = creator._create_packages(project_info)
        
        assert packages == []
        assert dev_packages == []


class TestDependencyCreatorExceptions:
    """Tests for custom exceptions."""
    
    def test_dependency_creator_not_found_error(self):
        """Test DependencyCreatorNotFoundError."""
        error = DependencyCreatorNotFoundError("Manager not found")
        assert str(error) == "Manager not found"
        assert isinstance(error, Exception)
    
    def test_dependency_creator_error(self):
        """Test DependencyCreatorError."""
        error = DependencyCreatorError("Operation failed")
        assert str(error) == "Operation failed"
        assert isinstance(error, Exception)
    
    def test_exceptions_can_be_raised_and_caught(self):
        """Test that exceptions can be raised and caught properly."""
        with pytest.raises(DependencyCreatorNotFoundError) as exc_info:
            raise DependencyCreatorNotFoundError("Test error")
        
        assert "Test error" in str(exc_info.value)
        
        with pytest.raises(DependencyCreatorError) as exc_info:
            raise DependencyCreatorError("Test error")
        
        assert "Test error" in str(exc_info.value)

    def test_abstract_methods_are_called(self, mock_config):
        creator = ConcreteDependencyCreator(mock_config)
        creator.create_dependency_file({"name": "test"})
        creator.install_dependencies(["a"], ["b"])

    def test_abstract_method_raises(self,mock_config):
        """Test that abstract methods raise NotImplementedError if not overridden."""

        class IncompleteCreator(BaseDependencyCreator):
            def create_dependency_file(self, project_info: dict) -> None:
                super().create_dependency_file(project_info)

            def install_dependencies(self, packages: list, dev_packages: list) -> None:
                super().install_dependencies(packages, dev_packages)

        creator = IncompleteCreator(mock_config)

        with pytest.raises(NotImplementedError):
            creator.create_dependency_file({})

        with pytest.raises(NotImplementedError):
            creator.install_dependencies([], [])
    