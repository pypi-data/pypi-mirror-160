"""frame range section in the UI."""

import hou
from ciohoudini import payload

def resolve_payload(node):
    title = node.parm("title").eval().strip()
    return {"job_title": title}


# def on_change(node, **kwargs):
#     """
#     """
#     payload.resolve()
#     resolve(node)
