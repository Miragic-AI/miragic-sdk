# Miragic SDK API Usage Examples

This directory contains examples showing how to use the Miragic SDK with server API endpoints.

## Quick Start

### 1. Basic API Usage

```python
from miragic_sdk import MiragicSDK

# Initialize with API endpoints
sdk = MiragicSDK(
    api_key="your_api_key_here",
    use_api=True,  # Enable API mode
    api_base_url="https://api.miragic.com/v1"
)

# Remove background
result = sdk.remove_background("input.jpg", "output.png")

# Apply blur
result = sdk.blur_background("input.jpg", "blurred.jpg", blur_strength=0.8)

# Upscale image
result = sdk.upscale_image("input.jpg", "upscaled.jpg", scale_factor=2)
```

### 2. Check API Status

```python
# Get API server status
status = sdk.get_api_status()
print(f"API Status: {status}")

# Get usage statistics
usage = sdk.get_usage_stats()
print(f"Usage: {usage}")
```

## API Endpoints

The SDK supports the following server API endpoints:

### Background Removal
- **Endpoint**: `POST /background-removal`
- **Parameters**: 
  - `image`: Base64 encoded image
  - `format`: Output format (default: png)
  - `parameters`: Additional processing parameters

### Background Blur
- **Endpoint**: `POST /blur-background`
- **Parameters**:
  - `image`: Base64 encoded image
  - `blur_strength`: Blur intensity (0.0-1.0)
  - `parameters`: Additional blur parameters

### Image Upscaling
- **Endpoint**: `POST /upscale`
- **Parameters**:
  - `image`: Base64 encoded image
  - `scale_factor`: Scale multiplier (1-8)
  - `parameters`: Additional upscaling parameters

## Configuration

### Environment Variables

You can set your API key as an environment variable:

```bash
export MIRAGIC_API_KEY="your_api_key_here"
```

Then use it in your code:

```python
import os
from miragic_sdk import MiragicSDK

sdk = MiragicSDK(
    api_key=os.getenv("MIRAGIC_API_KEY"),
    use_api=True
)
```

### Custom API Base URL

If you're using a custom API server:

```python
sdk = MiragicSDK(
    api_key="your_api_key",
    use_api=True,
    api_base_url="https://your-custom-api.com/v1"
)
```

## Error Handling

The SDK provides comprehensive error handling:

```python
try:
    result = sdk.remove_background("input.jpg", "output.png")
    print(f"Success: {result}")
except FileNotFoundError:
    print("Input file not found")
except ValueError as e:
    print(f"Invalid parameter: {e}")
except RuntimeError as e:
    print(f"API request failed: {e}")
```

## Batch Processing

Process multiple images efficiently:

```python
input_images = ["image1.jpg", "image2.jpg", "image3.jpg"]

for i, image in enumerate(input_images):
    try:
        # Remove background
        sdk.remove_background(image, f"output_{i}_no_bg.png")
        
        # Apply blur
        sdk.blur_background(image, f"output_{i}_blurred.jpg", blur_strength=0.7)
        
        # Upscale
        sdk.upscale_image(image, f"output_{i}_upscaled.jpg", scale_factor=2)
        
    except Exception as e:
        print(f"Failed to process {image}: {e}")
```

## Advanced Parameters

### Background Removal Parameters
- `threshold`: Background detection threshold (0-255)
- `edge_refinement`: Enable edge refinement (boolean)
- `hair_detection`: Special hair handling (boolean)

### Blur Parameters
- `blur_strength`: Blur intensity (0.0-1.0)
- `center_focus`: Focus blur on center (boolean)
- `max_radius`: Maximum blur radius (integer)

### Upscaling Parameters
- `scale_factor`: Scale multiplier (1-8)
- `method`: Upscaling method ('lanczos', 'bicubic', 'nearest')
- `sharpen`: Apply sharpening (boolean)
- `noise_reduction`: Reduce noise (boolean)

## Examples

Run the example script:

```bash
python api_usage_example.py
```

Make sure to:
1. Replace `"your_api_key_here"` with your actual API key
2. Update image paths to point to your actual images
3. Ensure you have the required dependencies installed

## Dependencies

The API client requires:
- `requests`: For HTTP requests
- `PIL` (Pillow): For image processing
- `numpy`: For image array operations

Install with:
```bash
pip install requests pillow numpy
```
