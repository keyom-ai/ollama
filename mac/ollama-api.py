from flask import Flask, request, jsonify
import subprocess
import logging
from threading import Thread
from queue import Queue, Empty

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def run_ollama(prompt, model="llama2"):
    command = ["ollama", "run", model, prompt]
    app.logger.debug(f"Running command: {' '.join(command)}")
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        q = Queue()
        t = Thread(target=enqueue_output, args=(process.stdout, q))
        t.daemon = True
        t.start()

        output = []
        while True:
            try:
                line = q.get_nowait()
                output.append(line)
                app.logger.debug(f"Ollama output line: {line.strip()}")
            except Empty:
                if process.poll() is not None:
                    break

        stderr = process.stderr.read()
        if stderr:
            app.logger.error(f"Stderr: {stderr}")

        return ''.join(output).strip()
    except Exception as e:
        app.logger.error(f"Error running Ollama: {e}")
        return None

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.json
        app.logger.debug(f"Received data: {data}")

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        prompt = data.get('prompt', '')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        model = data.get('model', 'llama2')

        app.logger.debug(f"Calling Ollama with prompt: {prompt}")
        response = run_ollama(prompt, model)
        app.logger.debug(f"Ollama response: {response}")

        if response is None:
            return jsonify({'error': 'Failed to generate response'}), 500

        return jsonify({'response': response})
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
