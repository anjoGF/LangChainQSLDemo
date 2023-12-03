from flask import Flask, request, jsonify
from langchain_service import LangChainService
import os

app = Flask(__name__)

# Initialize the LangChainService
service = LangChainService('Chinook.db', os.environ['OPENAI_API_KEY'])

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.json
        query_text = data.get('query')
        if not query_text:
            return jsonify({'error': 'No query provided'}), 400

        response = service.query_database(query_text)
        return jsonify({'response': response})

    except Exception as e:
        # print(e)

        # Return a JSON response with the error message and a server error status code
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
