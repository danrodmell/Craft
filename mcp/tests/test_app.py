import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from app import app

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

def test_process_context(client):
    test_data = {'query': 'test query', 'context': 'test context'}
    response = client.post('/mcp/context', json=test_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'received'
    assert data['data'] == test_data 