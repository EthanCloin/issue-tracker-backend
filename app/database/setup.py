from app.database.connector import DBEnv, get_sessionmaker_for
from app.models.issue import Issue as IssueDB
from app.schema.issue import IssueCreate, IssueStatus


def init_issue_records(env: DBEnv = DBEnv.STAGING):
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
    maker = get_sessionmaker_for(env)
    with maker() as s:
        for issue in issues:
            db_issue = IssueDB(**issue.dict())
            s.add(db_issue)
            s.commit()
            s.refresh(db_issue)
