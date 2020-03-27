import html
from typing import Dict


def build_html_text(title: str = "", body: str = "") -> str:
    """Build a basic html page.

    Args:
        title (str): Title used in the HTML <head><title> tag
        body (str): Content of the <body> HTML tag
    Returns:
        HTML string.
    """
    indented_body = "\n    ".join(body.split("\n"))

    text_html = """\
<!DOCTYPE html>
<html>
  <head>
    <title>{title}</title>
  </head>
  <body>
    {body}
  </body>
</html>
""".format(
        title=title, body=indented_body
    )
    return text_html


def dicts_to_anchors(d: Dict[str, Dict]) -> str:
    """Convert a dictionary to an HTML list of anchors.

    Example:
        The following dict:
        {
            "foo" : {
                "href": "http://foo.org"
            },
            "bar": {
                "href": "http://bar.org",
                "color": "blue"
            }
        }
        Will be converted to:
        <a href="http://foo.org"> foo </a><br/>
        <a href="http://bar.org" color="blue"> bar </a><br/>

    """
    response = ""
    for package_name, attributes in d.items():
        for a, b in attributes.items():
            print("MMMMMMMMMMMM", a, b)
        string_attributes = " ".join(
            [f'{a}="{html.escape(b)}"' for a, b in attributes.items()]
        )
        response = response + f"<a {string_attributes}>{package_name}</a><br/>\n"
    return response
