from boilrpy.file_generators.base_generator import BaseGenerator


class FlaskGenerator(BaseGenerator):
    """
    Flask structure generator.
    """

    def generate(self, *args, **kwargs) -> None:
        project_info = args[0] if args else {}
        self.generate_app_file()
        self.generate_base_template(project_info)
        self.generate_index_template(project_info)
        self.generate_dot_env_file()
        self.generate_style_file()
        self.generate_script_file()

    def generate_app_file(self) -> str:
        """
        Generate app file content.

        :return: Content of app file
        """
        return """from flask import Flask, render_template
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
"""

    def generate_base_template(self, project_info: dict) -> str:
        """
        Generate base template content.

        :args project_info: Dictionary containing project information

        :return: Content of base template
        """
        template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}${project_name}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <!-- Add your header content here -->
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <!-- Add your footer content here -->
    </footer>
    
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
"""
        return self.render_template(template, project_name=project_info["name"].title())

    def generate_index_template(self, project_info: dict) -> str:
        """
        Generate index template content.

        :args project_info: Dictionary containing project information

        :return: Content of index template
        """
        template = """{% extends "base.html" %}

{% block content %}
<h1>Welcome to ${project_name}</h1>
<p>${description}</p>
{% endblock %}
"""
        return self.render_template(
            template,
            project_name=project_info["name"].title(),
            description=project_info["description"],
        )

    def generate_dot_env_file(self) -> str:
        """
        Generate .env file content.

        :return: Content of .env file
        """
        return """FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
"""

    def generate_style_file(self) -> str:
        """
        Generate style file content.

        :return: Content of style file
        """
        return """/* Add your custom styles here */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #00d2ff 0%, #3a47d5 100%);
    color: white;
}
.container {
    text-align: center;
    padding: 2rem;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}
p {
    font-size: 1.2rem;
    line-height: 1.6;
}
"""

    def generate_script_file(self) -> str:
        """
        Generate script file content.

        :return: Content of script file
        """
        return """// Add your custom JavaScript here
console.log('Script loaded');
"""
