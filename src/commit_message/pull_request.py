from templates import Templates

class PullRequestSuggester:
    @staticmethod
    def suggest_pr_message(pr_diff, base_branch, head_branch):
        template = Templates.get_pull_request_template()
        
        # This is a basic implementation
        # In a real scenario, this would be more sophisticated
        
        description = f"Merge changes from {head_branch} into {base_branch}"
        
        changes = PullRequestSuggester._summarize_changes(pr_diff)
        
        filled_template = template.replace("[Provide a brief description of the changes in this PR]", description)
        filled_template = filled_template.replace("[List the main changes made in this PR]", changes)
        
        return filled_template

    @staticmethod
    def _summarize_changes(pr_diff):
        # This is a very simple implementation
        added_lines = len([line for line in pr_diff.split('\n') if line.startswith('+')])
        removed_lines = len([line for line in pr_diff.split('\n') if line.startswith('-')])
        
        return f"Added {added_lines} lines, removed {removed_lines} lines."
