"""
Pytest configuration and fixtures for the resume improver tests.
"""

import pytest
import tempfile
from PIL import Image
import shutil

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def test_image():
    """Create a test image for testing."""
    return Image.new('RGB', (100, 100), color='red')

@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing."""
    return """
    John Doe
    Software Engineer
    
    Experience:
    - Developed web applications
    - Worked with Python and JavaScript
    
    Education:
    - Bachelor's in Computer Science
    """

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    env_vars = {
        'AZURE_OPENAI_API_KEY': 'test-api-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test-endpoint.openai.azure.com/',
        'AZURE_OPENAI_API_VERSION': '2024-02-15',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'gpt-4'
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    return env_vars
