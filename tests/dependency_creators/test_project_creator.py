"""Additional tests for ProjectCreator to cover missing lines."""

import pytest
from unittest.mock import patch, MagicMock
from boilrpy.project_creator import ProjectCreator
from boilrpy.config import Config
from boilrpy.dependency_creators import DependencyCreatorFactory


class TestProjectCreatorMissingCoverage:
    """Tests to cover missing lines in ProjectCreator."""
    
    @pytest.fixture
    def mock_config(self):
        """Create a mock Config object."""
        config = MagicMock(spec=Config)
        config.get_charset.return_value = "utf-8"
        return config
    
    @pytest.fixture
    def project_creator(self, mock_config):
        """Create a ProjectCreator instance."""
        return ProjectCreator(mock_config)
    
    def test_create_dependency_files_with_valueerror_fallback(
        self, 
        project_creator
    ):
        """Test _create_dependency_files with ValueError and fallback to pip."""
        project_info = {
            "name": "test-project",
            "dependencies_manager": "unsupported_manager",  # This will cause ValueError
            "license": "MIT",
            "use_flask": False,
            "create_tests": True
        }
        
        mock_pip_creator = MagicMock()
        
        with patch("builtins.print") as mock_print, \
             patch.object(
                 DependencyCreatorFactory,
                 "create",
                 side_effect=[ValueError("Unsupported"), mock_pip_creator]
             ) as mock_factory:
            
            project_creator._create_dependency_files(project_info)
            
            # Verify error was printed
            assert mock_print.call_count >= 2
            print_calls = [str(call) for call in mock_print.call_args_list]
            assert any("Unsupported" in str(call) for call in print_calls)
            assert any("Falling back to pip" in str(call) for call in print_calls)
            
            # Verify factory was called twice (first with unsupported, then with pip)
            assert mock_factory.call_count == 2
            mock_factory.assert_any_call("unsupported_manager", project_creator.config)
            mock_factory.assert_any_call("pip", project_creator.config)
            
            # Verify pip creator was used
            mock_pip_creator.create_dependency_file.assert_called_once_with(project_info)
    
    def test_create_dependency_files_with_valid_manager(
        self, 
        project_creator
    ):
        """Test _create_dependency_files with valid dependency manager."""
        project_info = {
            "name": "test-project",
            "dependencies_manager": "poetry",
            "license": "MIT",
            "use_flask": True,
            "create_tests": True
        }
        
        mock_creator = MagicMock()
        
        with patch.object(
            DependencyCreatorFactory,
            "create",
            return_value=mock_creator
        ) as mock_factory:
            
            project_creator._create_dependency_files(project_info)
            
            # Verify factory was called once with correct manager
            mock_factory.assert_called_once_with("poetry", project_creator.config)
            
            # Verify creator was used
            mock_creator.create_dependency_file.assert_called_once_with(project_info)
    
    
    # def test_create_poetry_file_with_use_poetry_false(
    #     self, 
    #     project_creator
    # ):
    #     """Test _create_poetry_file returns early when use_poetry is False."""
    #     project_info = {
    #         "name": "test-project",
    #         "use_poetry": False
    #     }
        
    #     with patch("boilrpy.dependency_creators.PoetryCreator") as mock_poetry:
    #         result = project_creator._create_poetry_file(project_info)
            
    #         # Should return early without creating PoetryCreator
    #         mock_poetry.assert_not_called()
    #         assert result is None
    
    # def test_create_poetry_file_with_use_poetry_true(
    #     self, 
    #     project_creator
    # ):
    #     """Test _create_poetry_file creates poetry file when use_poetry is True."""
    #     project_info = {
    #         "name": "test-project",
    #         "use_poetry": True,
    #         "version": "0.1.0",
    #         "description": "Test",
    #         "author": "Test Author",
    #         "license": "MIT"
    #     }
        
    #     mock_poetry_instance = MagicMock()
        
    #     with patch(
    #         "boilrpy.dependency_creators.PoetryCreator",
    #         return_value=mock_poetry_instance
    #     ) as mock_poetry_class:
            
    #         project_creator._create_poetry_file(project_info)
            
    #         # Verify PoetryCreator was instantiated
    #         mock_poetry_class.assert_called_once_with(project_creator.config)
            
    #         # Verify create_poetry_file was called
    #         mock_poetry_instance.create_poetry_file.assert_called_once_with(project_info)
    
    # def test_create_project_calls_create_poetry_file(
    #     self,
    #     project_creator
    # ):
    #     """Test that create_project calls _create_poetry_file when use_poetry is True."""
    #     project_info = {
    #         "name": "poetry-project",
    #         "version": "0.1.0",
    #         "description": "Test",
    #         "author": "Test",
    #         "license": "MIT",
    #         "dependencies_manager": "poetry",
    #         "use_flask": False,
    #         "create_tests": False
    #     }
        
    #     with patch("os.makedirs"), \
    #          patch("os.chdir"), \
    #          patch.object(project_creator, "_create_project_structure"), \
    #          patch.object(project_creator, "_create_dependency_files"), \
    #          patch.object(project_creator, "_initialize_git_repository"):
            
    #         project_creator.create_project(project_info)
            
    #         # Verify _create_poetry_file was called
    #         mock_poetry_file.assert_called_once_with(project_info)
