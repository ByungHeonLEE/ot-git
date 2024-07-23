class Indexer:
    def __init__(self):
        self.commit_index = {}

    def index_commit(self, commit_hash, commit_message):
        # Simple indexing by storing commit message with hash as key
        self.commit_index[commit_hash] = commit_message

    def search_commits(self, keyword):
        # Simple search function
        return [
            (commit_hash, message)
            for commit_hash, message in self.commit_index.items()
            if keyword.lower() in message.lower()
        ]
