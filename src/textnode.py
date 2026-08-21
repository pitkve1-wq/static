from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
import re
import os
import shutil


class TextType(Enum):
    LINK = "link"
    TEXT = "text"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        else:
            return False

    def __repr__(self):
        a = f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return a


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if TextType.TEXT == text_node.text_type:
        return LeafNode(None, text_node.text)
    elif TextType.BOLD == text_node.text_type:
        return LeafNode("b", text_node.text)
    elif TextType.ITALIC == text_node.text_type:
        return LeafNode("i", text_node.text)
    elif TextType.CODE == text_node.text_type:
        return LeafNode("code", text_node.text)
    elif TextType.LINK == text_node.text_type:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif TextType.IMAGE == text_node.text_type:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("cannot be empty")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    flist = []
    for i in old_nodes:
        if i.text_type != TextType.TEXT:
            flist.append(i)
            continue
        a = i.text.split(delimiter)
        for m, x in enumerate(a):
            if x == "":
                continue
            elif m % 2 == 0:
                c = TextNode(x, TextType.TEXT)
                flist.append(c)
            else:
                c = TextNode(x, text_type)
                flist.append(c)
        if len(a) % 2 == 0:
            raise Exception("is not closed properly")
    return flist


def extract_markdown_images(text):
    a = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return a


def extract_markdown_links(text):
    d = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return d


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    flist = []
    for i in old_nodes:
        if i.text_type != TextType.TEXT:
            flist.append(i)
            continue
        k = extract_markdown_images(i.text)
        if len(k) == 0:
            flist.append(i)
            continue
        og = i.text
        for h in k:
            a = og.split(f"![{h[0]}]({h[1]})", 1)
            if len(a) != 2:
                raise Exception("the markdown wasnt closed properly")
            if a[0] != "":
                n = TextNode(a[0], TextType.TEXT)
                flist.append(n)
            c = TextNode(h[0], TextType.IMAGE, h[1])
            flist.append(c)
            og = a[1]
        if og != "":
            j = TextNode(og, TextType.TEXT)
            flist.append(j)
    return flist


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    flist = []
    for i in old_nodes:
        if i.text_type != TextType.TEXT:
            flist.append(i)
            continue
        k = extract_markdown_links(i.text)
        if len(k) == 0:
            flist.append(i)
            continue
        og = i.text
        for h in k:
            a = og.split(f"[{h[0]}]({h[1]})", 1)
            if len(a) != 2:
                raise Exception("the markdown wasnt closed properly")
            if a[0] != "":
                n = TextNode(a[0], TextType.TEXT)
                flist.append(n)
            c = TextNode(h[0], TextType.LINK, h[1])
            flist.append(c)
            og = a[1]
        if og != "":
            j = TextNode(og, TextType.TEXT)
            flist.append(j)
    return flist


def text_to_textnodes(text):
    v = []
    a = TextNode(text, TextType.TEXT)
    v.append(a)
    b = split_nodes_delimiter(v, "**", TextType.BOLD)
    b = split_nodes_delimiter(b, "_", TextType.ITALIC)
    b = split_nodes_delimiter(b, "`", TextType.CODE)
    c = split_nodes_image(b)
    n = split_nodes_link(c)
    return n


def markdown_to_blocks(markdown):
    blocks = []
    parts = markdown.split("\n\n")
    for i in parts:
        a = i.strip()
        if a == "":
            continue
        blocks.append(a)
    return blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown):
    parts = markdown.split("\n")
    prefixes = ["# ", "## ", "### ", "#### ", "##### ", "###### "]
    for pre in prefixes:
        if markdown.startswith(pre):
            return BlockType.HEADING
        else:
            continue
    match = True
    for i in parts:
        code_pre = "```\n"
        code_pre2 = "```"
        if not markdown.startswith(code_pre) or not markdown.endswith(code_pre2):
            match = False
            break
    if match:
        return BlockType.CODE
    match = True
    for i in parts:
        quote_pre = ">"
        if not i.startswith(quote_pre):
            match = False
            break
    if match:
        return BlockType.QUOTE
    match = True
    for i in parts:
        un_pre = "- "
        if not i.startswith(un_pre):
            match = False
            break
    if match:
        return BlockType.UNORDERED_LIST
    match = True
    num = 1
    for i in parts:
        or_pre = f"{num}. "
        if i.startswith(or_pre):
            num += 1
        else:
            match = False
    if match:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def text_to_children(text):
    text_n = text_to_textnodes(text)
    c = []
    for text_node in text_n:
        c.append(text_node_to_html_node(text_node))
    return c


def paragraph_to_html_node(block):
    a = block.split("\n")
    b = " ".join(a)
    c = text_to_children(b)
    d = ParentNode("p", c)
    return d


def code_to_html_node(block):
    blocka = block.strip("`").lstrip("\n")
    b = TextNode(blocka, TextType.TEXT)
    d = text_node_to_html_node(b)
    a = ParentNode("code", [d])
    return ParentNode("pre", [a])


def heading_to_html_node(block):
    prefixes = ["# ", "## ", "### ", "#### ", "##### ", "###### "]
    for pre in prefixes:
        if block.startswith(pre):
            c = block[len(pre) :]
            a = text_to_children(c)
            b = ParentNode(f"h{len(pre)-1}", a)
            return b
    raise Exception("invalid heading")


def quote_to_html_node(block):
    a = block.split("\n")
    c = []
    for i in a:
        if len(i) <= 1:
            m = i.strip(">")
            c.append(m)
            continue
        b = i[2:]
        c.append(b)
    x = " ".join(c)
    v = text_to_children(x)
    return ParentNode("blockquote", v)


def unordered_list_to_html_node(block):
    a = block.split("\n")
    new = []
    for i in a:
        b = i[2:]
        v = text_to_children(b)
        n = ParentNode("li", v)
        new.append(n)
    return ParentNode("ul", new)


def ordered_list_to_html_node(block):
    new = []
    num = 1
    a = block.split("\n")
    for i in a:
        or_pre = f"{num}. "
        if i.startswith(or_pre):
            b = i[len(or_pre) :]
            v = text_to_children(b)
            n = ParentNode("li", v)
            new.append(n)
            num += 1
    return ParentNode("ol", new)


def markdown_to_html_node(markdown):
    a = markdown_to_blocks(markdown)
    h = []
    for i in a:
        b = block_to_block_type(i)
        if b == BlockType.PARAGRAPH:
            x = paragraph_to_html_node(i)
            h.append(x)
        elif b == BlockType.QUOTE:
            x = quote_to_html_node(i)
            h.append(x)
        elif b == BlockType.CODE:
            v = code_to_html_node(i)
            h.append(v)
        elif b == BlockType.ORDERED_LIST:
            c = ordered_list_to_html_node(i)
            h.append(c)
        elif b == BlockType.UNORDERED_LIST:
            x = unordered_list_to_html_node(i)
            h.append(x)
        elif b == BlockType.HEADING:
            x = heading_to_html_node(i)
            h.append(x)
    return ParentNode("div", h)


def recursive_function(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    a = os.listdir(source)
    for i in a:
        b = os.path.join(destination, i)
        c = os.path.join(source, i)
        if os.path.isfile(c):
            x = shutil.copy(c, b)
        else:
            recursive_function(c, b)
    shutil.rmtree(destination)
