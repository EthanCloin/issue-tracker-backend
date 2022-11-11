"""this service provides endpoints to access issues in the database. """
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
    """create default issue rows as test data"""
    issues = [
        IssueCreate(title="1 Problem", description="really does it matter", assignee="mgmt"),
        IssueCreate(title="2 Problem", description="really does it matter", assignee="mgmt", status=IssueStatus.CLOSED),
        IssueCreate(title="3 Problem", description="really does it matter", assignee="facility"),
        IssueCreate(title="4 Problem", description="really does it matter", assignee="financial"),
        IssueCreate(title="5 Problem", description="really does it matter", assignee="mgmt", status=IssueStatus.CLOSED)
    ]

    with Session(engine) as s:
        for issue in issues:
            db_issue = IssueDB(**issue.dict())
            s.add(db_issue)
            s.commit()
            s.refresh(db_issue)

@app.on_event("startup")
def on_startup():
    init_db()
    init_issue_records()


@app.post("/issues/", response_model=Issue)
async def create_issue(issue: IssueCreate, db: LocalSession = Depends(get_db)):
    """add issue to database"""
    db_issue = IssueDB(**issue.dict())   
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


@app.get("/issues/", response_model=list[Issue])
async def get_all_issues(
    offset: int = 0, 
    limit: int = Query(default=20, lte=100), 
    db: LocalSession = Depends(get_db)
) -> list[Issue]:
    """returns all issues, maximum 100 per request. use offset to get additional if necessary"""
    
    result = db.query(IssueDB).offset(offset).limit(limit).all()

    return result

@app.get("/issues/{id}/", response_model=Issue)
async def get_issue(
    id: int, all_details: bool = False, db: LocalSession = Depends(get_db)
) -> Issue | None:
    """returns the issue matching provided id or null"""
    return db.query(IssueDB).filter(IssueDB.id == id).first()


@app.delete("/issues/{id}/", response_model=Issue)
async def delete_issue(id: int, db: LocalSession = Depends(get_db)):
    """removes issue with provided id from database"""
    target_issue = db.query(IssueDB).filter(IssueDB.id == id).first()
    db.delete(target_issue)
    db.commit()
    return target_issue


@app.put("/issues/{id}/", response_model=Issue)
async def update_issue(id: int, updated_values: IssueCreate, db: LocalSession = Depends(get_db)):
   """updates the issue with the given id with the provided new values. must provide all values
    typically required to create a new issue."""

    target_issue: IssueDB = db.query(IssueDB).filter(IssueDB.id == id).first()
    target_issue.update(**updated_values.dict())
    db.add(target_issue)
    db.commit()
    return target_issue