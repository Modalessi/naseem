class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, probs=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.probs = probs

    def to_html(self):
        raise NotImplementedError

    def probs_to_html(self) -> str:
        return " ".join([f'{key}="{value}"' for key, value in self.probs.items()])

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, probs={self.probs})"
