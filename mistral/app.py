from flask import Flask, request, jsonify
import subprocess
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

def run_ollama(conversation_history, model="mistral"):
    prompt = "\n".join(conversation_history)
    command = ["ollama", "run", model, prompt]
    app.logger.debug(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=30)
        app.logger.debug(f"Ollama stdout: {result.stdout}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Error running Ollama: {e}")
        app.logger.error(f"Stderr: {e.stderr}")
        return f"Error: {e}"
    except subprocess.TimeoutExpired:
        app.logger.error("Ollama process timed out")
        return "Error: Process timed out"

@app.route('/generate', methods=['POST'])
def generate_text():
    app.logger.debug(f"Received request: {request.json}")
    try:
        data = request.json
        if not data or 'conversation_history' not in data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        conversation_history = data['conversation_history']
        model = data.get('model', 'mistral')

        response = run_ollama(conversation_history, model)
        app.logger.debug(f"Generated response: {response}")
        
        return jsonify({'response': response})
    except Exception as e:
        app.logger.exception("An error occurred")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
