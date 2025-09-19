"""
Command-line interface for Miragic SDK.
"""

import argparse
import sys
import os
from pathlib import Path
from .core import MiragicSDK


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Miragic SDK - Advanced Image Processing Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Remove background from an image
  miragic remove-bg input.jpg output.png
  
  # Upscale an image by 2x
  miragic upscale input.jpg output.jpg --scale 2
  
  # Apply background blur
  miragic blur-bg portrait.jpg output.jpg --strength 0.8
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='%(prog)s 1.0.0'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Background removal command
    remove_bg_parser = subparsers.add_parser(
        'remove-bg', 
        help='Remove background from an image'
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
        help='Upscale an image'
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
        help='Apply background blur effect'
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
        default=True, 
        help='Apply center-focused blur'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize SDK
    try:
        sdk = MiragicSDK()
    except Exception as e:
        print(f"❌ Failed to initialize Miragic SDK: {e}")
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == 'remove-bg':
            result = sdk.remove_background(
                args.input, 
                args.output, 
                threshold=args.threshold
            )
            print(f"✅ Background removed: {result}")
            
        elif args.command == 'upscale':
            result = sdk.upscale_image(
                args.input, 
                args.output, 
                scale_factor=args.scale,
                method=args.method,
                sharpen=args.sharpen
            )
            print(f"✅ Image upscaled: {result}")
            
        elif args.command == 'blur-bg':
            result = sdk.blur_background(
                args.input, 
                args.output, 
                blur_strength=args.strength,
                center_focus=args.center_focus
            )
            print(f"✅ Background blurred: {result}")
            
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Invalid parameter: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
