from flask import Flask, request, jsonify
from flask_cors import CORS  # Importing CORS
from agent2 import Agent2  # Importing Agent2
from agent3 import Agent3  # Importing Agent3
from agent5 import Agent5  # Importing Agent5
from agent6 import Agent6  # Importing Agent6
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Enabling CORS for all routes

# Directory to save uploaded files and prompts
UPLOAD_FOLDER = './uploaded_files'
PROMPT_FOLDER = './prompts'  # New folder for storing prompts

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROMPT_FOLDER):
    os.makedirs(PROMPT_FOLDER)

# Global variables to store configuration and the latest file path
config = {
    "api_key": None,
    "user_input": None,
    "input_prompt": None  # Added new key to store the entered prompt
}
latest_file_path = None

# Route to set the API key and user input
@app.route('/set_config', methods=['POST'])
def set_config():
    """
    Set the API key and user input in the global configuration.
    """
    data = request.json
    config["api_key"] = data.get('api_key')
    config["user_input"] = data.get('user_input')

    if not config["api_key"] or not config["user_input"]:
        return jsonify({"error": "API key and user input are required"}), 400

    return jsonify({"message": "Configuration updated successfully", "config": config})

# Route to upload a file
@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload a file and store its path.
    """
    global latest_file_path
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    latest_file_path = file_path  # Update the latest file path
    return jsonify({'message': 'File uploaded successfully', 'file_path': latest_file_path}), 200

# Route to get the latest uploaded file
@app.route('/get_latest_file', methods=['GET'])
def get_latest_file():
    """
    Retrieve the path of the latest uploaded file.
    """
    if latest_file_path:
        return jsonify({'file_path': latest_file_path}), 200
    return jsonify({'error': 'No file uploaded yet'}), 404


# New route to set the prompt and store it in a file
@app.route('/set_prompt', methods=['POST'])
def set_prompt():
    """
    Store the entered prompt in the global configuration and write it to a file.
    """
    data = request.json
    config["input_prompt"] = data.get('input_prompt')

    if not config["input_prompt"]:
        return jsonify({"error": "Prompt input is required"}), 400

    # Define the file path for storing the prompt
    prompt_file_path = os.path.join(PROMPT_FOLDER, "latest_prompt.txt")
    # Store the prompt in the file
    try:
        with open(prompt_file_path, "w") as f:
            f.write(config["input_prompt"])

        agent = Agent2(latest_file_path)
        agent.agent2()
        agent = Agent3(latest_file_path)
        agent.agent3()
        agent = Agent5(latest_file_path)
        agent.agent5()
        agent = Agent6(latest_file_path)
        agent.agent6()

        

        

        return jsonify({"message": "Prompt stored successfully", "input_prompt": config["input_prompt"]})
    
    except Exception as e:
        return jsonify({"error": f"Error storing prompt: {str(e)}"}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(port=5000, debug=True)