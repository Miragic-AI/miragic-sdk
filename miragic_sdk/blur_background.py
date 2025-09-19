"""
Background blur module for the Miragic SDK.
"""

import os
from typing import Union, Optional
from PIL import Image, ImageFilter
import numpy as np


class BlurBackground:
    """
    Handles background blur effects for images.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the background blur processor.
        
        Args:
            api_key (str, optional): API key for enhanced features
        """
        self.api_key = api_key
        self._model_loaded = False
    
    def apply_blur(self, 
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
            **kwargs: Additional parameters
            
        Returns:
            str: Path to the blurred image
        """
        try:
            # Validate blur strength
            if not 0.0 <= blur_strength <= 1.0:
                raise ValueError("Blur strength must be between 0.0 and 1.0")
            
            # Load the input image
            if isinstance(input_path, str):
                if not os.path.exists(input_path):
                    raise FileNotFoundError(f"Input file not found: {input_path}")
                image = Image.open(input_path)
            else:
                image = Image.open(input_path)
            
            # Apply blur algorithm
            blurred_image = self._apply_blur_algorithm(image, blur_strength, **kwargs)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save the result
            blurred_image.save(output_path, quality=kwargs.get('quality', 95))
            
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"Background blur failed: {str(e)}")
    
    def _apply_blur_algorithm(self, 
                             image: Image.Image, 
                             blur_strength: float, 
                             **kwargs) -> Image.Image:
        """
        Core background blur algorithm.
        
        This is a placeholder implementation. In a real SDK, this would
        use advanced AI models to identify and blur only the background.
        
        Args:
            image (Image.Image): Input image
            blur_strength (float): Blur strength (0.0 to 1.0)
            **kwargs: Additional parameters
            
        Returns:
            Image.Image: Image with blurred background
        """
        # Convert to RGB if necessary
        if image.mode == 'RGBA':
            # Create a white background for RGBA images
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Calculate blur radius based on strength
        max_radius = kwargs.get('max_radius', 20)
        blur_radius = int(blur_strength * max_radius)
        
        # Apply Gaussian blur
        blurred = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        # In a real implementation, this would:
        # 1. Use AI to identify the subject/foreground
        # 2. Create a mask for the background
        # 3. Apply blur only to the background areas
        # 4. Composite the sharp foreground with blurred background
        
        # For now, we'll apply a simple center-focused blur effect
        if kwargs.get('center_focus', True):
            blurred = self._apply_center_focus_blur(image, blurred, blur_strength)
        
        return blurred
    
    def _apply_center_focus_blur(self, 
                                original: Image.Image, 
                                blurred: Image.Image, 
                                blur_strength: float) -> Image.Image:
        """
        Apply center-focused blur effect.
        
        Args:
            original (Image.Image): Original sharp image
            blurred (Image.Image): Blurred image
            blur_strength (float): Blur strength
            
        Returns:
            Image.Image: Image with center-focused blur
        """
        # Create a radial gradient mask
        width, height = original.size
        mask = Image.new('L', (width, height), 0)
        
        # Create radial gradient from center
        center_x, center_y = width // 2, height // 2
        max_distance = min(center_x, center_y)
        
        for y in range(height):
            for x in range(width):
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                # Normalize distance and apply blur strength
                normalized_distance = min(distance / max_distance, 1.0)
                mask_value = int(255 * normalized_distance * blur_strength)
                mask.putpixel((x, y), mask_value)
        
        # Apply the mask to blend original and blurred images
        result = Image.composite(original, blurred, mask)
        
        return result
    
    def batch_apply_blur(self, 
                        input_paths: list, 
                        output_dir: str,
                        blur_strength: float = 0.8,
                        **kwargs) -> list:
        """
        Apply blur effect to multiple images.
        
        Args:
            input_paths (list): List of input image paths
            output_dir (str): Directory to save blurred images
            blur_strength (float): Blur strength
            **kwargs: Additional parameters
            
        Returns:
            list: List of output image paths
        """
        output_paths = []
        
        for i, input_path in enumerate(input_paths):
            filename = os.path.basename(input_path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}_blurred{ext}")
            
            try:
                result_path = self.apply_blur(input_path, output_path, blur_strength, **kwargs)
                output_paths.append(result_path)
            except Exception as e:
                print(f"Failed to blur {input_path}: {str(e)}")
                continue
        
        return output_paths
    
    def get_blur_presets(self) -> dict:
        """
        Get predefined blur presets.
        
        Returns:
            dict: Dictionary of blur presets
        """
        return {
            'light': {'blur_strength': 0.3, 'max_radius': 10},
            'medium': {'blur_strength': 0.6, 'max_radius': 15},
            'strong': {'blur_strength': 0.9, 'max_radius': 25},
            'portrait': {'blur_strength': 0.8, 'max_radius': 20, 'center_focus': True},
            'product': {'blur_strength': 0.7, 'max_radius': 18, 'center_focus': True}
        }
