import json
import requests
import tornado
import os
import threading
from jupyter_server.base.handlers import APIHandler
from .utils import update_analytics

AUTOCOMPLETE_ROUTE = "AUTOCOMPLETE"


def call_autocomplete(data, api_key: str, domain: str) -> str:
    data_to_send = {**data, "max_length": 100}
    url = "https://" + domain + "/" + AUTOCOMPLETE_ROUTE
    rt_json = requests.post(
        url=url,
        json=data_to_send,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
        },
    ).json()

    if rt_json.get("message") == "Limit Exceeded":
        return "# Limit Exceeded"

    return rt_json.get("completion", "")


class AutoCompleteRouteHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):
        self.finish(
            json.dumps(
                {"data": "This is /jlab-ext-example/AUTOCOMPLETE endpoint!"})
        )

    @tornado.web.authenticated
    def post(self):
        # input_data is a dictionary with a key "name"
        input_data = self.get_json_body()
        data = input_data["data"]

        autocomplete_data = ""

        api_key, domain, flag = (
            input_data["apiKey"],
            input_data["domain"],
            input_data["flag"],
        )
        # If flag is set to false then we response with empty array.

        if flag:
            autocomplete_data = call_autocomplete(data, api_key, domain)
            x = threading.Thread(target=update_analytics, args=(domain, api_key, "autocomplete-success"))
            x.start()
        else:
            autocomplete_data = []
            x = threading.Thread(target=update_analytics, args=(domain, api_key, "autocomplete-failed"))
            x.start()

        self.finish(json.dumps(autocomplete_data))
