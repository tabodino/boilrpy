from functools import wraps
from colorama import init, Fore, Style

init(autoreset=True)


class ColorDecorator:
    """Decorator to color input and output messages."""
    @staticmethod
    def color_input(color=Fore.GREEN):
        """Decorator to color input messages."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                prompt = args[0] if args else kwargs.get("prompt", "")
                colored_prompt = f"{color}{prompt}{Style.RESET_ALL}"
                return func(colored_prompt, *args[1:], **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def color_output(color=Fore.GREEN):
        """Decorator to color output messages."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                message = args[0] if args else kwargs.get("message", "")
                colored_message = f"{color}{message}{Style.RESET_ALL}"
                return func(colored_message, *args[1:], **kwargs)
            return wrapper
        return decorator
