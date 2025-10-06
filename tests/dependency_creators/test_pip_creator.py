"""Tests for PipCreator."""

import pytest
from unittest.mock import patch, mock_open
import subprocess
from boilrpy.dependency_creators.pip_creator import PipCreator
from boilrpy.dependency_creators.base_dependency_creator import (
    DependencyCreatorNotFoundError,
    DependencyCreatorError
)


class TestPipCreator:
    """Tests for PipCreator class."""
    
    def test_initialization(self, mock_config):
        """Test PipCreator initialization."""
        creator = PipCreator(mock_config)
        assert creator.config == mock_config
        assert creator.charset == "utf-8"
    
    def test_create_dependency_file_with_packages(
        self, 
        mock_config, 
        project_info_with_flask
    ):
        """Test creating dependency files with packages."""
        creator = PipCreator(mock_config)
        
        with patch("builtins.open", mock_open()) as mock_file, \
             patch("builtins.print"):
            
            creator.create_dependency_file(project_info_with_flask)
            
            # Verify files were created
            assert mock_file.call_count >= 2  # requirements.txt and requirements-dev.txt
    
    def test_create_dependency_file_minimal(self, mock_config, project_info_minimal):
        """Test creating dependency files with minimal config."""
        creator = PipCreator(mock_config)
        
        with patch("builtins.open", mock_open()) as mock_file, \
             patch("builtins.print"):
            
            creator.create_dependency_file(project_info_minimal)
            
            # Should still create requirements.txt (empty or with comment)
            assert mock_file.called
    
    def test_create_dependency_file_prints_instructions(
        self, 
        mock_config, 
        base_project_info
    ):
        """Test that dependency file creation prints instructions."""
        creator = PipCreator(mock_config)
        
        with patch("builtins.open", mock_open()), \
             patch("builtins.print") as mock_print:
            
            creator.create_dependency_file(base_project_info)
            
            # Verify instructions were printed
            print_calls = [str(call) for call in mock_print.call_args_list]
            assert any("install dependencies" in str(call).lower() for call in print_calls)
            assert any("venv" in str(call).lower() for call in print_calls)
    
    def test_create_dependency_file_exception_handling(
        self, 
        mock_config, 
        base_project_info
    ):
        """Test exception handling during file creation."""
        creator = PipCreator(mock_config)
        
        with patch("builtins.open", side_effect=IOError("Cannot write file")):
            with pytest.raises(DependencyCreatorError) as exc_info:
                creator.create_dependency_file(base_project_info)
            
            assert "pip initialization failed" in str(exc_info.value)
    
    def test_install_dependencies_success(self, mock_config):
        """Test successful dependency installation."""
        creator = PipCreator(mock_config)
        packages = ["flask", "requests"]
        dev_packages = ["pytest"]
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies(packages, dev_packages)
            
            # Verify pip install was called with all packages
            mock_run.assert_called_once_with(
                ["pip", "install", "flask", "requests", "pytest"],
                check=True
            )
    
    def test_install_dependencies_empty_lists(self, mock_config):
        """Test installing with empty package lists."""
        creator = PipCreator(mock_config)
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies([], [])
            
            mock_run.assert_not_called()
    
    def test_install_dependencies_only_regular_packages(self, mock_config):
        """Test installing only regular packages."""
        creator = PipCreator(mock_config)
        packages = ["flask", "requests"]
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies(packages, [])
            
            mock_run.assert_called_once_with(
                ["pip", "install", "flask", "requests"],
                check=True
            )
    
    def test_install_dependencies_only_dev_packages(self, mock_config):
        """Test installing only dev packages."""
        creator = PipCreator(mock_config)
        dev_packages = ["pytest", "pylint"]
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies([], dev_packages)
            
            mock_run.assert_called_once_with(
                ["pip", "install", "pytest", "pylint"],
                check=True
            )
    
    def test_install_dependencies_pip_not_found(self, mock_config):
        """Test when pip is not found."""
        creator = PipCreator(mock_config)
        packages = ["flask"]
        
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(DependencyCreatorNotFoundError) as exc_info:
                creator.install_dependencies(packages, [])
            
            assert "pip not found" in str(exc_info.value)
    
    def test_install_dependencies_fails(self, mock_config):
        """Test handling of installation failure."""
        creator = PipCreator(mock_config)
        packages = ["invalid-package-name-xyz"]
        
        with patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "pip")
        ):
            with pytest.raises(DependencyCreatorError) as exc_info:
                creator.install_dependencies(packages, [])
            
            assert "Failed to install dependencies" in str(exc_info.value)
    
    def test_write_requirements_files_with_packages(self, mock_config):
        """Test creating requirements.txt with packages."""
        creator = PipCreator(mock_config)
        packages = ["flask", "requests", "pandas"]
        dev_packages = ["pytest", "pylint"]
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._write_requirements_files(packages, dev_packages)
            
            # Get all write calls
            write_calls = [
                call[0][0] 
                for call in mock_file().write.call_args_list
            ]
            
            # Verify packages were written
            assert any("flask" in call for call in write_calls)
            assert any("requests" in call for call in write_calls)
            assert any("pandas" in call for call in write_calls)
    
    def test_write_requirements_files_empty_packages(self, mock_config):
        """Test creating requirements.txt with no packages."""
        creator = PipCreator(mock_config)
        packages = []
        dev_packages = []
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._write_requirements_files(packages, dev_packages)
            
            # Should create file with comment
            write_calls = [
                call[0][0] 
                for call in mock_file().write.call_args_list
            ]
            assert any("Add your dependencies here" in call for call in write_calls)
    
    def test_write_requirements_files_with_dev_packages(self, mock_config):
        """Test creating requirements-dev.txt."""
        creator = PipCreator(mock_config)
        packages = ["flask"]
        dev_packages = ["pytest", "pylint"]
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._write_requirements_files(packages, dev_packages)
            
            # Verify open was called for both files
            assert mock_file.call_count == 2
            
            # Get all write calls
            write_calls = [
                call[0][0] 
                for call in mock_file().write.call_args_list
            ]
            
            # Verify dev packages and reference to requirements.txt
            assert any("-r requirements.txt" in call for call in write_calls)
            assert any("pytest" in call for call in write_calls)
            assert any("pylint" in call for call in write_calls)
    
    def test_write_requirements_files_only_dev_packages(self, mock_config):
        """Test creating requirements-dev.txt without regular packages."""
        creator = PipCreator(mock_config)
        packages = []
        dev_packages = ["pytest"]
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._write_requirements_files(packages, dev_packages)
            
            # Should create requirements-dev.txt
            write_calls = [
                call[0][0] 
                for call in mock_file().write.call_args_list
            ]
            assert any("-r requirements.txt" in call for call in write_calls)
            assert any("pytest" in call for call in write_calls)
