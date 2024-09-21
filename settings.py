import requests
import logging
logging.basicConfig(level=logging.INFO)

class RunRequest:
    def __init__(self, language: str, code: str):
        self.language = language
        self.code = code
         
result_success = "success"
result_error = "error"
result_unknown = "unknown"

def run_code(request: RunRequest) -> RunResponse:
    json_body = {
        "language": request.language,
        "version": "*",
        "files": request.code,        
    }
    try:
        response = requests.post("https://horrid-api-yihb.onrender.com/execute", json=json_body)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(e)
        return RunResponse(result_unknown, "", "")

    if response.status_code != 200:
        error_message = response.json().get("message", "")
        if not error_message:
            logging.error(response.text)
            return RunResponse(result_unknown, "", "")
        return RunResponse(result_error, error_message, "")

    data = response.json()
    lol = data['run']['output']
    if lol.strip() != '':  
        return RunResponse(lol)
    else:
        return RunResponse(result_success)

