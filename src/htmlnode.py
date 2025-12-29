from utils import TextType, VoidTags

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def __eq__(self, other):
        return (
            isinstance(other, HTMLNode) and
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def to_html(self):
        raise NotImplementedError("to_html method is not implemented yet.")

    def props_to_html(self):
        props_str = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
        return props_str

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, props={self.props}, children={self.children})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=[], props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value to render HTML.")
        if not self.tag:
            return f"{self.value}"
        # If self.tag exists, generate the HTML string
        props_str = self.props_to_html()

        if self.tag in VoidTags: # Void tags do not have closing tags
            return f"<{self.tag}{' ' + props_str if props_str else ''}/>"
        return f"<{self.tag}{' ' + props_str if props_str else ''}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, props=props)
        self.children = children  

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to render HTML.")
        if self.children is None:
            raise ValueError("ParentNode must have children to render HTML.")
        opening_tag = f"<{self.tag}{' ' + self.props_to_html() if self.props else ''}>"
        closing_tag = f"</{self.tag}>"
        children_html = ''.join(child.to_html() for child in self.children)
        return f"{opening_tag}{children_html}{closing_tag}"