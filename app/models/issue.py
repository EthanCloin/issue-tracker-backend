"""sqlalchemy models to represent tables/columns in relational db

see schema docstring for explanation of the Issue data"""

from sqlalchemy import Column, Enum, Integer, String, Text

from app.database.connector import Base
from app.schema.issue import IssueStatus


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), index=True)
    description = Column(Text)
    assignee = Column(String(64), index=True)
    status = Column(Enum(IssueStatus))

    def update(
        self,
        title: str,
        description: str,
        assignee: str,
        status: Enum[IssueStatus],
        id: int = None,
        **kwargs
    ):
        self.title = title
        self.description = description
        self.assignee = assignee
        self.status = status
