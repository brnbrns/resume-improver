import unittest
import os
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import ModelConfig, ModelManager


class TestModelConfig(unittest.TestCase):
    """Test cases for ModelConfig dataclass."""
    
    def test_model_config_creation_success(self):
        """Test successful ModelConfig creation with all required fields."""
        config = ModelConfig(
            api_key="test-key",
            endpoint="https://test.openai.azure.com/",
            api_version="2025-01-01",
            deployment_name="gpt-4o"
        )
        
        self.assertEqual(config.api_key, "test-key")
        self.assertEqual(config.endpoint, "https://test.openai.azure.com/")
        self.assertEqual(config.api_version, "2025-01-01")
        self.assertEqual(config.deployment_name, "gpt-4o")
    
    def test_model_config_defaults(self):
        """Test ModelConfig with default values."""
        config = ModelConfig(
            api_key="test-key",
            endpoint="https://test.openai.azure.com/"
        )
        
        self.assertEqual(config.api_version, "2025-01-01")
        self.assertEqual(config.deployment_name, "gpt-4o")
    
    def test_model_config_missing_api_key(self):
        """Test ModelConfig validation with missing API key."""
        with self.assertRaises(ValueError) as context:
            ModelConfig(
                api_key="",
                endpoint="https://test.openai.azure.com/"
            )
        self.assertIn("AZURE_OPENAI_API_KEY is required", str(context.exception))
    
    def test_model_config_missing_endpoint(self):
        """Test ModelConfig validation with missing endpoint."""
        with self.assertRaises(ValueError) as context:
            ModelConfig(
                api_key="test-key",
                endpoint=""
            )
        self.assertIn("AZURE_OPENAI_ENDPOINT is required", str(context.exception))


class TestModelManager(unittest.TestCase):
    """Test cases for ModelManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.original_env = dict(os.environ)
        self.test_config = ModelConfig(
            api_key="test-key",
            endpoint="https://test.openai.azure.com/",
            api_version="2025-01-01",
            deployment_name="gpt-4o"
        )
        
    def tearDown(self):
        """Clean up test fixtures."""
        os.environ.clear()
        os.environ.update(self.original_env)
    
    def test_model_manager_with_config(self):
        """Test ModelManager initialization with provided config."""
        manager = ModelManager(config=self.test_config, load_env=False)
        
        self.assertEqual(manager.config, self.test_config)
        self.assertIsNone(manager._client)
    
    def test_model_manager_from_environment(self):
        """Test ModelManager initialization from environment variables."""
        os.environ['AZURE_OPENAI_API_KEY'] = 'env-key'
        os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://env.openai.azure.com/'
        os.environ['AZURE_OPENAI_API_VERSION'] = '2024-12-01'
        os.environ['AZURE_OPENAI_DEPLOYMENT_NAME'] = 'gpt-4-turbo'
        
        manager = ModelManager(load_env=False)
        
        self.assertEqual(manager.config.api_key, 'env-key')
        self.assertEqual(manager.config.endpoint, 'https://env.openai.azure.com/')
        self.assertEqual(manager.config.api_version, '2024-12-01')
        self.assertEqual(manager.config.deployment_name, 'gpt-4-turbo')
    
    def test_model_manager_missing_env_vars(self):
        """Test ModelManager with missing environment variables."""
        # Clear relevant environment variables
        for key in ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT', 
                   'AZURE_OPENAI_API_VERSION', 'AZURE_OPENAI_DEPLOYMENT_NAME']:
            os.environ.pop(key, None)
        
        with self.assertRaises(ValueError):
            ModelManager(load_env=False)    
    @patch('model.AzureOpenAIChatCompletionClient')
    def test_client_property_creation(self, mock_client_class):
        """Test client property creates and caches client instance."""
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance
        
        manager = ModelManager(config=self.test_config, load_env=False)
        
        # First access should create client
        client1 = manager.client
        self.assertEqual(client1, mock_client_instance)
        
        # Second access should return cached client
        client2 = manager.client
        self.assertEqual(client2, mock_client_instance)
        
        # Verify client was only created once
        mock_client_class.assert_called_once_with(
            azure_deployment=self.test_config.deployment_name,
            model=self.test_config.deployment_name,
            api_key=self.test_config.api_key,
            azure_endpoint=self.test_config.endpoint,
            api_version=self.test_config.api_version,
        )
    
    def test_config_property_readonly(self):
        """Test that config property is read-only."""
        manager = ModelManager(config=self.test_config, load_env=False)
        
        # Should not be able to set config after initialization
        with self.assertRaises(AttributeError):
            manager.config = ModelConfig(
                api_key="new-key",
                endpoint="https://new.openai.azure.com/"
            )    
    def test_update_config(self):
        """Test updating configuration."""
        manager = ModelManager(config=self.test_config, load_env=False)
        
        # Update some configuration values
        manager.update_config(
            api_key="new-key",
            deployment_name="gpt-4-turbo"
        )
        
        # Verify config was updated
        self.assertEqual(manager.config.api_key, "new-key")
        self.assertEqual(manager.config.deployment_name, "gpt-4-turbo")
        # Other values should remain the same
        self.assertEqual(manager.config.endpoint, self.test_config.endpoint)
        self.assertEqual(manager.config.api_version, self.test_config.api_version)
        
        # Verify client was reset (would be recreated on next access)
        self.assertIsNone(manager._client)
    
    @patch('model.load_dotenv')
    def test_load_env_parameter(self, mock_load_dotenv):
        """Test that load_env parameter controls dotenv loading."""
        os.environ['AZURE_OPENAI_API_KEY'] = 'test-key'
        os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://test.openai.azure.com/'
        
        # Test with load_env=True (default)
        ModelManager(load_env=True)
        mock_load_dotenv.assert_called_once()
        
        # Test with load_env=False
        mock_load_dotenv.reset_mock()
        ModelManager(load_env=False)
        mock_load_dotenv.assert_not_called()


if __name__ == '__main__':
    unittest.main()
