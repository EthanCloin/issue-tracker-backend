"""This must be run as a module not a script to find the dependencies. 
AKA run with python3 -m app.console"""

import uvicorn

if __name__ == "__main__":
    print("RUNNING SERVER")
    uvicorn.run("app.api.v1.issue_service:app", host="0.0.0.0", port=8000)
