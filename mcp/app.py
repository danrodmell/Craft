from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'service': 'mcp-python',
        'version': os.getenv('MCP_VERSION', '0.1.0')
    })

@app.route('/mcp/context', methods=['POST'])
def process_context():
    data = request.get_json()
    # TODO: Implement MCP context processing
    return jsonify({
        'status': 'received',
        'data': data
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 