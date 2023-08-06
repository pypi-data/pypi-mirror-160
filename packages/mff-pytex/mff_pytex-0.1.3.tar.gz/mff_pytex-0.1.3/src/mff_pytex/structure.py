"""Module containing basic structure of file."""

from datetime import date
from typing import Any, Optional


TEMPLATE = "path_to_template"


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


class TexFile:
    """Basic TeX file structure.

    Attributes:
        file_path (str): Path to initialized file.
        preamble (Preamble): Preamble of file.
        body (Body): Body of a file.
    """

    def __init__(self, file_path: Optional[str] = None) -> None:
        """Initialize TexFile

        Args:
            file_path (str | None): Path to initialized file. If None, than use blank template.
        """
        if file_path is None:
            file_path = TEMPLATE

        self.file_path = file_path
        self._load_doc()

    def _load_doc(self) -> None:
        """Load pytex document by source .tex file.
        """
        pass

    def _print_doc(self, path: str) -> None:
        """Prints pytex document to .tex file. """
        pass

    def _create_pdf(self, path: str) -> None:
        """Create pdf file from pytex document. """
        pass


class Preamble:
    """Preamble contains basic info about author and document.

    Attributes:
        title (str): Title of document
        author (str): Author's name
        date (date): Date of creation of document
    """
    def __init__(self,
                 title: Optional[str] = None,
                 author: Optional[str] = None,
                 date: Optional[date] = None) -> None:
        """Initialize Preamble

        Args:
            title (str): Title of document, defaults None
            author (str): Author's name, defaults None
            date (date): Date of creation of document, defaults None
        """
        self.title = title
        self.author = author
        self.date = date


class Figure:
    """Basic figure structure.

    Attributes:
        fig_type (str): Type of figure
        _text (str): Content of figure,
    """

    def __init__(self, fig_type: str, *params: str) -> None:
        """Initialize Figure.

        Args:
            fig_type (str): Type of figure
        """
        self._text = ""
        self.fig_type = fig_type
        self.write(command('begin', self.fig_type))

    def __str__(self) -> str:
        """Returns content string encapsuled by figure.

        Returns:
            str: Content
        """
        return self._text + command('end', self.fig_type)

    def _writeline(self, text: str) -> None:
        """Write single line to the TeX file.

        Args:
            text (str): Line of text intended for insert to content.
        """
        self._text += f"{text}\n"

    def write(self, *lines: str) -> None:
        """Write multiple lines to the TeX file.

        Args:
            *lines (str): Lines of text intended for insert to content.
        """
        for line in lines:
            self._writeline(line)

    def add(self, figure: Any) -> None:
        """Writes figure to the TeX file.

        Args:
            figure (Any): Figure to use.
        """
        self.write(str(figure))

    def usepackage(self, pkg: str, *params: str) -> None:
        """Add a usepackage command to the TeX file. Optional params can be used.

        Args:
            pkg (str): Package to use
            *params (str): Optional parameters for package
        """
        self.write(command('usepackage', pkg, *params))

    def usepackages(self, *pkgs: str) -> None:
        """Add a usepackage command to the TeX file. Can be used for multiple packages.

        Args:
            *pkgs (str): Packages to use, can be multiple of them.
        """
        for pkg in pkgs:
            self.usepackage(pkg)

    def math(self, formula: str) -> None:
        self.write(f"\\[ {formula} \\]")


class Document(Figure):
    """Content of document."""

    def __init__(self) -> None:
        """Initialize document.
        """
        self._text = ""
        self.fig_type = "document"
        self.write(command('begin', self.fig_type))

    def tableofcontents(self) -> None:
        """Add a tableofcontents command to the TeX file."""
        self.write(command('tableofcontents'))

    def maketitle(self) -> None:
        """Add a maketitle command to the TeX file."""
        self.write(command('maketitle'))

    def newpage(self) -> None:
        """Add a newpage command to the TeX file."""
        self.write(command('newpage'))

    def clearpage(self) -> None:
        """Add a clearpage command to the TeX file."""
        self.write(command('clearpage'))


class Table(Figure):
    pass
