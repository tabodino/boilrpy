"""Tests for DependencyManagerChecker."""

import pytest
from unittest.mock import patch, MagicMock
import subprocess
import os
import sys
from boilrpy.dependency_creators.checker import DependencyManagerChecker


class TestDependencyManagerChecker:
    """Tests for DependencyManagerChecker."""
    
    def test_check_manager_installed(self):
        """Test checking an installed manager."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="pip 23.0.1 from /usr/local/lib",
                returncode=0
            )
            
            is_installed, version = DependencyManagerChecker.check_manager("pip")
            
            assert is_installed is True
            assert version == "pip 23.0.1 from /usr/local/lib"
    
    def test_check_manager_not_installed(self):
        """Test checking a manager that's not installed."""
        with patch("subprocess.run", side_effect=FileNotFoundError):
            is_installed, version = DependencyManagerChecker.check_manager("poetry")
            
            assert is_installed is False
            assert version is None
    
    def test_check_manager_command_fails(self):
        """Test when command returns non-zero exit code."""
        with patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "uv")
        ):
            is_installed, version = DependencyManagerChecker.check_manager("uv")
            
            assert is_installed is False
            assert version is None
    
    def test_check_manager_timeout(self):
        """Test when command times out."""
        with patch(
            "subprocess.run",
            side_effect=subprocess.TimeoutExpired("conda", 5)
        ):
            is_installed, version = DependencyManagerChecker.check_manager("conda")
            
            assert is_installed is False
            assert version is None
    
    def test_check_manager_unsupported(self):
        """Test checking an unsupported manager."""
        is_installed, version = DependencyManagerChecker.check_manager("unsupported")
        
        assert is_installed is False
        assert version is None
    
    def test_check_manager_subprocess_params(self):
        """Test that subprocess is called with correct parameters."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="pip 23.0", returncode=0)
            
            DependencyManagerChecker.check_manager("pip")
            
            mock_run.assert_called_once_with(
                ["pip", "--version"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
    
    def test_check_all_managers(self):
        """Test checking all managers."""
        def run_side_effect(*args, **kwargs):
            cmd = args[0][0]
            if cmd == "pip":
                return MagicMock(stdout="pip 23.0", returncode=0)
            elif cmd == "poetry":
                return MagicMock(stdout="poetry 1.8.0", returncode=0)
            else:
                raise FileNotFoundError()
        
        with patch("subprocess.run", side_effect=run_side_effect):
            results = DependencyManagerChecker.check_all_managers()
            
            assert len(results) == 4
            assert results["pip"][0] is True
            assert results["poetry"][0] is True
            assert results["uv"][0] is False
            assert results["conda"][0] is False
    
    def test_get_available_managers_some_installed(self):
        """Test getting available managers when some are installed."""
        with patch.object(
            DependencyManagerChecker,
            "check_all_managers",
            return_value={
                "pip": (True, "pip 23.0"),
                "poetry": (True, "poetry 1.8.0"),
                "uv": (False, None),
                "conda": (False, None)
            }
        ):
            available = DependencyManagerChecker.get_available_managers()
            
            assert len(available) == 2
            assert "pip" in available
            assert "poetry" in available
    
    def test_get_available_managers_none_installed(self):
        """Test when no managers are installed."""
        with patch.object(
            DependencyManagerChecker,
            "check_all_managers",
            return_value={
                "pip": (False, None),
                "poetry": (False, None),
                "uv": (False, None),
                "conda": (False, None)
            }
        ):
            available = DependencyManagerChecker.get_available_managers()
            
            assert len(available) == 0
    
    def test_get_available_managers_all_installed(self):
        """Test when all managers are installed."""
        with patch.object(
            DependencyManagerChecker,
            "check_all_managers",
            return_value={
                "pip": (True, "pip 23.0"),
                "poetry": (True, "poetry 1.8.0"),
                "uv": (True, "uv 0.1.0"),
                "conda": (True, "conda 23.11.0")
            }
        ):
            available = DependencyManagerChecker.get_available_managers()
            
            assert len(available) == 4
    
    def test_print_status_with_managers(self, capsys):
        """Test printing status when managers are available."""
        with patch.object(
            DependencyManagerChecker,
            "check_all_managers",
            return_value={
                "pip": (True, "pip 23.0.1"),
                "poetry": (False, None),
                "uv": (True, "uv 0.1.0"),
                "conda": (False, None)
            }
        ):
            DependencyManagerChecker.print_status()
            
            captured = capsys.readouterr()
            
            # Check header
            assert "Dependency Managers Status" in captured.out
            
            # Check individual status
            assert "pip" in captured.out
            assert "Installed" in captured.out
            assert "(pip 23.0.1)" in captured.out
            
            assert "poetry" in captured.out
            assert "Not installed" in captured.out
            
            # Check summary
            assert "Available managers: pip, uv" in captured.out
    
    def test_print_status_none_available(self, capsys):
        """Test printing status when no managers are available."""
        with patch.object(
            DependencyManagerChecker,
            "check_all_managers",
            return_value={
                "pip": (False, None),
                "poetry": (False, None),
                "uv": (False, None),
                "conda": (False, None)
            }
        ):
            DependencyManagerChecker.print_status()
            
            captured = capsys.readouterr()
            
            assert "No dependency managers found!" in captured.out
            assert "Please install at least one dependency manager" in captured.out
    
    def test_print_status_all_available(self, capsys):
        """Test printing status when all managers are available."""
        with patch.object(
            DependencyManagerChecker,
            "check_all_managers",
            return_value={
                "pip": (True, "pip 23.0"),
                "poetry": (True, "poetry 1.8.0"),
                "uv": (True, "uv 0.1.0"),
                "conda": (True, "conda 23.11.0")
            }
        ):
            DependencyManagerChecker.print_status()
            
            captured = capsys.readouterr()
            
            assert "Installed" in captured.out
            #assert "Available managers: conda, pip, poetry, uv" in captured.out


class TestDependencyManagerCheckerIntegration:
    """Integration tests for DependencyManagerChecker (real system calls)."""
    
    def test_check_pip_real(self):
        """Test checking pip on real system (should be available)."""
        is_installed, version = DependencyManagerChecker.check_manager("pip")
        
        # pip should be installed in test environment
        assert is_installed is True
        assert version is not None
        assert "pip" in version.lower()
    
    @pytest.mark.skipif(
        not DependencyManagerChecker.check_manager("poetry")[0],
        reason="Poetry not installed"
    )
    def test_check_poetry_real(self):
        """Test checking Poetry on real system (if installed)."""
        is_installed, version = DependencyManagerChecker.check_manager("poetry")
        
        assert is_installed is True
        assert version is not None
        assert "poetry" in version.lower()
    
    @pytest.mark.skipif(
        not DependencyManagerChecker.check_manager("uv")[0],
        reason="uv not installed"
    )
    def test_check_uv_real(self):
        """Test checking uv on real system (if installed)."""
        is_installed, version = DependencyManagerChecker.check_manager("uv")
        
        assert is_installed is True
        assert version is not None
    
    @pytest.mark.skipif(
        not DependencyManagerChecker.check_manager("conda")[0],
        reason="Conda not installed"
    )
    def test_check_conda_real(self):
        """Test checking Conda on real system (if installed)."""
        is_installed, version = DependencyManagerChecker.check_manager("conda")
        
        assert is_installed is True
        assert version is not None
        assert "conda" in version.lower()
    
    def test_get_available_managers_real(self):
        """Test getting available managers on real system."""
        available = DependencyManagerChecker.get_available_managers()
        
        # Should be a list
        assert isinstance(available, list)

    
    def test_check_all_managers_real(self):
        """Test checking all managers on real system."""
        results = DependencyManagerChecker.check_all_managers()
        
        # Should return dict with all managers
        assert isinstance(results, dict)
        assert len(results) == 4
        
        # All keys should be present
        assert "pip" in results
        assert "poetry" in results
        assert "uv" in results
        assert "conda" in results
        
        # pip should be available
        assert results["pip"][0] is True

    def test_print_status_output(self, capsys):
        mock_managers = {
            "poetry": (True, "1.8.0"),
            "pip": (False, None),
            "uv": (True, "0.1.0")
        }
        mock_available = ["poetry", "uv"]

        with patch.object(DependencyManagerChecker, "check_all_managers", return_value=mock_managers), \
            patch.object(DependencyManagerChecker, "get_available_managers", return_value=mock_available):

            DependencyManagerChecker.print_status()

            captured = capsys.readouterr()
            output = captured.out

            # Vérifications simples
            assert "Dependency Managers Status" in output
            assert "poetry     : Installed (1.8.0)" in output
            assert "pip        : Not installed" in output
            assert "uv         : Installed (0.1.0)" in output
            assert "Available managers: poetry, uv" in output

