from pymongo import MongoClient
import requests
import logging

logging.basicConfig(level=logging.INFO)

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

def run_code(request: RunRequest) -> RunResponse:
    json_body = {
        "language": request.language,
        "version": "*",
        "files": request.code,
        "stdin": request.stdin
    }
    try:
        response = requests.post("https://emkc.org/api/v2/piston/execute", json=json_body)
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
    return RunResponse(result_success, data["run"]["output"])

client = MongoClient("mongodb://localhost:27017/")
db = client["piston"]
stats_collection = db["stats"]
