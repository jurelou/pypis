from typing import Dict, List


def build_html_text(title: str = "", body: str = "") -> str:

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


def dicts_to_anchors(anchors: Dict[str, Dict]) -> str:
    response = ""
    for package_name, attributes in anchors.items():
        string_attributes = " ".join([f'{a}="{b}"' for a, b in attributes.items()])
        response = response + f"<a {string_attributes}>{package_name}</a><br/>\n"
    return response
