from typing import Optional, Sequence

from sqlalchemy.orm import Session

from app.database.connector import DBEnv, init_db_for, get_engine_for
from app.models.issue import Issue as IssueDB
from app.schema.issue import IssueCreate, IssueStatus

# startup helpers


def init_issue_records():
    init_db_for(DBEnv.STAGING)
    """create default issue rows as test data"""
    issues = [
        IssueCreate(
            title="1 Problem", description="really does it matter", assignee="mgmt"
        ),
        IssueCreate(
            title="2 Problem",
            description="really does it matter",
            assignee="mgmt",
            status=IssueStatus.CLOSED,
        ),
        IssueCreate(
            title="3 Problem", description="really does it matter", assignee="facility"
        ),
        IssueCreate(
            title="4 Problem", description="really does it matter", assignee="financial"
        ),
        IssueCreate(
            title="5 Problem",
            description="really does it matter",
            assignee="mgmt",
            status=IssueStatus.CLOSED,
        ),
    ]

    with Session(get_engine_for(DBEnv.STAGING)) as s:
        for issue in issues:
            db_issue = IssueDB(**issue.dict())
            s.add(db_issue)
            s.commit()
            s.refresh(db_issue)


def db_create_issue(issue_data: IssueCreate, db: Session) -> IssueDB:
    db_issue = IssueDB(**issue_data.dict())
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def db_get_all_issues(
    limit: int,
    offset: int,
    db: Session,
) -> Sequence[IssueDB]:
    return db.query(IssueDB).offset(offset).limit(limit).all()


def db_get_issue(id: int, db: Session) -> Optional[IssueDB]:
    return db.query(IssueDB).filter(IssueDB.id == id).first()


def db_delete_issue(id: int, db: Session) -> Optional[IssueDB]:
    target_issue = db.query(IssueDB).filter(IssueDB.id == id).first()
    if target_issue:
        db.delete(target_issue)
        db.commit()
    return target_issue


def db_update_issue(
    id: int, updated_values: IssueCreate, db: Session
) -> Optional[IssueDB]:
    target_issue = db.query(IssueDB).filter(IssueDB.id == id).first()

    if target_issue:
        target_issue.update(**updated_values.dict())
        db.add(target_issue)
        db.commit()
    return target_issue
