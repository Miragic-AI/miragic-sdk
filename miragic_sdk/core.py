"""
Core Miragic SDK class that provides the main interface for all image processing features.
"""

import os
from typing import Union, Optional
from .background_removal import BackgroundRemover
from .image_upscaler import ImageUpscaler
from .blur_background import BlurBackground


class MiragicSDK:
    """
    Main SDK class that provides access to all Miragic image processing features.
    
    This class serves as the primary interface for:
    - Background removal
    - Image upscaling
    - Background blur effects
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Miragic SDK.
        
        Args:
            api_key (str, optional): API key for enhanced features. 
                                   Can be None for basic free features.
        """
        self.api_key = api_key
        self.background_remover = BackgroundRemover(api_key)
        self.image_upscaler = ImageUpscaler(api_key)
        self.blur_background = BlurBackground(api_key)
    
    def remove_background(self, 
                         input_path: Union[str, bytes], 
                         output_path: str,
                         **kwargs) -> str:
        """
        Remove background from an image.
        
        Args:
            input_path (str or bytes): Path to input image or image data
            output_path (str): Path where the output image will be saved
            **kwargs: Additional parameters for background removal
            
        Returns:
            str: Path to the output image
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If input format is not supported
        """
        return self.background_remover.remove_background(input_path, output_path, **kwargs)
    
    def upscale_image(self, 
                     input_path: Union[str, bytes], 
                     output_path: str,
                     scale_factor: int = 2,
                     **kwargs) -> str:
        """
        Upscale an image to higher resolution.
        
        Args:
            input_path (str or bytes): Path to input image or image data
            output_path (str): Path where the upscaled image will be saved
            scale_factor (int): Factor by which to scale the image (default: 2)
            **kwargs: Additional parameters for upscaling
            
        Returns:
            str: Path to the upscaled image
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If scale factor is invalid
        """
        return self.image_upscaler.upscale(input_path, output_path, scale_factor, **kwargs)
    
    def blur_background(self, 
                       input_path: Union[str, bytes], 
                       output_path: str,
                       blur_strength: float = 0.8,
                       **kwargs) -> str:
        """
        Apply blur effect to the background of an image.
        
        Args:
            input_path (str or bytes): Path to input image or image data
            output_path (str): Path where the blurred image will be saved
            blur_strength (float): Strength of blur effect (0.0 to 1.0, default: 0.8)
            **kwargs: Additional parameters for blur effect
            
        Returns:
            str: Path to the blurred image
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If blur strength is out of range
        """
        return self.blur_background.apply_blur(input_path, output_path, blur_strength, **kwargs)
    
    def get_version(self) -> str:
        """
        Get the current SDK version.
        
        Returns:
            str: Current version string
        """
        from . import __version__
        return __version__
