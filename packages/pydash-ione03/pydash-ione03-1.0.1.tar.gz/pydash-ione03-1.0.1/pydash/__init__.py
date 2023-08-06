class PyDash:
    def __init__(self):
        pass

    @staticmethod
    def lower(string: str):
        """
        Converts a string to lowercase
        """
        return string.lower()

    @staticmethod
    def upper(string: str):
        """
        Converts a string to uppercase
        """
        return string.upper()

    @staticmethod
    def title(string: str):
        """
        Converts a string to titlecase
        """
        return string.title()

    @staticmethod
    def kebab(string: str):
        """
        Converts a string to kebabcase
        """
        return string.replace(" ", "-").lower()