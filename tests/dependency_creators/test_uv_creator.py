"""Tests for UvCreator."""

import pytest
from unittest.mock import patch, mock_open, MagicMock
import subprocess
from boilrpy.dependency_creators.uv_creator import UvCreator
from boilrpy.dependency_creators.base_dependency_creator import (
    DependencyCreatorNotFoundError,
    DependencyCreatorError
)


class TestUvCreator:
    """Tests for UvCreator class."""
    
    def test_initialization(self, mock_config):
        """Test UvCreator initialization."""
        creator = UvCreator(mock_config)
        assert creator.config == mock_config
        assert creator.charset == "utf-8"
    
    def test_create_dependency_file_success(self, mock_config, base_project_info):
        """Test successful dependency file creation with uv."""
        creator = UvCreator(mock_config)
        
        with patch("subprocess.run") as mock_run, \
             patch("builtins.open", mock_open()):
            
            # Mock uv --version check (success) and uv venv
            mock_run.return_value = MagicMock(stdout="uv 0.1.0", returncode=0)
            
            creator.create_dependency_file(base_project_info)
            
            # Verify uv --version was called first
            first_call = mock_run.call_args_list[0]
            assert first_call[0][0] == ["uv", "--version"]
            
            # Verify uv venv was called
            assert any(
                call[0][0] == ["uv", "venv"]
                for call in mock_run.call_args_list
            )
    
    def test_create_dependency_file_uv_not_found(self, mock_config, base_project_info):
        """Test when uv is not installed."""
        creator = UvCreator(mock_config)
        
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(DependencyCreatorNotFoundError) as exc_info:
                creator.create_dependency_file(base_project_info)
            
            error_msg = str(exc_info.value)
            assert "uv not found" in error_msg
            assert "pip install uv" in error_msg
    
    def test_create_dependency_file_uv_version_check_fails(
        self, 
        mock_config, 
        base_project_info
    ):
        """Test when uv --version check fails."""
        creator = UvCreator(mock_config)
        
        with patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "uv")
        ):
            with pytest.raises(DependencyCreatorNotFoundError) as exc_info:
                creator.create_dependency_file(base_project_info)
            
            error_msg = str(exc_info.value)
            assert "uv not found or not working properly" in error_msg
    
    def test_create_dependency_file_venv_creation_fails(
        self, 
        mock_config, 
        base_project_info
    ):
        """Test when uv venv command fails."""
        creator = UvCreator(mock_config)
        
        call_count = [0]
        
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            cmd = args[0]
            if cmd == ["uv", "--version"]:
                # First call: version check succeeds
                return MagicMock(stdout="uv 0.1.0", returncode=0)
            elif cmd == ["uv", "venv"]:
                # Second call: venv creation fails
                raise subprocess.CalledProcessError(1, "uv venv")
            return MagicMock(returncode=0)
        
        with patch("subprocess.run", side_effect=run_side_effect), \
             patch("builtins.open", mock_open()):
            
            with pytest.raises(DependencyCreatorError) as exc_info:
                creator.create_dependency_file(base_project_info)
            
            assert "uv initialization failed" in str(exc_info.value)
    
    def test_install_dependencies_success(self, mock_config):
        """Test successful dependency installation with uv."""
        creator = UvCreator(mock_config)
        packages = ["flask", "requests"]
        dev_packages = ["pytest"]
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies(packages, dev_packages)
            
            mock_run.assert_called_once_with(
                ["uv", "pip", "install", "flask", "requests", "pytest"],
                check=True
            )
    
    def test_install_dependencies_empty_lists(self, mock_config):
        """Test installing with empty package lists."""
        creator = UvCreator(mock_config)
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies([], [])
            
            mock_run.assert_not_called()
    
    def test_install_dependencies_only_regular_packages(self, mock_config):
        """Test installing only regular packages."""
        creator = UvCreator(mock_config)
        packages = ["flask", "requests"]
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies(packages, [])
            
            mock_run.assert_called_once_with(
                ["uv", "pip", "install", "flask", "requests"],
                check=True
            )
    
    def test_install_dependencies_only_dev_packages(self, mock_config):
        """Test installing only dev packages."""
        creator = UvCreator(mock_config)
        dev_packages = ["pytest", "pylint"]
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies([], dev_packages)
            
            mock_run.assert_called_once_with(
                ["uv", "pip", "install", "pytest", "pylint"],
                check=True
            )
    
    def test_install_dependencies_fails(self, mock_config):
        """Test handling of installation failure."""
        creator = UvCreator(mock_config)
        packages = ["invalid-package"]
        
        with patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "uv")
        ):
            with pytest.raises(DependencyCreatorError) as exc_info:
                creator.install_dependencies(packages, [])
            
            assert "Failed to install dependencies" in str(exc_info.value)
    
    def test_write_requirements_files_with_packages(self, mock_config):
        """Test creating requirements files with packages."""
        creator = UvCreator(mock_config)
        packages = ["flask", "requests"]
        dev_packages = ["pytest", "pylint"]
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._write_requirements_files(packages, dev_packages)
            
            # Verify both files were created
            assert mock_file.call_count == 2
            
            write_calls = [
                call[0][0] 
                for call in mock_file().write.call_args_list
            ]
            
            # Verify content
            assert any("flask" in call for call in write_calls)
            assert any("requests" in call for call in write_calls)
            assert any("pytest" in call for call in write_calls)
            assert any("-r requirements.txt" in call for call in write_calls)
    
    def test_write_requirements_files_empty_packages(self, mock_config):
        """Test creating requirements files with no packages."""
        creator = UvCreator(mock_config)
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._write_requirements_files([], [])
            
            # Should create a empty file to avoid Docker errors
            assert mock_file.call_count == 1
    
    def test_write_requirements_files_only_regular_packages(self, mock_config):
        """Test creating requirements.txt only."""
        creator = UvCreator(mock_config)
        packages = ["flask"]
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._write_requirements_files(packages, [])
            
            # Should only create requirements.txt
            assert mock_file.call_count == 1
            
            write_calls = [
                call[0][0] 
                for call in mock_file().write.call_args_list
            ]
            assert any("flask" in call for call in write_calls)
    
    def test_write_requirements_files_only_dev_packages(self, mock_config):
        """Test creating requirements-dev.txt only."""
        creator = UvCreator(mock_config)
        dev_packages = ["pytest"]
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            creator._write_requirements_files([], dev_packages)
            
            # Should create requirements-dev.txt
            assert mock_file.call_count == 2
            
            write_calls = [
                call[0][0] 
                for call in mock_file().write.call_args_list
            ]
            assert any("-r requirements.txt" in call for call in write_calls)
            assert any("pytest" in call for call in write_calls)
    
    def test_create_dependency_file_with_flask(self, mock_config, project_info_with_flask):
        """Test creating dependency file with Flask enabled."""
        creator = UvCreator(mock_config)
        
        with patch("subprocess.run") as mock_run, \
             patch("builtins.open", mock_open()):
            
            mock_run.return_value = MagicMock(stdout="uv 0.1.0", returncode=0)
            
            creator.create_dependency_file(project_info_with_flask)
            
            # Verify install was called with flask
            install_call = [
                call for call in mock_run.call_args_list 
                if call[0][0][0:3] == ["uv", "pip", "install"]
            ]
            assert len(install_call) > 0
            packages = install_call[0][0][0]
            assert "flask" in packages
    
    def test_create_dependency_file_with_libraries(
        self, 
        mock_config, 
        project_info_with_libraries
    ):
        """Test creating dependency file with additional libraries."""
        creator = UvCreator(mock_config)
        
        with patch("subprocess.run") as mock_run, \
             patch("builtins.open", mock_open()):
            
            mock_run.return_value = MagicMock(stdout="uv 0.1.0", returncode=0)
            
            creator.create_dependency_file(project_info_with_libraries)
            
            # Verify install was called with additional libraries
            install_call = [
                call for call in mock_run.call_args_list 
                if call[0][0][0:3] == ["uv", "pip", "install"]
            ]
            assert len(install_call) > 0
            packages = install_call[0][0][0]
            assert "requests" in packages
            assert "pandas" in packages
            assert "numpy" in packages
