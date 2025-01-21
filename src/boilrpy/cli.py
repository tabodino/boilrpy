from colorama import Fore, Style
from boilrpy.input_validator import InputValidator
from boilrpy.decorators.color_decorator import ColorDecorator

class CLI:
    """
    CLI class to gather input from the user.
    """
    def __init__(self, config):
        self.config = config

    def gather_project_info(self) -> dict:
        """
        Gather project information from the user.

        Returns:
            dict: Dictionary containing project information.
        """
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Welcome to boilrpy Project Creator!{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}Please provide the following information for your new project:"
            f"{Style.RESET_ALL}\n")
        project_info = {}
        project_info["name"] = self._get_valid_input(
            "Enter project name: ",
            InputValidator.validate_project_name)

        project_info["description"] = input(f"{Fore.GREEN}Project description: {Style.RESET_ALL}")
        project_info["version"] = self._get_valid_input(
            "Enter project version [0.1.0]: ",
            InputValidator.validate_version)
        project_info["author"] = input(f"{Fore.GREEN}Author name: {Style.RESET_ALL}") or ""
        project_info["license"] = self._choose_license()

        project_info["use_poetry"] = self._yes_no_question(
            "Use Poetry for dependency management? (y/n) [n]: ", "n"
        )
        project_info["use_docker"] = self._yes_no_question(
            "Generate Dockerfile? (y/n) [y]: ", "y"
        )
        project_info["create_tests"] = self._yes_no_question(
            "Create a test folder? (y/n) [y]: ", "y"
        )
        project_info["use_pylint"] = self._yes_no_question(
            "Use pylint in project? (y/n) [n]: ", "n"
        )
        self._display_summary(project_info)
        return project_info


    def _get_valid_input(self, prompt: str, validator: callable) -> str:
        while True:
            value = input(prompt)
            if validator(value):
                return value
            self.display_error("Invalid input. Please try again.")

    def _choose_license(self) -> str:
        licenses = self.config.get_available_licenses()
        print(f"\n{Fore.YELLOW}Available licenses:{Style.RESET_ALL}")
        for i, lic in enumerate(licenses, 1):
            print(f"{Fore.CYAN}{i}. {lic}{Style.RESET_ALL}")
        while True:
            choice = input("Choose a license (enter the number): ")
            try:
                index = int(choice) - 1
                if 0 <= index < len(licenses):
                    return licenses[index]
            except ValueError:
                pass
            self.display_error("Invalid choice. Please try again.")

    def _yes_no_question(self,
                         question: str,
                         default_response: str = None) -> bool:

        default_hint = f" [{default_response}]" if default_response else ""

        while True:
            answer = input(f"{question} (y/n){default_hint}: ").strip().lower()
            if not answer and default_response:
                answer = default_response.lower()
            if answer in ["y", "yes"]:
                return True
            if answer in ["n", "no"]:
                return False
            self.display_error("Invalid input. Please enter 'y' or 'n'.")

    @ColorDecorator.color_output(Fore.BLUE)
    def _display_summary(self, project_info: dict):
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Project Summary:{Style.RESET_ALL}")
        for key, value in project_info.items():
            print(f"{Fore.YELLOW}{key.capitalize()}: {Fore.WHITE}{value}")
        print("\n")

    @ColorDecorator.color_output(Fore.RED)
    def display_error(self, message: str):
        """Display an error message."""
        print(f"{Fore.RED}✘ Error: {message}{Style.RESET_ALL}")
