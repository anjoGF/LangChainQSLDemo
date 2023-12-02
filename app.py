
from flask import Flask, request, jsonify
from langchain_service import LangChainService
import os

app = Flask(__name__)

# Initialize the LangChainService
service = LangChainService('Chinook.db', os.environ['OPENAI_API_KEY'])

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query = data.get('query')
    response = service.query_database(query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
