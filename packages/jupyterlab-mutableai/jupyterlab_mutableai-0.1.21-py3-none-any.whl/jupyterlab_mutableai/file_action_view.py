import json
import os
import tornado
import shutil
import threading

from jupyter_server.base.handlers import APIHandler
from .utils import update_analytics


def clean_up(dirname: str):
    if os.path.exists(dirname) and os.path.isdir(dirname):
        shutil.rmtree(dirname)


def accept_changes(file_path, current_file_path):
    if not file_path:
        return False

    # If we find the transformed file then
    # read from that file and replace the base file
    # after this action we delete that folder.
    if os.path.exists(file_path):
        # Read in the file
        with open(file_path, "r") as file:
            filedata = file.read()
    if os.path.exists(current_file_path) and filedata:
        # Write the file out again
        with open(current_file_path, "w") as file:
            file.write(filedata)
        clean_up(file_path)
        return True
    return False


def decline_changes(file_path):
    """
    Delete the unique folder name if declined.
    """
    if not file_path:
        return False
    clean_up(file_path)
    return True


class FileActionRouterHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):
        self.finish(
            json.dumps(
                {"data": "This is /jlab-ext-example/TRANSFORM_NB endpoint!"})
        )

    @tornado.web.authenticated
    def post(self):
        input_data = self.get_json_body()

        # transformed file path
        file_path = input_data.get("file_path", "")
        
        # transformed file path
        current_file_path = input_data.get("current_file_path", "")

        # File action type

        action = input_data.get("action", "")

        url = input_data.get("url", "")

        api_key = input_data.get("apiKey", "")
        status = False

        if action == "accept":
            status = accept_changes(file_path, current_file_path)
            
            x = threading.Thread(target=update_analytics, args=(url, api_key, "accepted"))
            x.start()
            # update_analytics(url, api_key, "accepted")
        elif action == "decline":
            status = decline_changes(file_path)

            x = threading.Thread(target=update_analytics, args=(url, api_key, "declined"))
            x.start()
            # update_analytics(url, api_key, "declined")

        if status:
            self.finish({"status": "completed"})
        else:
            self.finish({"status": "failed"})
