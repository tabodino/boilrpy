from unittest.mock import MagicMock
import pytest
from boilrpy.file_generators.flask_generator import FlaskGenerator


@pytest.fixture
def flask_generator():
    return FlaskGenerator(None)


def test_generate(flask_generator):
    project_info = {"name": "Test Project", "description": "A test Flask project"}

    flask_generator.generate_app_file = MagicMock()
    flask_generator.generate_base_template = MagicMock()
    flask_generator.generate_index_template = MagicMock()
    flask_generator.generate_dot_env_file = MagicMock()
    flask_generator.generate_style_file = MagicMock()
    flask_generator.generate_script_file = MagicMock()

    flask_generator.generate(project_info)
    flask_generator.generate_app_file.assert_called_once()
    flask_generator.generate_base_template.assert_called_once_with(project_info)
    flask_generator.generate_index_template.assert_called_once_with(project_info)
    flask_generator.generate_dot_env_file.assert_called_once()
    flask_generator.generate_style_file.assert_called_once()
    flask_generator.generate_script_file.assert_called_once()


def test_generate_app_file(flask_generator):
    app_file_content = flask_generator.generate_app_file()
    assert "from flask import Flask, render_template" in app_file_content
    assert "from dotenv import load_dotenv" in app_file_content
    assert "app = Flask(__name__)" in app_file_content
    assert "def index():" in app_file_content
    assert "return render_template('index.html')" in app_file_content
    assert 'app.run(host="0.0.0.0", port=5000, debug=True)' in app_file_content


def test_generate_base_template(flask_generator):
    project_info = {"name": "Test Project"}
    base_template_content = flask_generator.generate_base_template(project_info)
    assert "<!DOCTYPE html>" in base_template_content
    assert (
        "<title>{% block title %}Test Project{% endblock %}</title>"
        in base_template_content
    )
    assert "{{ url_for('static', filename='css/style.css') }}" in base_template_content
    assert "{{ url_for('static', filename='js/script.js') }}" in base_template_content
    assert "{% block content %}{% endblock %}" in base_template_content


def test_generate_index_template(flask_generator):
    project_info = {"name": "Test Project", "description": "A test Flask project"}
    index_template_content = flask_generator.generate_index_template(project_info)
    assert '{% extends "base.html" %}' in index_template_content
    assert "{% block content %}" in index_template_content
    assert "<h1>Welcome to Test Project</h1>" in index_template_content
    assert "<p>A test Flask project</p>" in index_template_content
    assert "{% endblock %}" in index_template_content


def test_generate_dot_env_file(flask_generator):
    dot_env_content = flask_generator.generate_dot_env_file()
    assert "FLASK_APP=app.py" in dot_env_content
    assert "FLASK_ENV=development" in dot_env_content
    assert "FLASK_DEBUG=1" in dot_env_content


def test_generate_style_file(flask_generator):
    style_content = flask_generator.generate_style_file()
    assert "body {" in style_content
    assert "font-family: Arial, sans-serif;" in style_content
    assert (
        "background: linear-gradient(135deg, #00d2ff 0%, #3a47d5 100%);"
        in style_content
    )
    assert ".container {" in style_content
    assert "backdrop-filter: blur(10px);" in style_content


def test_generate_script_file(flask_generator):
    script_content = flask_generator.generate_script_file()
    assert "// Add your custom JavaScript here" in script_content
    assert "console.log('Script loaded');" in script_content
