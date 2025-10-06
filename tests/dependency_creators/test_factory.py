"""Tests for DependencyCreatorFactory."""

import pytest
from unittest.mock import MagicMock
from boilrpy.dependency_creators.factory import DependencyCreatorFactory
from boilrpy.dependency_creators.base_dependency_creator import BaseDependencyCreator
from boilrpy.dependency_creators.poetry_creator import PoetryCreator
from boilrpy.dependency_creators.pip_creator import PipCreator
from boilrpy.dependency_creators.uv_creator import UvCreator
from boilrpy.dependency_creators.conda_creator import CondaCreator


class TestDependencyCreatorFactory:
    """Tests for DependencyCreatorFactory."""
    
    def test_create_poetry_creator(self, mock_config):
        """Test creating Poetry creator."""
        creator = DependencyCreatorFactory.create("poetry", mock_config)
        assert isinstance(creator, PoetryCreator)
        assert creator.config == mock_config
    
    def test_create_pip_creator(self, mock_config):
        """Test creating pip creator."""
        creator = DependencyCreatorFactory.create("pip", mock_config)
        assert isinstance(creator, PipCreator)
        assert creator.config == mock_config
    
    def test_create_uv_creator(self, mock_config):
        """Test creating uv creator."""
        creator = DependencyCreatorFactory.create("uv", mock_config)
        assert isinstance(creator, UvCreator)
        assert creator.config == mock_config
    
    def test_create_conda_creator(self, mock_config):
        """Test creating Conda creator."""
        creator = DependencyCreatorFactory.create("conda", mock_config)
        assert isinstance(creator, CondaCreator)
        assert creator.config == mock_config
    
    def test_create_case_insensitive(self, mock_config):
        """Test that factory is case-insensitive."""
        creator_lower = DependencyCreatorFactory.create("poetry", mock_config)
        creator_upper = DependencyCreatorFactory.create("POETRY", mock_config)
        creator_mixed = DependencyCreatorFactory.create("PoEtRy", mock_config)
        
        assert type(creator_lower) == type(creator_upper) == type(creator_mixed)
        assert all(isinstance(c, PoetryCreator) for c in [creator_lower, creator_upper, creator_mixed])
    
    def test_create_unsupported_manager(self, mock_config):
        """Test creating with unsupported manager raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            DependencyCreatorFactory.create("unsupported", mock_config)
        
        assert "Unsupported dependency manager" in str(exc_info.value)
        assert "unsupported" in str(exc_info.value)
        assert "Supported managers" in str(exc_info.value)
    
    def test_create_empty_string(self, mock_config):
        """Test creating with empty string raises ValueError."""
        with pytest.raises(ValueError):
            DependencyCreatorFactory.create("", mock_config)
    
    def test_get_supported_managers(self):
        """Test getting list of supported managers."""
        managers = DependencyCreatorFactory.get_supported_managers()
        
        assert isinstance(managers, list)
        assert len(managers) == 4
        assert "pip" in managers
        assert "poetry" in managers
        assert "uv" in managers
        assert "conda" in managers
        
        # Verify list is sorted
        assert managers == sorted(managers)
    
    def test_is_supported_valid_manager(self):
        """Test checking if a manager is supported (valid cases)."""
        assert DependencyCreatorFactory.is_supported("poetry") is True
        assert DependencyCreatorFactory.is_supported("pip") is True
        assert DependencyCreatorFactory.is_supported("uv") is True
        assert DependencyCreatorFactory.is_supported("conda") is True
    
    def test_is_supported_invalid_manager(self):
        """Test checking if a manager is supported (invalid cases)."""
        assert DependencyCreatorFactory.is_supported("unsupported") is False
        assert DependencyCreatorFactory.is_supported("pipenv") is False
        assert DependencyCreatorFactory.is_supported("") is False
    
    def test_is_supported_case_insensitive(self):
        """Test that is_supported is case-insensitive."""
        assert DependencyCreatorFactory.is_supported("POETRY") is True
        assert DependencyCreatorFactory.is_supported("Poetry") is True
        assert DependencyCreatorFactory.is_supported("pOeTrY") is True
    
    def test_register_creator_success(self, mock_config):
        """Test registering a new creator."""
        class CustomCreator(BaseDependencyCreator):
            def create_dependency_file(self, project_info: dict) -> None:
                pass
            def install_dependencies(self, packages: list, dev_packages: list) -> None:
                pass
        
        DependencyCreatorFactory.register_creator("custom", CustomCreator)
        
        # Verify it was registered
        assert "custom" in DependencyCreatorFactory.get_supported_managers()
        
        # Verify we can create it
        creator = DependencyCreatorFactory.create("custom", mock_config)
        assert isinstance(creator, CustomCreator)
        
        # Cleanup
        del DependencyCreatorFactory._creators["custom"]
    
    def test_register_creator_invalid_type(self):
        """Test registering a creator that doesn't inherit from BaseDependencyCreator."""
        class NotACreator:
            pass
        
        with pytest.raises(TypeError) as exc_info:
            DependencyCreatorFactory.register_creator("invalid", NotACreator)
        
        assert "must inherit from BaseDependencyCreator" in str(exc_info.value)
    
    def test_register_creator_overwrites_existing(self, mock_config):
        """Test that registering overwrites existing creator."""
        class NewPoetryCreator(BaseDependencyCreator):
            def create_dependency_file(self, project_info: dict) -> None:
                pass
            def install_dependencies(self, packages: list, dev_packages: list) -> None:
                pass
        
        # Register new creator with same name
        DependencyCreatorFactory.register_creator("poetry", NewPoetryCreator)
        
        # Verify it was overwritten
        creator = DependencyCreatorFactory.create("poetry", mock_config)
        assert isinstance(creator, NewPoetryCreator)
        assert not isinstance(creator, PoetryCreator)
        
        # Restore original
        DependencyCreatorFactory.register_creator("poetry", PoetryCreator)
    
    def test_register_creator_case_insensitive_name(self, mock_config):
        """Test that register_creator normalizes names to lowercase."""
        class CustomCreator(BaseDependencyCreator):
            def create_dependency_file(self, project_info: dict) -> None:
                pass
            def install_dependencies(self, packages: list, dev_packages: list) -> None:
                pass
        
        DependencyCreatorFactory.register_creator("MyCustom", CustomCreator)
        
        # Should be registered as lowercase
        assert "mycustom" in DependencyCreatorFactory.get_supported_managers()
        
        # Can create with any case
        creator = DependencyCreatorFactory.create("MYCUSTOM", mock_config)
        assert isinstance(creator, CustomCreator)
        
        # Cleanup
        del DependencyCreatorFactory._creators["mycustom"]
    
    def test_factory_instance_isolation(self, mock_config):
        """Test that created instances are isolated."""
        creator1 = DependencyCreatorFactory.create("pip", mock_config)
        creator2 = DependencyCreatorFactory.create("pip", mock_config)
        
        # Should be different instances
        assert creator1 is not creator2
        
        # But same type and config
        assert type(creator1) == type(creator2)
        assert creator1.config == creator2.config


class TestDependencyCreatorFactoryIntegration:
    """Integration tests for DependencyCreatorFactory."""
    
    def test_create_all_supported_managers(self, mock_config):
        """Test creating all supported dependency managers."""
        managers = DependencyCreatorFactory.get_supported_managers()
        
        for manager in managers:
            creator = DependencyCreatorFactory.create(manager, mock_config)
            assert isinstance(creator, BaseDependencyCreator)
            assert creator.config == mock_config
    
    def test_factory_with_different_configs(self):
        """Test factory with different config objects."""
        config1 = MagicMock()
        config1.get_charset.return_value = "utf-8"
        
        config2 = MagicMock()
        config2.get_charset.return_value = "latin-1"
        
        creator1 = DependencyCreatorFactory.create("pip", config1)
        creator2 = DependencyCreatorFactory.create("pip", config2)
        
        assert creator1.config != creator2.config
        assert creator1.charset == "utf-8"
        assert creator2.charset == "latin-1"
