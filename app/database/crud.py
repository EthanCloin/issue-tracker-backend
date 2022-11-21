from sqlalchemy.orm import Session

from app.schema.issue import IssueCreate
from app.models.issue import Issue as IssueDB


def db_create_issue(issue_data: IssueCreate, db: Session) -> IssueDB:
    db_issue = IssueDB(**issue_data.dict())
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue
