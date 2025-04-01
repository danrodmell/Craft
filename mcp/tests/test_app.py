import pytest
import sys
from pathlib import Path
from unittest.mock import patch
sys.path.append(str(Path(__file__).parent.parent))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    with patch('app.mcp_client.health_check', return_value={'status': 'healthy'}):
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert data['service'] == 'mcp-python'
        assert 'version' in data
        assert data['mcp_status'] == {'status': 'healthy'}

def test_process_context_success(client):
    test_data = {
        'query': 'test query',
        'context': 'test context'
    }
    expected_result = {
        'processed_query': 'test query',
        'processed_context': 'test context',
        'response': 'test response'
    }
    
    with patch('app.mcp_client.process_context', return_value=expected_result):
        response = client.post('/mcp/context', json=test_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['result'] == expected_result

def test_process_context_missing_data(client):
    test_data = {'query': 'test query'}  # Missing context
    response = client.post('/mcp/context', json=test_data)
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'message' in data

def test_process_context_sdk_error(client):
    test_data = {
        'query': 'test query',
        'context': 'test context'
    }
    
    with patch('app.mcp_client.process_context', side_effect=Exception('SDK Error')):
        response = client.post('/mcp/context', json=test_data)
        assert response.status_code == 500
        data = response.get_json()
        assert data['status'] == 'error'
        assert 'message' in data 