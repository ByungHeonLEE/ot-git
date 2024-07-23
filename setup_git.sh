#!/bin/bash

# Clone the existing repository
git clone https://github.com/your-username/your-repo.git /git_repo

# Change to the repository directory
cd /git_repo

# Configure Git (you might want to make these configurable)
git config user.email "you@example.com"
git config user.name "Your Name"

# Start the Flask application
cd /app
flask run --host=0.0.0.0