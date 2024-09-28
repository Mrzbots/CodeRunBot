import requests

class RunRequest:
    def __init__(self, language: str, code: str):
        self.language = language
        self.code = code
         
result_success = "success"
result_error = "error"
result_unknown = "unknown"

def execute_code(request: RunRequest):
    json_body = {
        "language": request.language,
        "version": "*",
        "code": request.code      
    }    
    response = requests.post("https://horridapi2-0.onrender.com/execute", json=json_body)               
    data = response.json()                     
    return data
