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
