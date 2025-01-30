from colorama import Fore, Style
from boilrpy.decorators.color_decorator import ColorDecorator


def mock_input(prompt):
    return prompt


def mock_output(message):
    return message


def test_color_input_with_args():
    @ColorDecorator.color_input(Fore.RED)
    def mock_input(prompt):
        return prompt

    result = mock_input("Project name: ")
    expected = f"{Fore.RED}Project name: {Style.RESET_ALL}"
    assert result == expected


def test_color_input_with_no_args_or_kwargs():
    @ColorDecorator.color_input(Fore.YELLOW)
    def mock_input(*args, **kwargs):
        return ""

    result = mock_input()
    expected = ""
    assert result == expected


def test_color_input_default_color():
    @ColorDecorator.color_input()
    def mock_input(prompt):
        return prompt

    result = mock_input("Enter your email: ")
    expected = f"{Fore.GREEN}Enter your email: {Style.RESET_ALL}"
    assert result == expected


def test_color_output_with_args():
    @ColorDecorator.color_output(Fore.RED)
    def mock_output(message):
        return message

    result = mock_output("Hello, World!")
    expected = f"{Fore.RED}Hello, World!{Style.RESET_ALL}"
    assert result == expected
