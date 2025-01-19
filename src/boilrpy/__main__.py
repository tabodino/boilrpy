from boilrpy.cli import CLI
from boilrpy.config import Config
from boilrpy.project_creator import ProjectCreator


def main():
    """CLI entry point."""
    config = Config()
    cli = CLI(config)
    project_info = cli.gather_project_info()
    creator = ProjectCreator(config)
    creator.create_project(project_info)


if __name__ == "__main__":  # pragma: no cover
    main()
