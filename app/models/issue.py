"""sqlalchemy models to represent tables/columns in relational db"""

from sqlalchemy import Column, Integer, String, Text, Enum
from app.database.connector import Base
from app.schema.issue import IssueStatus


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), index=True)
    description = Column(Text)
    assignee = Column(String(64), index=True)
    status = Column(Enum(IssueStatus))