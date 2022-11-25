from fastapi.testclient import TestClient

from app.api.v1 import issue_service

# TODO: put test data into a single central location.
#  the crud file can pull from
#  there to get the initial rows as well.
client = TestClient(issue_service.app)


def test_get_all_returns_200():
    response = client.get("/issues/")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_get_one_returns_200():
    response = client.get("/issues/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "1 Problem",
        "description": "really does it matter",
        "assignee": "mgmt",
        "status": "open",
    }


# def test_create_issue_success_with_full_issue():
#     new_issue = issue_schema.IssueCreate(
#         title="My Test Title",
#         description="""
#     My Test Description is longer than My TestTitle and includes
#
#     Multiple
#     weird whitespace    characters""",
#         assignee="My Test Assignee",
#     )
#     body = new_issue.dict()
#     response = client.post("/issues/", json=body)
#     print("testing")
#     print(response)
