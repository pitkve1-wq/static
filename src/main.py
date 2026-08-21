from textnode import TextNode, TextType
import shutil
import os
from textnode import markdown_to_html_node
from pathlib import Path


def recursive_function(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    a = os.listdir(source)
    for i in a:
        b = os.path.join(destination, i)
        c = os.path.join(source, i)
        if os.path.isfile(c):
            print(f"source is {c} and destination is {b}")
            x = shutil.copy(c, b)
        else:
            recursive_function(c, b)


def extract_title(markdown):
    b = markdown.split("\n")
    for i in b:
        if i.startswith("# "):
            a = i[2:]
            a = a.strip()
            return a
    raise Exception("No h1 header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path, "r")
    text = file.read()
    file.close()
    x = open(template_path, "r")
    text2 = x.read()
    x.close()
    a = markdown_to_html_node(text)
    b = a.to_html()
    c = extract_title(text)
    m = text2.replace("{{ Title }}", c)
    m = m.replace("{{ Content }}", b)
    u = os.path.dirname(dest_path)
    os.makedirs(u, exist_ok=True)
    file = open(dest_path, "w")
    file.write(m)
    file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            a = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, a)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


def main():
    destination = "public"
    if os.path.exists(destination):
        shutil.rmtree(destination)
    source = "static"
    recursive_function(source, destination)
    dest_path = "public"
    template_path = "template.html"
    from_path = "content"
    generate_pages_recursive(from_path, template_path, dest_path)


main()
