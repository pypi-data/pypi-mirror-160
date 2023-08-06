"""Module containing basic structure of file."""

from datetime import date
from typing import Any


TEMPLATE = "path_to_template"


class TexFile:
    """Basic TeX file structure.

    Attributes:
        file_path (str): Path to initialized file.
        header (Header): Header of file.
        body (Body): Body of a file.
    """

    def __init__(self, file_path: str | None = None) -> None:
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


class Header:
    """Header contains basic info about author and document.

    Attributes:
        title (str): Title of document
        author (str): Author's name
        date (date): Date of creation of document
    """
    def __init__(self,
                 title: str | None = None,
                 author: str | None = None,
                 date: date | None = None) -> None:
        """Initialize Header

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
        __text (str): Content of figure,
    """

    def __init__(self, fig_type: str) -> None:
        """Initialize Figure.

        Args:
            fig_type (str): Type of figure
        """
        self.__text = ""
        self.fig_type = fig_type
        self.writeline(f"\\begin{fig_type}")

    def __str__(self) -> str:
        """Returns content string encapsuled by figure.

        Returns:
            str: Content
        """
        return self.__text + self.fig_type

    def writeline(self, text: str) -> None:
        """Write single line in content.

        Args:
            text (str): Line of text intended for insert to content.
        """
        self.__text += f"{text}\n"

    def write(self, *lines: str) -> None:
        """Write multiple lines in content.

        Args:
            *lines (str): Lines of text intended for insert to content.
        """
        for line in lines:
            self.writeline(line)

    def add(self, figure: Any) -> None:
        """Writes figure to content.

        Args:
            figure (Any): Figure intended for insert to content.
        """
        self.writeline(str(figure))
