import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.commit_message.suggester import CommitMessageSuggester
import traceback
import logging

app = Flask(__name__)
CORS(app)
suggester = CommitMessageSuggester()

logging.basicConfig(level=logging.DEBUG)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/suggest', methods=['POST'])
def suggest():
    app.logger.debug(f"Received request: {request.json}")
    try:
        diff = request.json.get('diff', '')
        if not diff:
            app.logger.warning("No diff provided")
            return jsonify({"error": "No diff provided"}), 400
        
        app.logger.debug("Calling suggester.suggest_and_format")
        suggested_message = suggester.suggest_and_format(diff)
        app.logger.debug(f"Suggested message: {suggested_message}")
        return jsonify({"suggested_message": suggested_message})
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print(f"Current working directory: {os.getcwd()}")
    print(f"Contents of current directory: {os.listdir('.')}")
    app.run(debug=True, host='0.0.0.0', port=5000)