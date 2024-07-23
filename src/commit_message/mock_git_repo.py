class MockGitRepo:
    def __init__(self):
        self.staged_changes = ""

    def stage_changes(self, changes):
        self.staged_changes += changes

    def get_diff(self):
        return self.staged_changes

    def commit(self, message):
        print(f"Committing with message:\n{message}")
        self.staged_changes = ""
