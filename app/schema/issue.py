"""pydantic 'schema' which represent expected request/response types for api endpoints. 
not to be confused sqlalchemy 'models' representing expected types for the database"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum


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