"""
API client module for Miragic SDK server endpoints.
"""

import os
import requests
import base64
from typing import Union, Optional, Dict, Any
from PIL import Image
import io


class MiragicAPIClient:
    """
    Client for interacting with Miragic server API endpoints.
    """
    
    def __init__(self, 
                 api_key: str, 
                 base_url: str = "https://api.miragic.com/v1",
                 timeout: int = 30):
        """
        Initialize the API client.
        
        Args:
            api_key (str): Your Miragic API key
            base_url (str): Base URL for the API (default: https://api.miragic.com/v1)
            timeout (int): Request timeout in seconds (default: 30)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'Miragic-SDK/1.0.0'
        })
    
    def _encode_image(self, image_input: Union[str, bytes, Image.Image]) -> str:
        """
        Encode image to base64 string for API transmission.
        
        Args:
            image_input: Image path, bytes, or PIL Image object
            
        Returns:
            str: Base64 encoded image string
        """
        if isinstance(image_input, str):
            # File path
            with open(image_input, 'rb') as f:
                image_data = f.read()
        elif isinstance(image_input, bytes):
            # Raw bytes
            image_data = image_input
        elif isinstance(image_input, Image.Image):
            # PIL Image object
            buffer = io.BytesIO()
            image_input.save(buffer, format='PNG')
            image_data = buffer.getvalue()
        else:
            raise ValueError("Unsupported image input type")
        
        return base64.b64encode(image_data).decode('utf-8')
    
    def _decode_image(self, base64_string: str) -> bytes:
        """
        Decode base64 string to image bytes.
        
        Args:
            base64_string: Base64 encoded image string
            
        Returns:
            bytes: Decoded image bytes
        """
        return base64.b64decode(base64_string)
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make API request to the server.
        
        Args:
            endpoint: API endpoint path
            data: Request data
            
        Returns:
            Dict: API response
            
        Raises:
            requests.RequestException: If API request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.post(
                url, 
                json=data, 
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")
    
    def remove_background(self, 
                         image_input: Union[str, bytes, Image.Image],
                         **kwargs) -> Image.Image:
        """
        Remove background from an image using server API.
        
        Args:
            image_input: Input image (path, bytes, or PIL Image)
            **kwargs: Additional parameters for background removal
            
        Returns:
            Image.Image: Processed PIL Image
            
        Raises:
            RuntimeError: If API request fails
        """
        # Encode image to base64
        image_b64 = self._encode_image(image_input)
        
        # Prepare request data
        data = {
            'file': image_b64
        }
        
        # Make API request
        response = self._make_request('/remove_background_on_sdk_base64', data)
        
        # Decode and return PIL Image
        if 'base64' in response:
            image_bytes = self._decode_image(response['base64'])
            return Image.open(io.BytesIO(image_bytes))
        else:
            raise RuntimeError("Invalid API response: missing image data")
    
    def blur_background(self, 
                       image_input: Union[str, bytes, Image.Image],
                       blur_strength: float = 0.8,
                       **kwargs) -> Image.Image:
        """
        Apply blur effect to background using server API.
        
        Args:
            image_input: Input image (path, bytes, or PIL Image)
            blur_strength: Blur strength (0.0 to 1.0, default: 0.8)
            **kwargs: Additional parameters for blur effect
            
        Returns:
            Image.Image: Processed PIL Image
            
        Raises:
            RuntimeError: If API request fails
        """
        # Validate blur strength
        if not 0.0 <= blur_strength <= 1.0:
            raise ValueError("Blur strength must be between 0.0 and 1.0")
        
        # Encode image to base64
        image_b64 = self._encode_image(image_input)
        
        # Prepare request data
        data = {
            'file': image_b64
        }
        
        # Make API request
        response = self._make_request('/blur_background_on_sdk_base64', data)
        
        # Decode and return image
        if 'image' in response:
            image_bytes = self._decode_image(response['image'])
            return Image.open(io.BytesIO(image_bytes))
        else:
            raise RuntimeError("Invalid API response: missing image data")
    
    def upscale_image(self, 
                     image_input: Union[str, bytes, Image.Image],
                     scale_factor: int = 2,
                     **kwargs) -> Image.Image:
        """
        Upscale an image using server API.
        
        Args:
            image_input: Input image (path, bytes, or PIL Image)
            scale_factor: Scale factor (1-8, default: 2)
            **kwargs: Additional parameters for upscaling
            
        Returns:
            Image.Image: Upscaled PIL Image
            
        Raises:
            RuntimeError: If API request fails
        """
        # Validate scale factor
        if scale_factor < 1 or scale_factor > 8:
            raise ValueError("Scale factor must be between 1 and 8")
        
        # Encode image to base64
        image_b64 = self._encode_image(image_input)
        
        # Prepare request data
        data = {
            'file': image_b64
        }
        
        # Make API request
        response = self._make_request('/upscale_image_sdk_base64', data)
        
        # Decode and return image
        if 'image' in response:
            image_bytes = self._decode_image(response['image'])
            return Image.open(io.BytesIO(image_bytes))
        else:
            raise RuntimeError("Invalid API response: missing image data")
    
    def get_api_status(self) -> Dict[str, Any]:
        """
        Get API server status and available features.
        
        Returns:
            Dict: API status information
        """
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to get API status: {str(e)}")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get your API usage statistics.
        
        Returns:
            Dict: Usage statistics
        """
        try:
            response = self.session.get(f"{self.base_url}/usage", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to get usage stats: {str(e)}")

