import json
import os
import tornado
import nbformat
from jupyter_server.base.handlers import APIHandler
import traceback


def check_transformation_exists(file_path: str):
    """
    Check the tempfile if it exists.
    """
    try:
        with open(file_path) as f:
            if f.read():
                return True
        return None
    except Exception as ex:
        return None


class CheckStatusRouterHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):
        self.finish(
            json.dumps({"data": "This is /jlab-ext-example/TRANSFORM_NB endpoint!"})
        )

    @tornado.web.authenticated
    def post(self):
        input_data = self.get_json_body()
        file_path = input_data["file_path"]
        ext = input_data["ext"]

        result = check_transformation_exists(file_path)

        if result:
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    if ext == "ipynb":
                        nb_result = nbformat.read(
                            file, as_version=4, capture_validation_error=None
                        )
                        return self.finish({"status": "finished", "file": nb_result})
                    else:
                        return self.finish({"status": "finished", "file": file.read()})
                except Exception as e:
                    traceback.print_exc()
                    self.finish({"status": "error", "error": str(e)})
        else:
            self.finish({"status": "pending"})
