class Exception404(Exception):
    """The exception for a 404 error from a request"""
    def __init__(self):
        self.args = ("404",)

class TitleNotFoundException(Exception):
    """The exception is thrown when a parser can't find the title of a novel"""
    def __init__(self):
        self.args = ("No title found",)

class ChapterNotFoundException(Exception):
    """The exception is thrown when a parser can't find the latest chapter of a novel"""
    def __init__(self):
        self.args = ("No chapter number found",)