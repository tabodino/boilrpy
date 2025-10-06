"""Tests for PoetryCreator."""

import pytest
from unittest.mock import patch, mock_open, MagicMock, call
import subprocess
from boilrpy.dependency_creators.poetry_creator import PoetryCreator
from boilrpy.dependency_creators.base_dependency_creator import (
    DependencyCreatorNotFoundError,
    DependencyCreatorError
)


class TestPoetryCreator:
    """Tests for PoetryCreator class."""
    
    def test_initialization(self, mock_config):
        """Test PoetryCreator initialization."""
        creator = PoetryCreator(mock_config)
        assert creator.config == mock_config
        assert creator.charset == "utf-8"
    
    def test_create_dependency_file_success(self, mock_config, base_project_info):
        """Test successful dependency file creation."""
        creator = PoetryCreator(mock_config)
        
        mock_toml_data = {
            "tool": {
                "poetry": {
                    "name": "",
                    "version": "",
                    "description": "",
                    "authors": [],
                    "license": ""
                }
            }
        }
        
        with patch("subprocess.run") as mock_run, \
             patch("builtins.open", mock_open(read_data="")) as mock_file, \
             patch("toml.load", return_value=mock_toml_data), \
             patch("toml.dump"), \
             patch.object(creator, "_check_poetry_version", return_value="1.8.0"):
            
            mock_run.return_value = MagicMock(stdout="Poetry version 1.8.0", returncode=0)
            
            creator.create_dependency_file(base_project_info)
            
            # Verify poetry init was called
            assert any(
                call_args[0][0] == ["poetry", "init", "-n"]
                for call_args in mock_run.call_args_list
            )
    
    def test_create_dependency_file_poetry_not_found(self, mock_config, base_project_info):
        """Test when Poetry is not installed."""
        creator = PoetryCreator(mock_config)
        
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(DependencyCreatorNotFoundError) as exc_info:
                creator.create_dependency_file(base_project_info)
            
            assert "Poetry not found" in str(exc_info.value)
    
    def test_create_dependency_file_poetry_init_fails(self, mock_config, base_project_info):
        """Test when poetry init command fails."""
        creator = PoetryCreator(mock_config)
        
        with patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "poetry")
        ):
            with pytest.raises(DependencyCreatorError) as exc_info:
                creator.create_dependency_file(base_project_info)
            
            assert "Poetry initialization failed" in str(exc_info.value)
    
    def test_install_dependencies_regular_packages(self, mock_config):
        """Test installing regular packages."""
        creator = PoetryCreator(mock_config)
        packages = ["flask", "requests"]
        dev_packages = []
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies(packages, dev_packages)
            
            mock_run.assert_called_once_with(
                ["poetry", "add"] + packages,
                check=True
            )
    
    def test_install_dependencies_dev_packages(self, mock_config):
        """Test installing dev packages."""
        creator = PoetryCreator(mock_config)
        packages = []
        dev_packages = ["pytest", "pylint"]
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies(packages, dev_packages)
            
            mock_run.assert_called_once_with(
                ["poetry", "add", "--group", "dev"] + dev_packages,
                check=True
            )
    
    def test_install_dependencies_both_types(self, mock_config):
        """Test installing both regular and dev packages."""
        creator = PoetryCreator(mock_config)
        packages = ["flask", "requests"]
        dev_packages = ["pytest", "pylint"]
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies(packages, dev_packages)
            
            assert mock_run.call_count == 2
            # Check dev packages call
            mock_run.assert_any_call(
                ["poetry", "add", "--group", "dev"] + dev_packages,
                check=True
            )
            # Check regular packages call
            mock_run.assert_any_call(
                ["poetry", "add"] + packages,
                check=True
            )
    
    def test_install_dependencies_empty_lists(self, mock_config):
        """Test installing with empty package lists."""
        creator = PoetryCreator(mock_config)
        packages = []
        dev_packages = []
        
        with patch("subprocess.run") as mock_run:
            creator.install_dependencies(packages, dev_packages)
            
            mock_run.assert_not_called()
    
    def test_install_dependencies_fails(self, mock_config):
        """Test handling of installation failure."""
        creator = PoetryCreator(mock_config)
        packages = ["flask"]
        
        with patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "poetry")
        ):
            with pytest.raises(DependencyCreatorError) as exc_info:
                creator.install_dependencies(packages, [])
            
            assert "Failed to install dependencies" in str(exc_info.value)
    
    def test_update_pyproject_toml_version_1(self, mock_config, base_project_info):
        """Test updating pyproject.toml for Poetry v1."""
        creator = PoetryCreator(mock_config)
        
        mock_toml_data = {
            "tool": {
                "poetry": {
                    "name": "",
                    "version": "",
                    "description": "",
                    "authors": [],
                    "license": ""
                }
            }
        }
        
        with patch("builtins.open", mock_open()) as mock_file, \
             patch("toml.load", return_value=mock_toml_data) as mock_load, \
             patch("toml.dump") as mock_dump, \
             patch.object(creator, "_check_poetry_version", return_value="1.8.0"):
            
            creator._update_pyproject_toml(base_project_info)
            
            # Verify toml.dump was called
            mock_dump.assert_called_once()
            dumped_data = mock_dump.call_args[0][0]
            
            # Verify data was updated correctly for v1
            assert dumped_data["tool"]["poetry"]["name"] == "test-project"
            assert dumped_data["tool"]["poetry"]["version"] == "0.1.0"
            assert dumped_data["tool"]["poetry"]["description"] == "A test project"
            assert dumped_data["tool"]["poetry"]["authors"] == ["Test Author"]
            assert dumped_data["tool"]["poetry"]["license"] == "MIT"
    
    def test_update_pyproject_toml_version_2(self, mock_config, base_project_info):
        """Test updating pyproject.toml for Poetry v2."""
        creator = PoetryCreator(mock_config)
        
        mock_toml_data = {
            "project": {
                "name": "",
                "version": "",
                "description": "",
                "authors": [],
                "license": {}
            }
        }
        
        with patch("builtins.open", mock_open()) as mock_file, \
             patch("toml.load", return_value=mock_toml_data) as mock_load, \
             patch("toml.dump") as mock_dump, \
             patch.object(creator, "_check_poetry_version", return_value="2.0.0"):
            
            creator._update_pyproject_toml(base_project_info)
            
            mock_dump.assert_called_once()
            dumped_data = mock_dump.call_args[0][0]
            
            # Verify data was updated correctly for v2
            assert dumped_data["project"]["name"] == "test-project"
            assert dumped_data["project"]["version"] == "0.1.0"
            assert dumped_data["project"]["description"] == "A test project"
            assert dumped_data["project"]["authors"] == [{"name": "Test Author"}]
            assert dumped_data["project"]["license"] == {"text": "MIT"}
    
    def test_update_pyproject_toml_no_author(self, mock_config):
        """Test updating pyproject.toml without author."""
        creator = PoetryCreator(mock_config)
        project_info = {
            "name": "test",
            "version": "0.1.0",
            "description": "Test",
            "author": "",  # Empty author
            "license": "MIT"
        }
        
        mock_toml_data = {
            "project": {
                "name": "",
                "version": "",
                "description": "",
                "authors": [],
                "license": {}
            }
        }
        
        with patch("builtins.open", mock_open()), \
             patch("toml.load", return_value=mock_toml_data), \
             patch("toml.dump") as mock_dump, \
             patch.object(creator, "_check_poetry_version", return_value="2.0.0"):
            
            creator._update_pyproject_toml(project_info)
            
            dumped_data = mock_dump.call_args[0][0]
            # Authors should not be set when empty
            assert "authors" not in dumped_data["project"] or \
                   dumped_data["project"]["authors"] == []
    
    def test_check_poetry_version(self, mock_config):
        """Test checking Poetry version."""
        creator = PoetryCreator(mock_config)
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = "Poetry (version 1.8.0)"
            mock_run.return_value.returncode = 0
            # mock_run.return_value = MagicMock(
            #     stdout="Poetry (version 1.8.0)",
            #     returncode=0
            # )
            
            version = creator._check_poetry_version()
            assert version == "1.8.0)"
            mock_run.assert_called_once_with(
                ["poetry", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
    
    def test_check_poetry_version_different_format(self, mock_config):
        """Test checking Poetry version with different output format."""
        creator = PoetryCreator(mock_config)
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="Poetry version 2.0.1",
                returncode=0
            )
            
            version = creator._check_poetry_version()
            
            assert version == "2.0.1"
