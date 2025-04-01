import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from app import app
from mcp import mcp, process_context, health_check

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
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
    
    response = client.post('/mcp/context', json=test_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['result']['processed_query'] == 'test query'
    assert data['result']['processed_context'] == 'test context'
    assert 'response' in data['result']

def test_process_context_missing_data(client):
    test_data = {'query': 'test query'}  # Missing context
    response = client.post('/mcp/context', json=test_data)
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'message' in data

def test_process_context_server_error(client, monkeypatch):
    def mock_process_context(*args, **kwargs):
        raise Exception("Test error")
    
    monkeypatch.setattr('app.process_context', mock_process_context)
    
    test_data = {
        'query': 'test query',
        'context': 'test context'
    }
    
    response = client.post('/mcp/context', json=test_data)
    assert response.status_code == 500
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'message' in data 