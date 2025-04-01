from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'ok',
        'service': 'mcp-service',
        'version': '1.0.0'
    })

@app.route('/mcp/context', methods=['POST'])
def handle_context():
    # This will be expanded with actual MCP SDK integration
    data = request.get_json()
    return jsonify({
        'status': 'received',
        'data': data
    })

if __name__ == '__main__':
    port = int(os.environ.get('MCP_PORT', 5000))
    app.run(host='0.0.0.0', port=port) 