from textnode import TextNode, TextType
import shutil
import os
from textnode import markdown_to_html_node
from pathlib import Path
import sys


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


def generate_page(from_path, template_path, dest_path, basepath):
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
    m = m.replace('href="/', f'href="{basepath}')
    m = m.replace('src="/', f'src="{basepath}')
    u = os.path.dirname(dest_path)
    os.makedirs(u, exist_ok=True)
    file = open(dest_path, "w")
    file.write(m)
    file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            a = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, a, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    destination = "docs"
    if os.path.exists(destination):
        shutil.rmtree(destination)
    source = "static"
    recursive_function(source, destination)
    dest_path = "docs"
    template_path = "template.html"
    from_path = "content"
    generate_pages_recursive(from_path, template_path, dest_path, basepath)


main()
