import os
import anthropic
from typing import Optional

class CommitMessageSuggester:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def suggest_commit_message(self, code: str) -> str:
        """
        Suggest a commit message based on the provided code.

        Args:
            code (str): The code changes for which to generate a commit message.

        Returns:
            str: A suggested commit message.
        """
        prompt = f"""
        As an AI assistant, your task is to generate a concise and informative commit message based on the following code changes:

        ```
        {code}
        ```

        Please follow these guidelines:
        1. Start with a short (50 characters or less) summary of the changes.
        2. If necessary, add a more detailed explanation after a blank line.
        3. Use the imperative mood in the subject line (e.g., "Add feature" not "Added feature").
        4. Capitalize the subject line.
        5. Do not end the subject line with a period.
        6. Wrap the body at 72 characters.
        7. Use the body to explain what and why, not how.

        Generate the commit message:
        """

        response = self.client.completions.create(
            model="claude-2",
            prompt=prompt,
            max_tokens_to_sample=300,
            temperature=0.7,
        )

        return response.completion.strip()

    def suggest_from_file(self, file_path: str) -> Optional[str]:
        """
        Suggest a commit message based on the contents of a file.

        Args:
            file_path (str): Path to the file containing code changes.

        Returns:
            Optional[str]: A suggested commit message, or None if the file couldn't be read.
        """
        try:
            with open(file_path, 'r') as file:
                code = file.read()
            return self.suggest_commit_message(code)
        except IOError as e:
            print(f"Error reading file: {e}")
            return None

if __name__ == "__main__":
    suggester = CommitMessageSuggester()
    
    # Example usage with a string
    code_changes = """
    def add_numbers(a, b):
        return a + b

    def multiply_numbers(a, b):
        return a * b
    """
    suggested_message = suggester.suggest_commit_message(code_changes)
    print("Suggested commit message:")
    print(suggested_message)

    # Example usage with a file
    file_path = "path/to/your/changed_file.py"
    suggested_message_from_file = suggester.suggest_from_file(file_path)
    if suggested_message_from_file:
        print("\nSuggested commit message from file:")
        print(suggested_message_from_file)
