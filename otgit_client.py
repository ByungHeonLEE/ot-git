import subprocess
import requests
import sys

def get_git_diff():
    try:
        return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')
    except subprocess.CalledProcessError:
        print("Error: Unable to get git diff. Make sure you're in a git repository and have staged changes.")
        return ""

def suggest_commit_message(diff):
    try:
        response = requests.post('http://192.168.215.2:5000/suggest', json={'diff': diff}, timeout=10)
        response.raise_for_status()
        if response.text:
            return response.json()['suggested_message']
        else:
            print("Error: Empty response from server")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def process_commit_message(message):
    lines = message.split('\n')
    type_and_subject = lines[0]
    
    # Extract additional info (up to 3 bullet points)
    additional_info = [line.strip('- ') for line in lines[1:] if line.strip().startswith('-')][:3]
    
    # Combine type_and_subject with additional info
    if additional_info:
        return f"{type_and_subject}\n\n" + "\n".join(f"- {info}" for info in additional_info)
    return type_and_subject

def commit_changes(message):
    try:
        subprocess.run(['git', 'commit', '-m', message], check=True)
        print("Changes committed successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to commit changes.")

if __name__ == "__main__":
    diff = get_git_diff()
    if diff:
        suggested_message = suggest_commit_message(diff)
        if suggested_message:
            processed_message = process_commit_message(suggested_message)
            print(f"Suggested commit message:\n\n{processed_message}\n")
            if len(sys.argv) > 1 and sys.argv[1] == '--commit':
                commit_changes(processed_message)
            else:
                print("To commit with this message, run the script with --commit flag")
    else:
        print("No changes to commit.")