class Templates:
    @staticmethod
    def get_commit_template():
        return """
        [Type]: Brief description

        Detailed explanation

        [Related Issues]: #issue_number
        """

    @staticmethod
    def get_pull_request_template():
        return """
        ## Description
        [Provide a brief description of the changes in this PR]

        ## Related Issue
        [Link to the related issue, if applicable]

        ## Changes Made
        [List the main changes made in this PR]

        ## Testing
        [Describe how these changes were tested]

        ## Additional Notes
        [Any additional information or context]
        """
COMMIT_TYPES = [
    "feat",     # A new feature
    "fix",      # A bug fix
    "docs",     # Documentation only changes
    "style",    # Changes that do not affect the meaning of the code (white-space, formatting, etc)
    "refactor", # A code change that neither fixes a bug nor adds a feature
    "perf",     # A code change that improves performance
    "test",     # Adding missing tests or correcting existing tests
    "chore",    # Changes to the build process or auxiliary tools and libraries such as documentation generation
    "revert",   # Reverts a previous commit
]

COMMIT_TEMPLATE = "{type}): {subject}\n\n{body}\n\n{footer}"

PROMPT_TEMPLATE = """
Human: As an AI assistant, your task is to generate a concise and informative commit message based on the following code changes:

```
{diff}
```

Please follow these guidelines:
1. Use the following format: <type>): <subject>
2. <type> must be one of the following: {commit_types}
3. <subject> should be no greater than 50 characters, in the imperative, present tense
4. Add a more detailed explanation in the body, wrapped at 72 characters
5. Use the body to explain what and why, not how
6. If applicable, add a footer to reference issues or breaking changes

Generate the commit message:

Assistant: Here's a suggested commit message based on the provided guidelines and code changes:
"""
