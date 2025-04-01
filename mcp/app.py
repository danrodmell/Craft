from flask import Flask, request, jsonify
from dotenv import load_dotenv
from mcp import MCPClient, MCPConfig
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize MCP client
mcp_config = MCPConfig(
    api_key=os.getenv('MCP_API_KEY'),
    environment=os.getenv('MCP_ENVIRONMENT', 'development')
)
mcp_client = MCPClient(config=mcp_config)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'service': 'mcp-python',
        'version': os.getenv('MCP_VERSION', '0.1.0'),
        'mcp_status': mcp_client.health_check()
    })

@app.route('/mcp/context', methods=['POST'])
def process_context():
    try:
        data = request.get_json()
        query = data.get('query')
        context = data.get('context')
        
        if not query or not context:
            return jsonify({
                'status': 'error',
                'message': 'Both query and context are required'
            }), 400

        # Process context using MCP SDK
        result = mcp_client.process_context(
            query=query,
            context=context,
            options={
                'max_tokens': int(os.getenv('MCP_MAX_TOKENS', 1000)),
                'temperature': float(os.getenv('MCP_TEMPERATURE', 0.7))
            }
        )

        return jsonify({
            'status': 'success',
            'result': result
        })

    except Exception as e:
        app.logger.error(f"Error processing context: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 