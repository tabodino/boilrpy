class Config:
    """
    BoilrPy configuration class.
    """
    def __init__(self):
        self.available_licenses = ["MIT", "Apache", "GPL", "BSD", "None"]
        self.use_camel_case = False  # 'camelCase' or 'snake_case'
        self.charset = "utf-8"
        self.default_version = "0.1.0"
        self.python_version = "3.11"

    def get_available_licenses(self) -> list:
        """ Returns a list of available licenses. """
        return self.available_licenses

    def get_use_camel_case(self) -> bool:
        """ Returns whether to use camelCase or snake_case. """
        return self.use_camel_case

    def get_charset(self) -> str:
        """ Returns the charset. """
        return self.charset

    def get_default_version(self) -> str:
        """ Returns the default version. """
        return self.default_version
