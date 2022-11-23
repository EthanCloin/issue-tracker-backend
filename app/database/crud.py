from typing import Sequence

from sqlalchemy.orm import Session

from app.models.issue import Issue as IssueDB
from app.schema.issue import IssueCreate


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


def db_get_issue(id: int, db: Session) -> IssueDB:
    return db.query(IssueDB).filter(IssueDB.id == id).first()
