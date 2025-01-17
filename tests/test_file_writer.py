import pytest
from unittest.mock import mock_open, patch
from boilrpy.file_writer import FileWriter, FileWriterError
import os


@pytest.fixture
def file_writer():
    return FileWriter(charset="utf-8")


def test_init_with_custom_charset():
    fw = FileWriter(charset="ascii")
    assert fw.charset == "ascii"


@patch("builtins.open", new_callable=mock_open)
def test_open_file_success(mock_file, file_writer):
    with file_writer.open_file("test.txt", "w") as f:
        assert f == mock_file.return_value


@patch("builtins.open")
def test_open_file_ioerror(mock_open, file_writer):
    mock_open.side_effect = IOError("Cannot open file")
    file_writer = FileWriter()
    with pytest.raises(FileWriterError):
        with file_writer.open_file("test.txt", "w"):
            pass


@patch("builtins.open", new_callable=mock_open)
def test_write_file_success(mock_file, file_writer):
    file_writer.write_file("test.txt", "content")
    mock_file.assert_called_once_with("test.txt", "w", encoding="utf-8")
    mock_file().write.assert_called_once_with("content")


@patch("builtins.open")
def test_write_file_ioerror(mock_open, file_writer):
    mock_open.side_effect = IOError("Test error")
    with pytest.raises(FileWriterError) as excinfo:
        file_writer.write_file("test.txt", "content")
    assert "Error writing to file test.txt: Error opening file test.txt: Test error" in str(
        excinfo.value)


@patch("os.makedirs")
def test_create_directory_success(mock_makedirs, file_writer):
    file_writer.create_directory("test_dir")
    mock_makedirs.assert_called_once_with("test_dir", exist_ok=True)


@patch("os.makedirs")
def test_create_directory_success_exist_ok_false(mock_makedirs, file_writer):
    file_writer.create_directory("test_dir", exist_ok=False)
    mock_makedirs.assert_called_once_with("test_dir", exist_ok=False)


@patch("os.makedirs")
def test_create_directory_oserror(mock_makedirs, file_writer):
    mock_makedirs.side_effect = OSError("Test error")
    with pytest.raises(FileWriterError, match="Error creating directory test_dir: Test error"):
        file_writer.create_directory("test_dir")


def test_file_writer_error():
    error = FileWriterError("Test error message")
    assert str(error) == "Test error message"
