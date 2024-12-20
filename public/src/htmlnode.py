import re
import typing as t
from textnode import TextType, TextNode


class HTMLNode:

    def __init__(self, tag: t.Optional[str] = None, value: t.Optional[str] = None,
                 children: t.Optional[t.List] = None, props: t.Optional[dict] = None):
        self.tag = tag # An HTMLNode w/o a tag will render to raw text
        self.value = value # An HTMLNode w/o a value will be assumed to have children
        self.children = children # An HTMLNode w/o children will be assume to have a value
        self.props = props # An HTMLNode w/o props won't have any attributes

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return "".join(f' {k}="{v}"' for k, v in self.props.items()) if self.props else ""


class LeafNode(HTMLNode):

    def __init__(self, tag: t.Optional[str] = None, value: t.Optional[str] = None,
                 props: t.Optional[dict] = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode should have a value")
        if self.tag is None:
            return self.value
        return '<' + self.tag + self.props_to_html() + '>' + self.value + f'</{self.tag}>'


class ParentNode(HTMLNode):

    def __init__(self, tag: t.Optional[str] = None, children: t.Optional[t.List] = None,
                 props: t.Optional[dict] = None):
        super().__init__(tag=tag, props=props, children=children)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode should have a tag")

        if self.children is None:
            raise ValueError("ParentNode should have children")

        parent_html = '<' + self.tag + self.props_to_html() + '>'
        for child in self.children:
            parent_html += "".join(child.to_html())
        parent_html += f'</{self.tag}>'

        return parent_html


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag= "b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag= "i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag= "code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag= "a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag= "img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Unsupported TextType: {text_node}")


if __name__ == "__main__":
    print('yo')
