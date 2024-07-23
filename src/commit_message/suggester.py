import os
import anthropic
from dotenv import load_dotenv
from typing import Optional, List, Tuple
from .templates import COMMIT_TYPES, COMMIT_TEMPLATE, PROMPT_TEMPLATE

class CommitMessageSuggester:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env file")
        self.client = anthropic.Anthropic(api_key=api_key)

    def get_git_diff(self) -> str:
        try:
            import subprocess
            return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')
        except subprocess.CalledProcessError:
            print("Error: Unable to get git diff. Make sure you're in a git repository and have staged changes.")
            return ""

    def suggest_commit_message(self, diff: str) -> str:
        if not diff.strip():
            return "No changes detected."

        prompt = PROMPT_TEMPLATE.format(
            diff=diff,
            commit_types=", ".join(COMMIT_TYPES)
        )

        message = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            temperature=0.7,
            messages=[
                {
                "role": "user",
                "content": prompt
                }
            ]
        )

        return message.content[0].text

    def parse_commit_message(self, message: str) -> Tuple[str, str, str, str]:
        """
        Parse the generated commit message into its components.

        Args:
            message (str): The full commit message.

        Returns:
            Tuple[str, str, str, str]: type, subject, body, footer
        """
        lines = message.split('\n')
        header = lines[0]
        body = '\n'.join(lines[1:]).strip()

        # Parse header
        type, subject = header.split(':', 1)

        # Split body and footer
        if '\n\n' in body:
            body, footer = body.rsplit('\n\n', 1)
        else:
            footer = ''

        return type.strip(), subject.strip(), body.strip(), footer.strip()

    def format_commit_message(self, type: str, subject: str, body: str, footer: str) -> str:
        """
        Format the commit message components into the final message.

        Args:
            type (str): Commit type.
            subject (str): Commit subject.
            body (str): Commit body.
            footer (str): Commit footer.

        Returns:
            str: Formatted commit message.
        """
        return COMMIT_TEMPLATE.format(
            type=type,
            subject=subject,
            body=body,
            footer=footer
        )

    def summarize_commit_message(self, message: str) -> str:
        """
        Summarize the commit message for multiple file changes.

        Args:
            message (str): The full commit message.

        Returns:
            str: A summarized commit message.
        """
        lines = message.split('\n')
        main_message = lines[0]
        
        # Extract file names from the message
        file_changes = [line.strip() for line in lines if line.strip().startswith('-') and ':' in line]
        
        # Summarize file changes
        if len(file_changes) > 1:
            files_summary = f"Update {len(file_changes)} files"
        elif len(file_changes) == 1:
            files_summary = file_changes[0].split(':')[0].strip('- ')
        else:
            files_summary = "Make changes"

        # Combine main message with files summary
        summary = f"{main_message} && {files_summary}"
        
        # Add up to 3 bullet points of additional info
        additional_info = [line.strip('- ') for line in lines[1:] if line.strip().startswith('-') and ':' not in line][:3]
        if additional_info:
            summary += "\n\n" + "\n".join(f"- {info}" for info in additional_info)

        return summary

    def suggest_and_format(self, diff: str) -> str:
        if not diff:
            return "No changes detected."

        suggested_message = self.suggest_commit_message(diff)
        summarized_message = self.summarize_commit_message(suggested_message)
        
        # Parse the summarized message
        type, subject, body, footer = self.parse_commit_message(summarized_message)
        
        # Format the final message
        return self.format_commit_message(type, subject, body, footer)

if __name__ == "__main__":
    # Test with real git repository
    suggester = CommitMessageSuggester()
    formatted_message = suggester.suggest_and_format(suggester.get_git_diff())
    print("Suggested commit message (real git):")
    print(formatted_message)