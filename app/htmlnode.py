class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, probs=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.probs = probs

    def to_html(self):
        raise NotImplementedError

    def probs_to_html(self) -> str:
        if self.probs:
            return " ".join([f'{key}="{value}"' for key, value in self.probs.items()])

        return ""

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, probs={self.probs})"


class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, probs=None):
        super().__init__(tag=tag, value=value, probs=probs)

    def to_html(self):
        if not self.value:
            raise ValueError

        if not self.tag:
            return self.value

        probs_space = " " if self.probs else ""
        return f"<{self.tag}{probs_space}{self.probs_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, probs=None):
        self.tag = tag
        self.children = children
        self.probs = probs

    def to_html(self):
        if not self.tag:
            raise ValueError("there is no tag (required)")

        if not self.children:
            raise ValueError("this is a prent node, it should have children")

        probs_space = " " if self.probs else ""
        html = f"<{self.tag}{probs_space}{self.probs_to_html()}>"

        for node in self.children:
            html += node.to_html()

        html += f"</{self.tag}>"
        return html
