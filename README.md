# OLLAMA on Linux and Mac

## Overview

This repository contains instructions and code for running OLLAMA on Linux and Mac. It is divided into two main sections:

- [Llama2](llama2/README.md): Instructions and code for running Llama2 with OLLAMA on Linux.
- [Mistral](mistral/README.md): Instructions and code for running Mistral with OLLAMA on Linux.

## Running OLLAMA on Mac

To run OLLAMA on a Mac, follow these steps:

1. Execute: ```curl https://ollama.ai/install.sh | sh```
2. Pull a model, like Mistral or LLaMA 2
   ```ollama pull mistral```
   ```ollama pull llama2```

3. Run: ```ollama run llama2```
4. Try various prompts and observe the outputs.
5. Experiment with different things:
   ```ollama run llama2 "Summarize the benefits of AI in healthcare" \```
## Running simple API with Flask to expose LLaMA2 or Mistral
1. Ensure Python and Flask are installed:
   ```pip install flask```
2. Create a new Python file (e.g., ollama_api.py) and paste the code from [ollama-api.py](mac/ollama-api.py)
3. Run the flask application:
   ```python ollama_api.py```
4. Test the API using curl or a tool like Postman:
   ```curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "Explain quantum computing in simple terms", "model": "llama2"}'```

5. Extend the API:
   - Add error handling
   - Implement request validation
   - Add support for streaming responses
   - Create a simple web interface for interacting with the API





