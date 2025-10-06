"""Tests for CondaCreator."""

import pytest
from unittest.mock import patch, mock_open, MagicMock
import subprocess
from boilrpy.config import Config
from boilrpy.dependency_creators.conda_creator import CondaCreator
from boilrpy.dependency_creators.base_dependency_creator import (
    DependencyCreatorNotFoundError,
    DependencyCreatorError
)


class TestCondaCreator:
    """Tests for CondaCreator class."""
    
    def test_initialization(self, mock_config):
        """Test CondaCreator initialization."""
        creator = CondaCreator(mock_config)
        assert creator.config == mock_config
        assert creator.charset == "utf-8"
    
    def test_create_dependency_file_success(self, mock_config, base_project_info):
        """Test successful environment.yml creation."""
        creator = CondaCreator(mock_config)
        
        with patch("builtins.open", mock_open()) as mock_file, \
             patch("builtins.print"):
            
            creator.create_dependency_file(base_project_info)
            
            # Verify environment.yml was created
            mock_file.assert_called_once_with("environment.yml", "w", encoding="utf-8")
    
    def test_create_dependency_file_prints_instructions(
        self, 
        mock_config, 
        base_project_info
    ):
        """Test that instructions are printed."""
        creator = CondaCreator(mock_config)
        
        with patch("builtins.open", mock_open()), \
             patch("builtins.print") as mock_print:
            
            creator.create_dependency_file(base_project_info)
            
            # Verify instructions were printed
            print_calls = [str(call) for call in mock_print.call_args_list]
            assert any("conda env create" in str(call) for call in print_calls)
            assert any("conda activate" in str(call) for call in print_calls)
    
    def test_create_dependency_file_exception_handling(
        self, 
        mock_config, 
        base_project_info
    ):
        """Test exception handling during file creation."""
        creator = CondaCreator(mock_config)
        
        with patch("builtins.open", side_effect=IOError("Cannot write file")):
            with pytest.raises(DependencyCreatorError) as exc_info:
                creator.create_dependency_file(base_project_info)
            
            assert "conda initialization failed" in str(exc_info.value)
    
    def test_install_dependencies_success(self, mock_config):
        """Test successful dependency installation with conda."""
        creator = CondaCreator(mock_config)
        packages = ["numpy", "pandas"]
        dev_packages = ["pytest"]
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies(packages, dev_packages)
            
            mock_run.assert_called_once_with(
                ["conda", "install", "-y", "numpy", "pandas", "pytest"],
                check=True
            )
    
    def test_install_dependencies_empty_lists(self, mock_config):
        """Test installing with empty package lists."""
        creator = CondaCreator(mock_config)
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies([], [])
            
            mock_run.assert_not_called()
    
    def test_install_dependencies_conda_not_found(self, mock_config):
        """Test when conda is not installed."""
        creator = CondaCreator(mock_config)
        packages = ["numpy"]
        
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(DependencyCreatorNotFoundError) as exc_info:
                creator.install_dependencies(packages, [])
            
            assert "conda not found" in str(exc_info.value)
    
    def test_install_dependencies_fails(self, mock_config):
        """Test handling of installation failure."""
        creator = CondaCreator(mock_config)
        packages = ["invalid-package"]
        
        with patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "conda")
        ):
            with pytest.raises(DependencyCreatorError) as exc_info:
                creator.install_dependencies(packages, [])
            
            assert "Failed to install dependencies" in str(exc_info.value)
    
    def test_create_environment_file_basic(self, mock_config, base_project_info):
        """Test creating basic environment.yml file."""
        creator = CondaCreator(mock_config)
        packages = ["flask"]
        dev_packages = ["pytest"]
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._create_environment_file(base_project_info, packages, dev_packages)
            
            # Get written content
            write_calls = mock_file().write.call_args_list
            content = "".join(call[0][0] for call in write_calls)
            
            # Verify structure
            assert f"name: {base_project_info['name']}" in content
            assert "channels:" in content
            assert "dependencies:" in content
            assert "python=" in content
            assert "flask" in content
            assert "pytest" in content
            assert "pip:" in content
    
    def test_create_environment_file_with_python_version(self, mock_config):
        """Test creating environment.yml with specific Python version."""
        creator = CondaCreator(mock_config)
        project_info = {
            "name": "test-project",
            "python_version": "3.9"
        }
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._create_environment_file(project_info, [], [])
            
            write_calls = mock_file().write.call_args_list
            content = "".join(call[0][0] for call in write_calls)
            
            assert "python=3.9" in content
    
    def test_create_environment_file_default_python_version(self, mock_config):
        """Test creating environment.yml with default Python version."""
        creator = CondaCreator(mock_config)
        project_info = {"name": "test-project"}
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._create_environment_file(project_info, [], [])
            
            write_calls = mock_file().write.call_args_list
            content = "".join(call[0][0] for call in write_calls)
            
            # Should use default version (3.11)
            assert "python=3.11" in content
    
    def test_create_environment_file_with_many_packages(self, mock_config):
        """Test creating environment.yml with multiple packages."""
        creator = CondaCreator(mock_config)
        project_info = {"name": "data-science-project"}
        packages = ["numpy", "pandas", "scikit-learn", "matplotlib"]
        dev_packages = ["pytest", "pylint", "black"]
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._create_environment_file(project_info, packages, dev_packages)
            
            write_calls = mock_file().write.call_args_list
            content = "".join(call[0][0] for call in write_calls)
            
            # Verify all packages are included
            for package in packages + dev_packages:
                assert package in content
    
    def test_create_environment_file_empty_packages(self, mock_config):
        """Test creating environment.yml with no packages."""
        creator = CondaCreator(mock_config)
        project_info = {"name": "minimal-project"}
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._create_environment_file(project_info, [], [])
            
            write_calls = mock_file().write.call_args_list
            content = "".join(call[0][0] for call in write_calls)
            
            # Should still have structure
            assert "name: minimal-project" in content
            assert "dependencies:" in content
            assert "python=" in content
