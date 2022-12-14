"""this service provides endpoints to access issues in the database. """
from typing import Optional, Sequence

from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_db
from app.api.v1.exceptions import MissingIssueException
from app.database import crud, setup
from app.schema.issue import Issue, IssueCreate

# TODO: move app instance and CORS handling into upper-level main.py file
#   replace this with an APIRouter and add it to higher-layer app
# api setup
app = FastAPI()

# needs to be the frontend server url
origins = ["http://localhost:3000", "localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(MissingIssueException)
async def missing_issue_handler(req: Request, exc: MissingIssueException):
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Uh Oh...it looks like an issue with "
            f"id={exc.issue_id} doesn't exist!"
        },
    )


@app.on_event("startup")
def on_startup():
    setup.init_db_for(setup.DBEnv.STAGING)
    setup.init_issue_records()


@app.post("/issues/", response_model=Issue)
async def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    """add issue to database"""
    db_issue = crud.db_create_issue(issue, db)
    return Issue.from_orm(db_issue)


@app.get("/issues/", response_model=Sequence[Issue])
async def get_all_issues(
    offset: int = 0,
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
) -> Sequence[Issue]:
    """returns all issues, maximum 100 per request. use offset to get
    additional if necessary"""

    # TODO: add fxn to convert Issue Model to Schema for type safety
    db_issues = crud.db_get_all_issues(offset=offset, limit=limit, db=db)
    return [Issue.from_orm(issue) for issue in db_issues]


@app.get("/issues/{id}/", response_model=Issue)
async def get_issue(id: int, db: Session = Depends(get_db)) -> Issue | None:
    """returns the issue matching provided id or null"""
    db_issue = crud.db_get_issue(id=id, db=db)
    if db_issue:
        return Issue.from_orm(db_issue)
    else:
        raise MissingIssueException(id)


@app.delete("/issues/{id}/", response_model=Issue)
async def delete_issue(id: int, db: Session = Depends(get_db)):
    """removes issue with provided id from database"""
    db_issue = crud.db_delete_issue(id=id, db=db)
    if db_issue:
        return db_issue
    else:
        raise MissingIssueException(id)


@app.put("/issues/{id}/", response_model=Optional[Issue])
async def update_issue(
    id: int, updated_values: IssueCreate, db: Session = Depends(get_db)
):
    """updates the issue with the given id with the provided new values.
    must provide all values typically required to create a new issue."""
    db_issue = crud.db_update_issue(id=id, updated_values=updated_values, db=db)
    if db_issue:
        return db_issue
    raise MissingIssueException(id)
