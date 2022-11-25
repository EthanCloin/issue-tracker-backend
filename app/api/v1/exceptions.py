class MissingIssueException(Exception):
    """raised when a provided issue_id is not found in the database"""

    def __init__(self, issue_id: int):
        self.issue_id = issue_id
