import re
import typing as t
from pprint import pprint
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def their_split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def their_split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def my_split_nodes_delimiter(old_nodes: list, delimeter: str, text_type: TextType):
    new_nodes = []

    if delimeter == "*":
        new_text_type = TextType.ITALIC
    elif delimeter == "**":
        new_text_type = TextType.BOLD
    elif delimeter == "`":
        new_text_type = TextType.CODE
    else:
        raise Exception(f"Unsupported delimeter: '{delimeter}'")

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        del_open = False
        build_text = ""
        delim_match_text = ""
        delimeter_agg = ""

        for ch in node.text:
            if ch in delimeter:
                delimeter_agg += ch
            if ch == delimeter and not del_open or delimeter_agg == delimeter and not del_open:
                del_open = True
                delimeter_agg = ""
                new_nodes.append(TextNode(build_text, text_type=TextType.TEXT))
                continue
            if del_open and delimeter_agg in delimeter and ch not in delimeter_agg:
                delim_match_text += ch
            if not del_open and delimeter_agg in delimeter and ch not in delimeter_agg:
                build_text += ch
            if delimeter_agg == delimeter and del_open:
                del_open = False
                new_nodes.append(TextNode(delim_match_text, text_type=new_text_type))
                delim_match_text = ""
                build_text = ""
                delimeter_agg = ""
        if del_open:
            raise Exception(f"Matching closing delimeter {delimeter} not found in {node.text}")
        if build_text:
            new_nodes.append(TextNode(build_text, text_type=TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    img_expr = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    img_matches = re.findall(img_expr, text)
    return img_matches

def extract_markdown_links(text):
    link_expr = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    link_matches = re.findall(link_expr, text)
    return link_matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = node.text
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections_list = sections.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections_list) != 2:
                raise ValueError(f"Invalid markdown, link section not closed: {sections}")
            if sections_list[0] != "":
                new_nodes.append(TextNode(sections_list[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            sections = sections_list[1]
        if sections != "":
            new_nodes.append(TextNode(sections, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = node.text
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections_list = sections.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections_list) != 2:
                raise ValueError(f"Invalid markdown, link section not closed: {sections}")
            if sections_list[0] != "":
                new_nodes.append(TextNode(sections_list[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            sections = sections_list[1]
        if sections != "":
            new_nodes.append(TextNode(sections, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    return new_nodes


def markdown_to_blocks(markdown):
    markdown_blocks = []
    for block in markdown.split("\n\n"):
        if block == "":
            continue
        markdown_blocks.append(block.strip())
    return markdown_blocks


def block_to_block_type(block: str):
    lines = block.split("\n")
    # Headings start with 1-6 # characters, followed by a space, then the heading text
    if re.match(r"^#+\s", block):
        return "heading"
    # Code blocks must start with 3 backticks and end with 3 backticks
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"
    # Every line in a quote block must start with a > character
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    # every line in an unordered list block must start with a * or - character followed by a space
    elif re.match(r"[*-]\s", block):
        for idx, line in enumerate(lines):
            if not re.match(r"[*-]\s", lines[idx]):
                return "paragraph"
        return "unordered_list"
    # Every line in an ordered list block must start with a number followed by a . character and a space
    elif re.match(r"\d+\.\s", block):
        for idx, line in enumerate(lines):
            if not re.match(r"\d+\.\s", lines[idx]):
                return "paragraph"
        return "ordered_list"
    # If non of the above then it is a normal paragraph
    else:
        return "paragraph"


if __name__ == "__main__":
    code_block = "```\nx = 'Hello World\nprint(x)\n```"
    value = block_to_block_type(code_block)
    print(value)
