import re

NAME_PATTERN = r"^[a-zA-Z0-9_\-\s]+$"
VERSION_PATTERN = (
    r"^\s*(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)" + r"(?:-(alpha|beta|rc))?\s*$"
)


class InputValidator:
    """
    Class for validating user input.
    """

    DEFAULT_VERSION = "0.1.0"

    @staticmethod
    def validate_project_name(name: str) -> bool:
        """
        Validate project name.

        Args:
            name (str): Project name.

        Returns:
            bool: Whether the project name is valid.
        """
        return re.match(NAME_PATTERN, name) is not None

    @staticmethod
    def validate_version(version: str = DEFAULT_VERSION) -> bool:
        """
        Validate project version.

        Args:
            version (str): Project version.

        Returns:
            bool: Whether the project version is valid.
        """
        return True if version == "" else re.match(VERSION_PATTERN, version) is not None
