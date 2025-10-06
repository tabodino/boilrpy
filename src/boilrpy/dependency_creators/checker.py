"""Utility to check if dependency managers are installed."""

import subprocess
from typing import Dict, Optional


class DependencyManagerChecker:
    """Check availability of dependency managers on the system."""

    @staticmethod
    def check_manager(manager_name: str) -> tuple[bool, Optional[str]]:
        """Check if a dependency manager is installed.

        Args:
            manager_name: Name of the dependency manager to check

        Returns:
            tuple: (is_installed, version_string or None)
        """
        version_commands = {
            "pip": ["pip", "--version"],
            "poetry": ["poetry", "--version"],
            "uv": ["uv", "--version"],
            "conda": ["conda", "--version"],
        }

        command = version_commands.get(manager_name)
        if not command:
            return False, None

        try:
            result = subprocess.run(
                command, capture_output=True, text=True, check=True, timeout=5
            )
            return True, result.stdout.strip()
        except (
            FileNotFoundError,
            subprocess.CalledProcessError,
            subprocess.TimeoutExpired,
        ):
            return False, None

    @staticmethod
    def check_all_managers() -> Dict[str, tuple[bool, Optional[str]]]:
        """Check all supported dependency managers.

        Returns:
            dict: Dictionary mapping manager names to (is_installed, version)
        """
        managers = ["pip", "poetry", "uv", "conda"]
        return {
            manager: DependencyManagerChecker.check_manager(manager)
            for manager in managers
        }

    @staticmethod
    def get_available_managers() -> list[str]:
        """Get list of available (installed) dependency managers.

        Returns:
            list: List of installed manager names
        """
        all_managers = DependencyManagerChecker.check_all_managers()
        return [
            manager for manager, (installed, _) in all_managers.items() if installed
        ]

    @staticmethod
    def print_status() -> None:
        """Print status of all dependency managers."""
        print("\n" + "=" * 60)
        print("Dependency Managers Status")
        print("=" * 60)

        all_managers = DependencyManagerChecker.check_all_managers()

        for manager, (installed, version) in all_managers.items():
            status = "Installed" if installed else "Not installed"
            version_info = f" ({version})" if version else ""
            print(f"{manager:10} : {status}{version_info}")

        print("=" * 60)

        available = DependencyManagerChecker.get_available_managers()
        if available:
            print(f"\nAvailable managers: {', '.join(available)}")
        else:
            print("\n No dependency managers found!")
            print("Please install at least one dependency manager.")


if __name__ == "__main__":  # pragma: no cover
    # Run status check
    DependencyManagerChecker.print_status()
