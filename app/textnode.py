class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object) -> bool:

        if not isinstance(value, TextNode):
            return False

        text_equality = self.text == value.text
        text_type_equality = self.text_type == value.text_type
        url_equality = self.url == value.url

        return text_equality and text_type_equality and url_equality

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
