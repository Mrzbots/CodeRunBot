import os
import json
import requests
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

auth_token = os.getenv("AUTH")
auth_header = {"Authorization": auth_token} if auth_token else {}

class RunRequest:
    def __init__(self, language: str, code: str, stdin: str):
        self.language = language
        self.code = code
        self.stdin = stdin

class RunResponse:
    def __init__(self, result: str, output: str, compiler_output: str):
        self.result = result
        self.output = output
        self.compiler_output = compiler_output

result_success = "success"
result_error = "error"
result_unknown = "unknown"

def get_languages() -> Tuple[List[str], str]:
    try:
        response = requests.get("https://emkc.org/api/v2/piston/runtimes", headers=auth_header)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(e)
        return [], str(e)

    languages_map = response.json()
    language_set = {obj["Language"] for obj in languages_map}
    languages = sorted(list(language_set))
    return languages, ""

def run_code(request: RunRequest) -> RunResponse:
    json_body = {
        "language": request.language,
        "version": "*",
        "files": request.code,
        "stdin": request.stdin
    }
    try:
        response = requests.post("https://emkc.org/api/v2/piston/execute", json=json_body, headers=auth_header)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(e)
        return RunResponse(result_unknown, "", "")

    if response.status_code != 200:
        error_message = response.json().get("Message", "")
        if not error_message:
            logging.error(response.text)
            return RunResponse(result_unknown, "", "")
        return RunResponse(result_error, error_message, "")

    data = response.json()
    return RunResponse(result_success, data["Run"]["Output"], data["Compile"]["Output"])

client = MongoClient("mongodb://localhost:27017/")
db = client["piston"]
stats_collection = db["stats"]
