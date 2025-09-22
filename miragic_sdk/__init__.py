"""
Miragic SDK - Advanced Image Processing Toolkit

A powerful Python SDK for advanced image processing and manipulation.
Transform your images with professional-grade AI-powered tools.
"""

__version__ = "1.0.0"
__author__ = "Miragic Team"
__email__ = "support@miragic.com"
__description__ = "Advanced image processing SDK with background removal, upscaling, and blur effects"

from .core import MiragicSDK
from .background_removal import BackgroundRemover
from .image_upscaler import ImageUpscaler
from .blur_background import BlurBackground
from .api_client import MiragicAPIClient

__all__ = [
    "MiragicSDK",
    "BackgroundRemover", 
    "ImageUpscaler",
    "BlurBackground",
    "MiragicAPIClient"
]
