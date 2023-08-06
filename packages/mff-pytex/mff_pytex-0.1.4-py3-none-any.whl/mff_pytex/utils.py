"""Basic utils for work with LaTeX documents."""


from datetime import date as datum
from typing import Any, Optional
import sys
from os import path


def get_dir() -> str:
    """Returns directory where main file has been executed.

    Returns:
        str: Directory name where is main file
    """
    return str(path.dirname(str(sys.modules['__main__'].__file__)))


def get_path() -> str:
    """Returns path to main file.

    Returns:
        str: Path to main file
    """
    return str(path.abspath(str(sys.modules['__main__'].__file__)))


def command(comm: str, main: Optional[str] = None, *params) -> str:
    """Template for creating commands.

    If main is None, than return '\\command'.
    If main is not none, but any optional parameter given, than return '\\command{main}'
    If main and optional parameters given, than return '\\command[param1, param2, ...]{main}'

    Args:
        comm (str): Name of command
        main (str): Main parameter of command, defaults None
        *params (str): Optional parameters of command

    Returns:
        str: string of given command by given parameters.
    """
    if main is None:
        return f"\\{comm}"
    elif params:
        return f"\\{comm}[{', '.join(params)}]{{{main}}}"
    else:
        return f"\\{comm}{{{main}}}"
