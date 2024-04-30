class ChapterNotFoundException(Exception):
    """The exception is thrown when a parser can't find the latest chapter of a novel."""

    def __init__(self):
        self.msg = "No chapter number found"

class MissingParserException(Exception):
    """The exception is thrown when no parser applies to a given novel."""

    def __init__(self):
        self.msg = "Missing parser"

class NcodeNotFoundException(Exception):
    """The exception is thrown when the ncode is not found in the url."""

    def __init__(self):
        self.msg = "Ncode not found"