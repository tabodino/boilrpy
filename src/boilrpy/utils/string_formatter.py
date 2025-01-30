import re


class StringFormatter:
    """
    A utility class for formatting strings.
    """

    @staticmethod
    def to_camel_case(string: str) -> str:
        """
        Convert a string to camelCase.

        Args:
            string (str): The input string.

        Returns:
            str: The string in camelCase format.
        """
        if re.match(r"^[a-z][a-zA-Z0-9]*$", string):
            return string
        if re.match(r"^[A-Z][a-zA-Z0-9]*$", string):
            return string[0].lower() + string[1:]
        words = re.findall(r"[A-Za-z0-9]+", string)
        return words[0].lower() + "".join(word.capitalize() for word in words[1:])

    @staticmethod
    def to_snake_case(string: str) -> str:
        """
        Convert a string to snake_case.

        Args:
            string (str): The input string.

        Returns:
            str: The string in snake_case format.
        """
        string = string.strip()
        if re.match(r"^[a-z0-9_]+$", string):
            return string
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
        return re.sub("[^a-z0-9]+", "_", s2.lower())

    @staticmethod
    def format_project_name(project_name: str, use_camel_case: bool) -> str:
        """
        Format a project name to either camelCase or snake_case.

        Args:
            project_name (str): The input project name.
            use_camel_case (bool): Whether to use camelCase or snake_case.

        Returns:
            str: The formatted project name.
        """
        if use_camel_case:
            return StringFormatter.to_camel_case(project_name)
        return StringFormatter.to_snake_case(project_name)
