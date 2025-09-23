"""
Core Miragic SDK class that provides the main interface for all image processing features.
"""

import os
from PIL import Image
from typing import Union, Optional
from .background_removal import BackgroundRemover
from .image_upscaler import ImageUpscaler
from .blur_background import BlurBackground
from .api_client import MiragicAPIClient


class MiragicSDK:
    """
    Main SDK class that provides access to all Miragic image processing features.
    
    This class serves as the primary interface for:
    - Background removal
    - Image upscaling
    - Background blur effects
    """
    
    def __init__(self, 
                 api_key: Optional[str] = "api_key",
                 use_api: bool = True,
                 api_base_url: str = "http://147.93.84.74:8085"):
        """
        Initialize the Miragic SDK.
        
        Args:
            api_key (str, optional): API key for enhanced features. 
                                   Can be None for basic free features.
            use_api (bool): Whether to use server API endpoints (default: False)
            api_base_url (str): Base URL for API endpoints (default: https://api.miragic.com/v1)
        """
        self.api_key = api_key
        self.use_api = use_api
        self.api_base_url = api_base_url
        
        if use_api:
            if not api_key:
                raise ValueError("API key is required when using server endpoints")
            self.api_client = MiragicAPIClient(api_key, api_base_url)
        else:
            self.background_remover = BackgroundRemover(api_key)
            self.image_upscaler = ImageUpscaler(api_key)
            self.blur_background = BlurBackground(api_key)
    
    def remove_background(self, 
                         input_path: Union[str, bytes], 
                         **kwargs) -> Image.Image:
        """
        Remove background from an image.
        
        Args:
            input_path (str or bytes): Path to input image or image data
            **kwargs: Additional parameters for background removal
            
        Returns:
            Image.Image: PIL Image object
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If input format is not supported
        """
        if self.use_api:
            # Use server API
            processed_image = self.api_client.remove_background(input_path, **kwargs)
            
            return processed_image
        else:
            # Use local processing
            return self.background_remover.remove_background(input_path, **kwargs)
    
    def upscale_image(self, 
                     input_path: Union[str, bytes], 
                     scale_factor: int = 2,
                     **kwargs) -> Image.Image:
        """
        Upscale an image to higher resolution.
        
        Args:
            input_path (str or bytes): Path to input image or image data
            scale_factor (int): Factor by which to scale the image (default: 2)
            **kwargs: Additional parameters for upscaling
            
        Returns:
            Image.Image: PIL Image object
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If scale factor is invalid
        """
        if self.use_api:
            # Use server API
            processed_image = self.api_client.upscale_image(input_path, scale_factor, **kwargs)
                
            return processed_image
        else:
            # Use local processing
            return self.image_upscaler.upscale(input_path, scale_factor, **kwargs)
    
    def blur_background(self, 
                       input_path: Union[str, bytes], 
                       blur_strength: float = 0.8,
                       **kwargs) -> Image.Image:
        """
        Apply blur effect to the background of an image.
        
        Args:
            input_path (str or bytes): Path to input image or image data
            blur_strength (float): Strength of blur effect (0.0 to 1.0, default: 0.8)
            **kwargs: Additional parameters for blur effect
            
        Returns:
            Image.Image: PIL Image object
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If blur strength is out of range
        """
        if self.use_api:
            # Use server API
            processed_image = self.api_client.blur_background(input_path, blur_strength, **kwargs)
            
            return processed_image
        else:
            # Use local processing
            return self.blur_background.apply_blur(input_path, blur_strength, **kwargs)
    
    def get_version(self) -> str:
        """
        Get the current SDK version.
        
        Returns:
            str: Current version string
        """
        from . import __version__
        return __version__
    
    def get_api_status(self) -> dict:
        """
        Get API server status (only available when using API mode).
        
        Returns:
            dict: API status information
            
        Raises:
            RuntimeError: If not using API mode
        """
        if not self.use_api:
            raise RuntimeError("API status is only available when using API mode")
        return self.api_client.get_api_status()
    
    def get_usage_stats(self) -> dict:
        """
        Get API usage statistics (only available when using API mode).
        
        Returns:
            dict: Usage statistics
            
        Raises:
            RuntimeError: If not using API mode
        """
        if not self.use_api:
            raise RuntimeError("Usage stats are only available when using API mode")
        return self.api_client.get_usage_stats()