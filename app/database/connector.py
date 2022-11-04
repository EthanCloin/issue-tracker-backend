from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pathlib import Path
from app.schema.issue import Issue, IssueCreate, IssueStatus

db_file = Path("app/temp.db")
DATABASE_URL = f"sqlite:///{db_file}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


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
            db_issue = Issue.from_orm(issue)
            s.add(db_issue)
            s.commit()
            s.refresh()

def init_db():
    print("INITING THE DB")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # init_issue_records()
    