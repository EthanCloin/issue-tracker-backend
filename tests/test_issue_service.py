from fastapi.testclient import TestClient
from app.api.v1 import issue_service, dependencies
from app.schema import issue as issue_schema

client = TestClient(issue_service.app)

def test_create_issue_success_with_full_issue():
    new_issue = issue_schema.IssueCreate(
        title="My Test Title",
        description="""
    My Test Description is longer than My TestTitle and includes
    
    Multiple 
    weird whitespace    characters""",
        assignee="My Test Assignee",
    )
    body = new_issue.dict()
    response = client.post("/issues/", json=body)
    print("testing")
    print(response)
