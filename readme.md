# OTGIT (OT Git)

OTGIT is a commit message suggester that uses AI to generate meaningful commit messages based on your Git diff.

## Flow Chart

flowchart TD
    A[Start] --> B[Set up OTGIT]
    B --> C[Stage Git Changes]
    C --> D[Run OTGIT Client]
    D --> E{Approve Suggestion?}
    E -->|Yes| F[Commit Changes]
    E -->|No| G[Edit Message]
    G --> F
    F --> H[End]

## Prerequisites

- Docker
- Git
- Anthropic API key

## Project Structure

```
otgit/
├── src/
│   └── commit_message/
│       ├── suggester.py
│       └── templates.py
├── server.py
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/otgit.git
   cd otgit
   ```

2. Create a `.env` file in the project root and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

## Building the Docker Image & Run the Container

In the project root directory, run:

```
docker build -t otgit-suggester .
docker run -d -p 5000:5000 --env-file .env --name otgit-service otgit-suggester
```

## Usage

1. Copy the otgit_client.py at your git repository
   ```
   cp /otgit/paths/otgit_client.py
   ```
2. Modify the otgit_client.py 14th line to your IP_address 
    ```
    response = requests.post('http://192.168.215.2:5000/suggest', json={'diff': diff}, timeout=10)
    ```

3. Stage your Git changes as usual:
    ```
    git add .
    ```

4. To get the suggested message, run the command: 
   ```
   python otgit_client.py
   ```

5. If you are satisfied with the suggestion, commit the changes:
```
python otgit_client.py --commit
```
