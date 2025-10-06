import argparse
from boilrpy.cli import CLI
from boilrpy.config import Config
from boilrpy.project_creator import ProjectCreator
from boilrpy.dependency_creators.checker import DependencyManagerChecker


def run_cli(args):
    """Run the CLI with given arguments."""
    if args.check_deps:
        DependencyManagerChecker.print_status()
        return

    config = Config()
    cli = CLI(config)
    project_info = cli.gather_project_info()
    creator = ProjectCreator(config)
    creator.create_project(project_info)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Boilrpy - Python Project Boilerplate Generator"
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check which dependency managers are installed",
    )
    args = parser.parse_args()
    run_cli(args)


if __name__ == "__main__":  # pragma: no cover
    main()
