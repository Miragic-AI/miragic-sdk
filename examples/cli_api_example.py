#!/usr/bin/env python3
"""
Command-line interface example for Miragic SDK API usage.
"""

import argparse
import sys
import os
from pathlib import Path

# Add parent directory to path to import miragic_sdk
sys.path.insert(0, str(Path(__file__).parent.parent))

from miragic_sdk import MiragicSDK
from config import config


def setup_sdk() -> MiragicSDK:
    """
    Setup and initialize the Miragic SDK with API configuration.
    
    Returns:
        MiragicSDK: Initialized SDK instance
    """
    if not config.validate():
        sys.exit(1)
    
    config.setup_directories()
    
    return MiragicSDK(**config.get_sdk_config())


def remove_background_command(args):
    """Handle background removal command."""
    sdk = setup_sdk()
    
    try:
        result = sdk.remove_background(
            input_path=args.input,
            output_path=args.output,
            threshold=args.threshold
        )
        print(f"✅ Background removed: {result}")
    except Exception as e:
        print(f"❌ Background removal failed: {e}")
        sys.exit(1)


def blur_background_command(args):
    """Handle background blur command."""
    sdk = setup_sdk()
    
    try:
        result = sdk.blur_background(
            input_path=args.input,
            output_path=args.output,
            blur_strength=args.strength,
            center_focus=args.center_focus
        )
        print(f"✅ Background blurred: {result}")
    except Exception as e:
        print(f"❌ Background blur failed: {e}")
        sys.exit(1)


def upscale_command(args):
    """Handle image upscaling command."""
    sdk = setup_sdk()
    
    try:
        result = sdk.upscale_image(
            input_path=args.input,
            output_path=args.output,
            scale_factor=args.scale,
            method=args.method,
            sharpen=args.sharpen
        )
        print(f"✅ Image upscaled: {result}")
    except Exception as e:
        print(f"❌ Image upscaling failed: {e}")
        sys.exit(1)


def status_command(args):
    """Handle status command."""
    sdk = setup_sdk()
    
    try:
        status = sdk.get_api_status()
        print("📊 API Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"❌ Failed to get API status: {e}")
        sys.exit(1)


def usage_command(args):
    """Handle usage statistics command."""
    sdk = setup_sdk()
    
    try:
        usage = sdk.get_usage_stats()
        print("📈 Usage Statistics:")
        for key, value in usage.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"❌ Failed to get usage stats: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Miragic SDK API CLI - Process images using server endpoints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Remove background from an image
  python cli_api_example.py remove-bg input.jpg output.png
  
  # Upscale an image by 2x
  python cli_api_example.py upscale input.jpg output.jpg --scale 2
  
  # Apply background blur
  python cli_api_example.py blur-bg portrait.jpg output.jpg --strength 0.8
  
  # Check API status
  python cli_api_example.py status
  
  # Get usage statistics
  python cli_api_example.py usage
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='Miragic SDK API CLI 1.0.0'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Background removal command
    remove_bg_parser = subparsers.add_parser(
        'remove-bg', 
        help='Remove background from an image using API'
    )
    remove_bg_parser.add_argument('input', help='Input image path')
    remove_bg_parser.add_argument('output', help='Output image path')
    remove_bg_parser.add_argument(
        '--threshold', 
        type=int, 
        default=128, 
        help='Background removal threshold (0-255)'
    )
    
    # Image upscaling command
    upscale_parser = subparsers.add_parser(
        'upscale', 
        help='Upscale an image using API'
    )
    upscale_parser.add_argument('input', help='Input image path')
    upscale_parser.add_argument('output', help='Output image path')
    upscale_parser.add_argument(
        '--scale', 
        type=int, 
        default=2, 
        help='Scale factor (1-8)'
    )
    upscale_parser.add_argument(
        '--method', 
        choices=['lanczos', 'bicubic', 'nearest'], 
        default='lanczos', 
        help='Upscaling method'
    )
    upscale_parser.add_argument(
        '--sharpen', 
        action='store_true',
        help='Apply sharpening after upscaling'
    )
    
    # Background blur command
    blur_parser = subparsers.add_parser(
        'blur-bg', 
        help='Apply background blur using API'
    )
    blur_parser.add_argument('input', help='Input image path')
    blur_parser.add_argument('output', help='Output image path')
    blur_parser.add_argument(
        '--strength', 
        type=float, 
        default=0.8, 
        help='Blur strength (0.0-1.0)'
    )
    blur_parser.add_argument(
        '--center-focus', 
        action='store_true',
        help='Focus blur on center of image'
    )
    
    # Status command
    status_parser = subparsers.add_parser(
        'status', 
        help='Check API server status'
    )
    
    # Usage command
    usage_parser = subparsers.add_parser(
        'usage', 
        help='Get API usage statistics'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == 'remove-bg':
        remove_background_command(args)
    elif args.command == 'upscale':
        upscale_command(args)
    elif args.command == 'blur-bg':
        blur_background_command(args)
    elif args.command == 'status':
        status_command(args)
    elif args.command == 'usage':
        usage_command(args)


if __name__ == "__main__":
    main()
