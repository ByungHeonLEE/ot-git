import os
import anthropic
from typing import Optional, List, Tuple
from .templates import COMMIT_TYPES, COMMIT_TEMPLATE, PROMPT_TEMPLATE
from .mock_git_repo import MockGitRepo

class CommitMessageSuggester:
    def __init__(self, use_mock=False):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.use_mock = use_mock
        self.mock_repo = MockGitRepo() if use_mock else None

    def get_git_diff(self) -> str:
        """
        Get the git diff of the current changes.

        Returns:
            str: The git diff output.
        """
        if self.use_mock:
            return self.mock_repo.get_diff()
        else:
            try:
                import subprocess
                return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')
            except subprocess.CalledProcessError:
                print("Error: Unable to get git diff. Make sure you're in a git repository and have staged changes.")
                return ""

    def suggest_commit_message(self, diff: str) -> str:
        """
        Suggest a commit message based on the provided git diff.

        Args:
            diff (str): The git diff for which to generate a commit message.

        Returns:
            str: A suggested commit message.
        """
        if not diff.strip():
            return "No changes detected."

        prompt = PROMPT_TEMPLATE.format(
            diff=diff,
            commit_types=", ".join(COMMIT_TYPES)
        )

        response = self.client.completions.create(
            model="claude-2",
            prompt=prompt,
            max_tokens_to_sample=500,
            temperature=0.7,
        )

        return response.completion.strip()

    def parse_commit_message(self, message: str) -> Tuple[str, str, str, str, str]:
        """
        Parse the generated commit message into its components.

        Args:
            message (str): The full commit message.

        Returns:
            Tuple[str, str, str, str, str]: type, scope, subject, body, footer
        """
        lines = message.split('\n')
        header = lines[0]
        body = '\n'.join(lines[1:]).strip()

        # Parse header
        type_scope, subject = header.split(':', 1)
        if '(' in type_scope:
            type, scope = type_scope.split('(')
            scope = scope.rstrip(')')
        else:
            type, scope = type_scope, ''

        # Split body and footer
        if '\n\n' in body:
            body, footer = body.rsplit('\n\n', 1)
        else:
            footer = ''

        return type.strip(), scope.strip(), subject.strip(), body.strip(), footer.strip()

    def format_commit_message(self, type: str, scope: str, subject: str, body: str, footer: str) -> str:
        """
        Format the commit message components into the final message.

        Args:
            type (str): Commit type.
            scope (str): Commit scope.
            subject (str): Commit subject.
            body (str): Commit body.
            footer (str): Commit footer.

        Returns:
            str: Formatted commit message.
        """
        return COMMIT_TEMPLATE.format(
            type=type,
            scope=f"({scope})" if scope else "",
            subject=subject,
            body=body,
            footer=footer
        )

    def suggest_and_format(self) -> str:
        """
        Suggest a commit message based on the current git diff and format it.

        Returns:
            str: A formatted commit message suggestion.
        """
        diff = self.get_git_diff()
        if not diff:
            return "No changes detected."

        suggested_message = self.suggest_commit_message(diff)
        type, scope, subject, body, footer = self.parse_commit_message(suggested_message)
        return self.format_commit_message(type, scope, subject, body, footer)

if __name__ == "__main__":
    # Test with real git repository
    suggester = CommitMessageSuggester()
    formatted_message = suggester.suggest_and_format()
    print("Suggested commit message (real git):")
    print(formatted_message)

    # Test with mock git repository
    mock_suggester = CommitMessageSuggester(use_mock=True)
    mock_suggester.mock_repo.stage_changes("""
diff --git a/example.py b/example.py
index 1234567..abcdefg 100644
--- a/example.py
+++ b/example.py
@@ -1,5 +1,5 @@
 def hello_world():
-    print("Hello, World!")
+    print("Hello, GitHub!")
 
 if __name__ == "__main__":
     hello_world()
""")
    mock_formatted_message = mock_suggester.suggest_and_format()
    print("\nSuggested commit message (mock git):")
    print(mock_formatted_message)
