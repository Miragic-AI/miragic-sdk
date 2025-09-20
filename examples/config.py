"""
Configuration file for Miragic SDK API usage examples.
"""

import os
from typing import Optional


class MiragicConfig:
    """
    Configuration class for Miragic SDK API settings.
    """
    
    def __init__(self):
        # API Configuration
        self.api_key: Optional[str] = os.getenv("MIRAGIC_API_KEY")
        self.api_base_url: str = os.getenv("MIRAGIC_API_BASE_URL", "https://api.miragic.com/v1")
        self.api_timeout: int = int(os.getenv("MIRAGIC_API_TIMEOUT", "30"))
        
        # Default processing parameters
        self.default_blur_strength: float = 0.8
        self.default_scale_factor: int = 2
        self.default_threshold: int = 128
        
        # File paths
        self.input_dir: str = "input"
        self.output_dir: str = "output"
        
        # Supported image formats
        self.supported_formats: list = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
    
    def validate(self) -> bool:
        """
        Validate configuration settings.
        
        Returns:
            bool: True if configuration is valid
        """
        if not self.api_key:
            print("❌ API key not found. Set MIRAGIC_API_KEY environment variable.")
            return False
        
        if not os.path.exists(self.input_dir):
            print(f"⚠️ Input directory '{self.input_dir}' does not exist.")
            return False
        
        return True
    
    def setup_directories(self):
        """
        Create necessary directories.
        """
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_sdk_config(self) -> dict:
        """
        Get SDK configuration dictionary.
        
        Returns:
            dict: SDK configuration
        """
        return {
            'api_key': self.api_key,
            'use_api': True,
            'api_base_url': self.api_base_url
        }


# Global configuration instance
config = MiragicConfig()
