import requests
import os

def deploy_to_mcp_server(api_url, api_key, payload):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        print('Deployment successful!')
    else:
        print(f'Failed to deploy: {response.status_code} - {response.text}')
    return response

if __name__ == '__main__':
    api_url = os.getenv('MCP_API_URL')
    api_key = os.getenv('MCP_API_KEY')
    
    payload = {
        'service_name': 'example_service',
        'version': '1.0.0',
        'config': {
            'param1': 'value1',
            'param2': 'value2'
        }
    }
    
    deploy_to_mcp_server(api_url, api_key, payload) 