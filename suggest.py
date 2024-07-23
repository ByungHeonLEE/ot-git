import re

class Suggester:
    @staticmethod
    def suggest_commit_message(code_diff):
        # This is a very basic implementation
        # In a real-world scenario, this would be much more sophisticated
        
        added_lines = [line for line in code_diff.split('\n') if line.startswith('+')]
        
        if not added_lines:
            return "Update code"
        
        # Try to identify the main action
        if any('def ' in line for line in added_lines):
            return "Add new function"
        elif any('class ' in line for line in added_lines):
            return "Add new class"
        elif any('import ' in line for line in added_lines):
            return "Add new import"
        
        # Default message
        return "Update code"
