from enum import Enum


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    TEXT = "text"
    UNKNOWN = "unknown"


class TextNode:

    def __init__(self, text=None, text_type: Enum = None, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        text_eq = self.text == other.text
        test_type_eq = self.text_type == other.text_type
        url_eq = self.url == other.url
        if all([text_eq, test_type_eq, url_eq]):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

