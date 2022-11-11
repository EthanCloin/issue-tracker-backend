"""pydantic 'schema' which represent expected request/response types for api endpoints. 
not to be confused sqlalchemy 'models' representing expected types for the database

Issue represents an entry provided by the user which contains at least a title,
description, assignee, and status. This issues will need to be filtered, sorted,
and updated. much of that is currently done on the frontend."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class IssueStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class IssueBase(BaseModel):
    title: str
    description: str
    assignee: str
    status: IssueStatus = IssueStatus.OPEN


class IssueCreate(IssueBase):
    """provided on client request"""

    pass


class Issue(IssueBase):
    """returned from db standard get"""

    id: int

    class Config:
        orm_mode = True


class IssueDetail(Issue):
    """returned from db details get"""

    created_on: datetime
    updated_on: datetime
