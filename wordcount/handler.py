import json
from .wordcount import process_text


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    return json.dumps(process_text(req))
