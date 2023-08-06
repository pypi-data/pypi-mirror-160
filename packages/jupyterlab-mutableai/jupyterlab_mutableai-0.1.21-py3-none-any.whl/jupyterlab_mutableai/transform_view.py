from importlib.resources import path
import json
import requests
import tornado
import threading
from uuid import uuid4

from io import BytesIO
from jupyter_server.base.handlers import APIHandler
import base64
import tempfile

TRANSFORM_NB_ROUTE = "TRANSFORM_NB"


def create_file_packet(nb_filename: str) -> dict:
    """Create a file packet for the transform docker container
    Args:
      filename: the name of the file to be sent to the transform docker container
    Returns:
      A dict that is the file packet for the transform docker container
    """
    f = open(nb_filename, "rb").read()
    data = {
        "file_name": nb_filename,
        "file_data": base64.b64encode(f).decode("utf-8"),
    }
    return data


def call_transform_nb(
    filename: str, api_key: str, domain: str, mode: str, instruction: str = ""
) -> dict:
    """Call the transform docker container
    Args:
      filename: the name of the file to be sent to the transform docker container
    Returns:
      A dict that is the response from the transform docker container
    """
    data = create_file_packet(filename)
    data["mode"] = mode
    data["response_type"] = "FILE"

    if instruction:
        data["instruction"] = instruction
    url = "https://" + domain + "/" + TRANSFORM_NB_ROUTE
    response = requests.post(
        url=url,
        json=data,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
        },
    )
    return response


def threaded_transform(input_data, tmp_name: str):
    nb_filename = input_data["name"]
    instruction = input_data.get("instruction", "")

    api_key, domain, mode = (
        input_data["apiKey"],
        input_data["transformDomain"],
        input_data["mode"],
    )

    response = call_transform_nb(nb_filename, api_key, domain, mode, instruction)
    json_response = response.json()

    tar_file_content = base64.b64decode(json_response["file_data"]).decode("utf-8")
    with open(tmp_name, "w") as f:
        f.write(tar_file_content)


class TransformJupyterRouteHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):
        self.finish(
            json.dumps({"data": "This is /jlab-ext-example/TRANSFORM_NB endpoint!"})
        )

    @tornado.web.authenticated
    def post(self):

        # input_data is a dictionary with a key "name"
        input_data = self.get_json_body()

        nb_filename = input_data["name"]

        # get dirname of nb_filename
        with tempfile.NamedTemporaryFile() as tmp:
            x = threading.Thread(target=threaded_transform, args=(input_data, tmp.name))
            x.start()
            self.finish(
                json.dumps(
                    {
                        "message": "processing transformation",
                        "file_path": tmp.name,
                    }
                )
            )
