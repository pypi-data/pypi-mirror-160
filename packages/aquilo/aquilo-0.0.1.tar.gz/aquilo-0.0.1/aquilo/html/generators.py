from typing import Union, Iterable, Callable

from aquilo.browser.elements import Element


def build(element_tree: Callable, title: str = None, description: str = None) -> str:
    """
    It takes an element tree and returns an HTML document

    :param element_tree: str
    :type element_tree: str
    :param title: The title of the page
    :type title: str
    :param description: str = None
    :type description: str
    :return: A string of HTML code.
    """
    html: str = f"""
<!DOCTYPE html><html lang="en"><head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head><body>{element_tree()}</body></html>
        """
    return html


def get_404():
    return """
<!doctype html>
<html lang="en">
<head>
  <title>Not Found</title>
</head>
<body>
  <h1>Not Found</h1><p>The requested resource was not found on this server.</p>
</body>
</html>
""".encode()


def generate_dom_tree(root: Union[Iterable, Element]) -> str:
    """
    It takes a root element, and returns a string representation of the DOM tree

    :param root: The root element of the DOM tree
    :type root: Union[Iterable, Element]
    :return: A string of HTML code.
    """
    element_tree = ["<div>"]

    for tag in root:
        try:
            iter(tag)
            is_iterable = True
        except TypeError:
            is_iterable = False

        if is_iterable:
            for i in tag:
                element_tree.append(i())
        else:
            element_tree.append(tag())

    element_tree.append("</div>")

    return "".join(element_tree)
