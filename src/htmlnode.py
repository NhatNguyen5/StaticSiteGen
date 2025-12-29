class HTMLNode:
    def __init__(self, tag, value=None, children=None, props=None):
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

    def add_child(self, child_node):
        self.children.append(child_node)

    def set_attribute(self, key, value):
        self.props[key] = value

    def get_attribute(self, key):
        return self.props.get(key)

    def to_html(self):
        """ if self.value is not None:
            return f"<{self.tag} {self.props}>{self.value}</{self.tag}>"
        else:
            html = f"<{self.tag} {self.props}>"
            for child in self.children:
                html += child.to_html()
            html += f"</{self.tag}>"
            return html """
        raise NotImplementedError("to_html method is not implemented yet.")

    def props_to_html(self):
        props_str = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
        return props_str

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, props={self.props}, children={self.children})"
    