"""Tests for ReadmeGenerator."""

import pytest
from unittest.mock import MagicMock, patch
from boilrpy.file_generators.readme_generator import ReadmeGenerator


class TestReadmeGenerator:
    """Tests for ReadmeGenerator class."""
    
    @pytest.fixture
    def mock_config(self):
        """Create a mock Config object."""
        config = MagicMock()
        config.get_charset.return_value = "utf-8"
        return config
    
    @pytest.fixture
    def readme_generator(self, mock_config):
        """Create a ReadmeGenerator instance."""
        return ReadmeGenerator(mock_config)
    
    def test_generate_with_pip(self, readme_generator):
        """Test README generation with pip."""
        project_info = {
            "name": "test-project",
            "description": "A test project",
            "dependencies_manager": "pip",
            "use_flask": False,
            "create_tests": True
        }
        
        content = readme_generator.generate(project_info)
        
        # Check for title-cased version of name
        assert "Test-Project" in content or "test-project" in content.lower()
        assert "A test project" in content
        assert "pip install" in content
        assert "pytest" in content
    
    def test_generate_with_poetry(self, readme_generator):
        """Test README generation with poetry."""
        project_info = {
            "name": "poetry-project",
            "description": "A poetry project",
            "dependencies_manager": "poetry",
            "use_flask": False,
            "create_tests": True
        }
        
        content = readme_generator.generate(project_info)
        
        assert "Poetry-Project" in content or "poetry" in content.lower()
        assert "poetry install" in content
        assert "poetry run pytest" in content
    
    def test_generate_with_flask_and_pip(self, readme_generator):
        """Test README generation with Flask using pip."""
        project_info = {
            "name": "flask-project",
            "description": "A Flask project",
            "dependencies_manager": "pip",
            "use_flask": True,
            "create_tests": False
        }
        
        content = readme_generator.generate(project_info)
        
        assert "Flask-Project" in content or "flask" in content.lower()
        assert "flask run" in content.lower()
        assert "Flask" in content or "flask" in content
    
    def test_generate_with_flask_and_poetry(self, readme_generator):
        """Test README generation with Flask using poetry."""
        project_info = {
            "name": "flask-poetry-project",
            "description": "A Flask project with poetry",
            "dependencies_manager": "poetry",
            "use_flask": True,
            "create_tests": False
        }
        
        content = readme_generator.generate(project_info)
        
        assert "Flask-Poetry-Project" in content or "flask-poetry" in content.lower()
        assert "poetry run flask run" in content.lower()
    
    def test_generate_with_uv(self, readme_generator):
        """Test README generation with uv."""
        project_info = {
            "name": "uv-project",
            "description": "An uv project",
            "dependencies_manager": "uv",
            "use_flask": False,
            "create_tests": True
        }
        
        content = readme_generator.generate(project_info)
        
        assert "Uv-Project" in content or "uv" in content.lower()
        assert "uv venv" in content or "uv pip install" in content
    
    def test_generate_with_conda(self, readme_generator):
        """Test README generation with conda."""
        project_info = {
            "name": "conda-project",
            "description": "A conda project",
            "dependencies_manager": "conda",
            "use_flask": False,
            "create_tests": True
        }
        
        content = readme_generator.generate(project_info)
        
        assert "Conda-Project" in content or "conda" in content.lower()
        assert "conda" in content
    
    def test_generate_with_flask_different_managers(self, readme_generator):
        """Test Flask instructions differ based on dependency manager."""
        managers = ["pip", "poetry", "uv", "conda"]
        
        for manager in managers:
            project_info = {
                "name": f"{manager}-flask-project",
                "description": f"Flask with {manager}",
                "dependencies_manager": manager,
                "use_flask": True,
                "create_tests": False
            }
            
            content = readme_generator.generate(project_info)
            
            # Each manager should have Flask run instructions
            assert "flask run" in content.lower()
    
    def test_generate_with_all_features(self, readme_generator):
        """Test README with all features enabled."""
        project_info = {
            "name": "full-featured-project",
            "description": "A project with all features",
            "dependencies_manager": "poetry",
            "use_flask": True,
            "create_tests": True,
            "use_pylint": True
        }
        
        content = readme_generator.generate(project_info)
        
        assert "Full-Featured-Project" in content or "full-featured" in content.lower()
        assert "poetry" in content
        assert "flask" in content.lower()
        assert "test" in content.lower()
    
    def test_generate_includes_description(self, readme_generator):
        """Test that description is included in README."""
        project_info = {
            "name": "my-project",
            "description": "This is a unique description",
            "dependencies_manager": "pip",
            "use_flask": False,
            "create_tests": False
        }
        
        content = readme_generator.generate(project_info)
        
        assert "This is a unique description" in content
    
    def test_generate_with_tests_includes_testing_section(self, readme_generator):
        """Test that testing section is included when create_tests is True."""
        project_info = {
            "name": "test-project",
            "description": "Project with tests",
            "dependencies_manager": "pip",
            "use_flask": False,
            "create_tests": True
        }
        
        content = readme_generator.generate(project_info)
        
        assert "Testing" in content or "Test" in content
        assert "pytest" in content
    
    def test_generate_without_tests_no_testing_section(self, readme_generator):
        """Test that testing section is not included when create_tests is False."""
        project_info = {
            "name": "no-test-project",
            "description": "Project without tests",
            "dependencies_manager": "pip",
            "license": "MIT",
            "use_flask": False,
            "create_tests": False
        }
        
        content = readme_generator.generate(project_info)
        
        # Should not have pytest instructions
        assert "pytest" not in content.lower() or "Testing" not in content
    
    def test_generate_with_pylint(self, readme_generator):
        """Test README generation with pylint enabled."""
        project_info = {
            "name": "pylint-project",
            "description": "Project with pylint",
            "dependencies_manager": "pip",
            "license": "MIT",
            "use_flask": False,
            "create_tests": False,
            "use_pylint": True
        }
        
        content = readme_generator.generate(project_info)
        
        assert "pylint" in content.lower() or "Pylint" in content
    
    def test_generate_has_contributing_section(self, readme_generator):
        """Test that README includes contributing section."""
        project_info = {
            "name": "contrib-project",
            "description": "Project",
            "dependencies_manager": "pip",
            "license": "MIT",
            "use_flask": False,
            "create_tests": False
        }
        
        content = readme_generator.generate(project_info)
        
        assert "Contributing" in content
        assert "Fork the repository" in content
        assert "Pull Request" in content
    
    def test_generate_with_different_dep_managers_has_setup(self, readme_generator):
        """Test that all dependency managers have setup instructions."""
        managers = ["pip", "poetry", "uv", "conda"]
        
        for manager in managers:
            project_info = {
                "name": f"{manager}-project",
                "description": f"Project with {manager}",
                "dependencies_manager": manager,
                "license": "MIT",
                "use_flask": False,
                "create_tests": False
            }
            
            content = readme_generator.generate(project_info)
            
            # All should have Setup section
            assert "Setup" in content
            # Should mention the dependency manager
            assert manager in content.lower()
