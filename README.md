# Summary

Backend for demo Issue Tracker application utilizing SQLite, SQLAlchemy ORM, and FastAPI framework

## Running Server
To run the server on your local machine, you will need to ensure that `poetry` and `python3.10` 
are already installed. Refer to official documentation if 
this is not the case.

- Create a virtual environment with poetry by running `poetry env use python3.10`
- Install dependencies with `poetry install`
- Start the server by running `poetry run python3 -m app.console`
- Test the endpoints by going to the /docs endpoint on the localhost

## Tasks

- [X] Support Issue PUT
- [X] Support Issue DELETE
- [ ] Support IssueDetail GET
- [ ] Integrate with Frontend and replace restdb.io

## Concerns

- Consider whether the models, schema, database packages should be simplified into a single file
- Consider a better way to initialize the data besides putting it into the issue_service api file
