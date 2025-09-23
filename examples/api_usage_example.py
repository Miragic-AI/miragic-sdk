"""
Example script demonstrating how to use Miragic SDK with server API endpoints.

This script shows how to:
1. Initialize the SDK with API endpoints
2. Remove backgrounds from images
3. Apply blur effects to backgrounds
4. Upscale images
5. Check API status and usage statistics
"""

import os
from miragic_sdk import MiragicSDK


def main():
    """
    Main function demonstrating API usage.
    """
    
    # Initialize SDK with API endpoints
    print("🚀 Initializing Miragic SDK with API endpoints...")
    sdk = MiragicSDK()
    
    # Check API status
    print("\n📊 Checking API status...")
    try:
        status = sdk.get_api_status()
        print(f"✅ API Status: {status}")
    except Exception as e:
        print(f"❌ Failed to get API status: {e}")
    
    # Example image paths (replace with your actual image paths)
    input_image = "input.jpg"
    
    # 1. Background Removal Example
    print("\n🎭 Removing background from image...")
    try:
        sdk.remove_background(input_image).save("no_background.png")
    except Exception as e:
        print(f"❌ Background removal failed: {e}")
    
    # 2. Background Blur Example
    print("\n🌫️ Applying background blur...")
    try:
        sdk.blur_background(input_image).save("blurred_background.jpg")
    except Exception as e:
        print(f"❌ Background blur failed: {e}")
    
    # 3. Image Upscaling Example
    print("\n📈 Upscaling image...")
    try:
        sdk.upscale_image(input_image).save("upscaled_2x.jpg")
    except Exception as e:
        print(f"❌ Image upscaling failed: {e}")
    
    # 4. Get Usage Statistics
    print("\n📊 Getting usage statistics...")
    try:
        usage = sdk.get_usage_stats()
        print(f"✅ Usage stats: {usage}")
    except Exception as e:
        print(f"❌ Failed to get usage stats: {e}")
    
    print("\n🎉 API usage examples completed!")


def batch_processing_example():
    """
    Example of batch processing multiple images using API endpoints.
    """
    API_KEY = "your_api_key_here"
    
    # Initialize SDK
    sdk = MiragicSDK(api_key=API_KEY, use_api=True)
    
    # List of input images
    input_images = [
        "image1.jpg",
        "image2.jpg", 
        "image3.jpg"
    ]
    
    output_dir = "batch_output"
    os.makedirs(output_dir, exist_ok=True)
    
    print("🔄 Processing batch of images...")
    
    for i, input_image in enumerate(input_images):
        if not os.path.exists(input_image):
            print(f"⚠️ Skipping {input_image} (file not found)")
            continue
            
        print(f"Processing {input_image} ({i+1}/{len(input_images)})...")
        
        try:
            # Remove background
            sdk.remove_background(
                input_path=input_image,
                output_path=os.path.join(output_dir, f"bg_removed_{i+1}.png")
            )
            
            # Apply blur
            sdk.blur_background(
                input_path=input_image,
                output_path=os.path.join(output_dir, f"blurred_{i+1}.jpg"),
                blur_strength=0.6
            )
            
            # Upscale
            sdk.upscale_image(
                input_path=input_image,
                output_path=os.path.join(output_dir, f"upscaled_{i+1}.jpg"),
                scale_factor=2
            )
            
            print(f"✅ Completed processing {input_image}")
            
        except Exception as e:
            print(f"❌ Failed to process {input_image}: {e}")
    
    print("🎉 Batch processing completed!")


def advanced_parameters_example():
    """
    Example showing advanced parameters for each processing type.
    """
    API_KEY = "your_api_key_here"
    sdk = MiragicSDK(api_key=API_KEY, use_api=True)
    
    input_image = "portrait.jpg"
    output_dir = "advanced_output"
    os.makedirs(output_dir, exist_ok=True)
    
    print("🔧 Advanced parameters example...")
    
    # Advanced background removal
    try:
        sdk.remove_background(
            input_path=input_image,
            output_path=os.path.join(output_dir, "advanced_bg_removal.png"),
            threshold=150,           # Custom threshold
            edge_refinement=True,    # Better edge detection
            hair_detection=True      # Special handling for hair
        )
        print("✅ Advanced background removal completed")
    except Exception as e:
        print(f"❌ Advanced background removal failed: {e}")
    
    # Advanced blur with presets
    blur_presets = {
        'portrait': {'blur_strength': 0.8, 'center_focus': True},
        'product': {'blur_strength': 0.7, 'center_focus': True},
        'artistic': {'blur_strength': 0.9, 'center_focus': False}
    }
    
    for preset_name, params in blur_presets.items():
        try:
            sdk.blur_background(
                input_path=input_image,
                output_path=os.path.join(output_dir, f"blur_{preset_name}.jpg"),
                **params
            )
            print(f"✅ {preset_name} blur completed")
        except Exception as e:
            print(f"❌ {preset_name} blur failed: {e}")
    
    # Advanced upscaling with different methods
    upscale_methods = ['lanczos', 'bicubic', 'nearest']
    
    for method in upscale_methods:
        try:
            sdk.upscale_image(
                input_path=input_image,
                output_path=os.path.join(output_dir, f"upscaled_{method}.jpg"),
                scale_factor=3,
                method=method,
                sharpen=True,
                noise_reduction=True
            )
            print(f"✅ {method} upscaling completed")
        except Exception as e:
            print(f"❌ {method} upscaling failed: {e}")


if __name__ == "__main__":
    print("🎯 Miragic SDK API Usage Examples")
    print("=" * 50)
    
    # Run basic example
    main()
    
    # Uncomment to run additional examples
    # batch_processing_example()
    # advanced_parameters_example()
