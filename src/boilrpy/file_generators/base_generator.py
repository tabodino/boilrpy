from abc import ABC, abstractmethod
from string import Template
from boilrpy.config import Config


class BaseGenerator(ABC):
    """
    Abstract base class for file generators.
    """

    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def generate(self, *args, **kwargs) -> str:
        """
        Generate the file content.
        """

    def render_template(self, template: str, **kwargs) -> str:
        """
        Render a template with the given kwargs.
        """
        return Template(template).safe_substitute(**kwargs)
