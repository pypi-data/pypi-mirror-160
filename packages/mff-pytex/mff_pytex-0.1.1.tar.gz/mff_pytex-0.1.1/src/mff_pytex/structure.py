"""Main module."""

TEMPLATE = "path_to_template"

def test_docs(hello: str) -> str:
    """Test Docs

    Testing how docs writing works

    Args:
        hello (str): String which should be printed

    Returns:
        str: Printed string
    """

    print(hello)
    return hello


class TexFile:

    def __init__(self, file_path: str | None = None) -> None:
        if file_path is None:
            file_path = TEMPLATE

        self.file_path = file_path
