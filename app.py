from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure the API key
genai.configure(api_key="AIzaSyAOA6ILk50M-A5jRXd5ncruS0clh4hcKxU")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Invalid input'}), 400
        
        prompt = data['prompt']
        model = genai.GenerativeModel("gemini-1.5-flash")
        custom = "you work for ekalavya engines.you must behave like an ai agent trained only for data analysis,business analysis and answer only questions based on 1.Data collection,2.Automation ,3.Sql optimization,4.Visualisation,5.training dataset,6.accuracy.data complexity and load,8.add on parameters"
        response = model.generate_content(custom+prompt)
        
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)