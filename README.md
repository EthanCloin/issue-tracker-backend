# Summary

Backend for demo Issue Tracker application utilizing SQLite, SQLAlchemy ORM, and FastAPI framework

You can reference the Docker images available here: https://hub.docker.com/repository/docker/ethancloin/issue-tracker

Currently, version 1.0.1 is hosted via digitalocean and available at http://24.199.84.215:8000/docs.


## Running Server
To run the server on your local machine, you will need to ensure that `poetry` and `python3.10` 
are already installed. Refer to official documentation if 
this is not the case.

- Create a virtual environment with poetry by running `poetry env use python3.10`
- Install dependencies with `poetry install`
- Start the server by running `poetry run python3 -m app.console`
- Test the endpoints by going to the /docs endpoint on the localhost

## Contributing
Fork this repo and make a pull request. Or reach out to me via Discord (Starved Spectre#8883) to discuss what you would like to do. 
