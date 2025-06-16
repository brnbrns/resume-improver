"""
Object-oriented model configuration and management.
"""

import os
from typing import Optional
from dataclasses import dataclass

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from dotenv import load_dotenv


@dataclass
class ModelConfig:
    """Configuration data class for Azure OpenAI model settings."""
    api_key: str
    endpoint: str
    api_version: str = "2025-01-01"
    deployment_name: str = "gpt-4o"
    
    def __post_init__(self):
        """Validate required configuration after initialization."""
        if not self.api_key:
            raise ValueError("AZURE_OPENAI_API_KEY is required")
        if not self.endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT is required")
        if not self.api_version:
            raise ValueError("AZURE_OPENAI_API_VERSION is required")
        if not self.deployment_name:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME is required")


class ModelManager:
    """Manages Azure OpenAI model client configuration and creation."""
    
    def __init__(self, config: Optional[ModelConfig] = None, load_env: bool = True):
        """
        Initialize the model manager.
        
        Args:
            config: Optional ModelConfig instance. If None, loads from environment.
            load_env: Whether to load environment variables from .env file
        """
        if load_env:
            load_dotenv()
        
        self._config = config
        self._client = None
        
        if config is None:
            self._config = self._load_config_from_env()
    
    def _load_config_from_env(self) -> ModelConfig:
        """
        Load configuration from environment variables.
        
        Returns:
            ModelConfig: Configuration loaded from environment
            
        Raises:
            ValueError: If required environment variables are missing
        """
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
        
        if not api_key or not endpoint:
            raise ValueError(
                "Please set Azure Open AI Endpoint Details in your environment variables. "
                "Required: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT"
            )
        
        return ModelConfig(
            api_key=api_key,
            endpoint=endpoint,
            api_version=api_version,
            deployment_name=deployment_name
        )
    
    @property
    def config(self) -> ModelConfig:
        """Get the current model configuration."""
        return self._config
    
    @property
    def client(self) -> AzureOpenAIChatCompletionClient:
        """
        Get or create the Azure OpenAI client.
        
        Returns:
            AzureOpenAIChatCompletionClient: Configured client instance
        """
        if self._client is None:
            self._client = self._create_client()
        return self._client
    
    def _create_client(self) -> AzureOpenAIChatCompletionClient:
        """
        Create a new Azure OpenAI client with current configuration.
        
        Returns:
            AzureOpenAIChatCompletionClient: New client instance
        """
        return AzureOpenAIChatCompletionClient(
            azure_deployment=self._config.deployment_name,
            model=self._config.deployment_name,
            api_key=self._config.api_key,
            azure_endpoint=self._config.endpoint,
            api_version=self._config.api_version,
        )
    
    def update_config(self, **kwargs) -> None:
        """
        Update configuration with new values.
        
        Args:
            **kwargs: Configuration parameters to update
        """
        # Create new config with updated values
        config_dict = {
            'api_key': self._config.api_key,
            'endpoint': self._config.endpoint,
            'api_version': self._config.api_version,
            'deployment_name': self._config.deployment_name,        }
        config_dict.update(kwargs)
        
        self._config = ModelConfig(**config_dict)
        # Reset client to force recreation with new config
        self._client = None
