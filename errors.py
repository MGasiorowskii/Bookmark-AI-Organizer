class EnvError(Exception):
    def __str__(self):
        return warning(self.args[0])


class ProcessingError(Exception):
    def __str__(self):
        return error(self.args[0])


def error(message: str) -> str:
    """Prints an error message in red color."""
    return f"\033[91m{message}\033[0m"


def warning(message: str) -> str:
    """Prints a warning message in yellow color."""
    return f"\033[93m{message}\033[0m"
