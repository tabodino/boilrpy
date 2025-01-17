from contextlib import contextmanager
import os
from typing import Generator
from boilrpy.config import Config


class FileWriterError(Exception):
    """Custom exception for FileWriter errors"""


class FileWriter:
    """Class to write files and directories."""
    def __init__(self, charset: str = Config().get_charset()) -> None:
        self.charset = charset

    @contextmanager
    def open_file(self, filename: str, mode: str = "w") -> Generator:
        """Context manager to open and close a file.

        Args:
            filename (str): The name of the file to open.
            mode (str, optional): The mode to open the file in. Defaults to "w".

        Yields:
            file: The opened file object.
        """
        file = None
        try:
            file = open(filename, mode, encoding=self.charset)
            yield file
        except IOError as e:
            raise FileWriterError(f"Error opening file {filename}: {e}") from e
        finally:
            if file:
                file.close()

    def write_file(self, filename: str, content: str) -> None:
        """Write content to a file.

        Args:
            filename (str): The name of the file to write to.
            content (str): The content to write to the file.
        """
        try:
            with self.open_file(filename, "w") as file:
                file.write(content)
        except FileWriterError as e:
            raise FileWriterError(f"Error writing to file {filename}: {e}") from e

    def create_directory(self, directory: str, exist_ok: bool = True) -> None:
        """Create a directory.

        Args:
            directory (str): The name of the directory to create.
            exist_ok (bool, optional): Whether to raise an exception 
            if the directory already exists. Defaults to True.
        """
        try:
            os.makedirs(directory, exist_ok=exist_ok)
        except OSError as e:
            raise FileWriterError(f"Error creating directory {directory}: {e}") from e
