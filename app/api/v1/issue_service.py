# from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.dependencies import LocalSession, get_db
from app.database.connector import init_db, engine
from app.schema.issue import Issue, IssueCreate, IssueStatus
from app.models.issue import Issue as IssueDB
from sqlalchemy.orm import Session

# TODO: move app instance and CORS handling into upper-level main.py file
#   replace this with an APIRouter and add it to higher-layer app
# api setup
print("APP ASSIGNED")
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

def init_issue_records():
    """create default issue rows"""
    print('creating issues lmfao')
    issues = [
        IssueCreate(title="1 Problem", description="really does it matter", assignee="mgmt"),
        IssueCreate(title="2 Problem", description="really does it matter", assignee="mgmt", status=IssueStatus.CLOSED),
        IssueCreate(title="3 Problem", description="really does it matter", assignee="facility"),
        IssueCreate(title="4 Problem", description="really does it matter", assignee="financial"),
        IssueCreate(title="5 Problem", description="really does it matter", assignee="mgmt", status=IssueStatus.CLOSED)
    ]

    # mapped_issues = [Issue.from_orm(issue) for issue in issues]
    with Session(engine) as s:
        for issue in issues:
            db_issue = IssueDB(**issue.dict())
            s.add(db_issue)
            s.commit()
            s.refresh(db_issue)

@app.on_event("startup")
def on_startup():
    print("STARTING UP")
    init_db()
    init_issue_records()


# TODO: refactor all below paths to be more logical
@app.post("/issues/")
async def create_issue(issue: IssueCreate, db: LocalSession = Depends(get_db)):
    print("rec'd: " + str(issue))
    db_issue = IssueDB(**issue.dict())   
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


# currently having an issue getting this data. need to figure out proper way to use
# the dependency version of session to fetch data. at least the create works so use that
@app.get("/issues/")
async def get_all_issues(
    offset: int = 0, 
    limit: int = Query(default=20, lte=100), 
    db: LocalSession = Depends(get_db)
) -> list[Issue]:
    
    result = db.query(IssueDB).offset(offset).limit(limit).all()

    return result
