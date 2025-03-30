import requests_mock
import unittest
import os
from deploy_to_mcp import deploy_to_mcp_server

class TestDeployment(unittest.TestCase):
    def setUp(self):
        """Set up test environment variables."""
        self.api_url = os.getenv('MCP_API_URL', 'http://test-api.example.com')
        self.api_key = os.getenv('MCP_API_KEY', 'test-key')
        self.test_payload = {
            'service_name': 'test_service',
            'version': '1.0.0',
            'config': {
                'param1': 'test_value1',
                'param2': 'test_value2'
            }
        }

    def test_deploy_to_mcp_server(self):
        """Test the deployment function with test data."""
        with requests_mock.Mocker() as m:
            m.post(self.api_url, json={'status': 'success'})

            try:
                response = deploy_to_mcp_server(self.api_url, self.api_key, self.test_payload)
                self.assertEqual(response.json(), {'status': 'success'})
            except Exception as e:
                self.fail(f"Deployment failed with error: {str(e)}")

    def test_payload_structure(self):
        """Test that the payload has the correct structure."""
        required_fields = ['service_name', 'version', 'config']
        for field in required_fields:
            self.assertIn(field, self.test_payload)
        
        # Test config structure
        self.assertIsInstance(self.test_payload['config'], dict)
        self.assertIn('param1', self.test_payload['config'])
        self.assertIn('param2', self.test_payload['config'])

if __name__ == '__main__':
    unittest.main() 