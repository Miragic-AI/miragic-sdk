#!/usr/bin/env python3
"""
Build script for Miragic SDK package.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False


def clean_build_dirs():
    """Clean previous build artifacts."""
    print("\n🧹 Cleaning previous build artifacts...")
    
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for pattern in dirs_to_clean:
        for path in Path('.').glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"   Removed {path}")
            elif path.is_file():
                path.unlink()
                print(f"   Removed {path}")


def build_package():
    """Build the package."""
    commands = [
        ("python -m pip install --upgrade build", "Installing/upgrading build tools"),
        ("python -m build", "Building package"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def verify_package():
    """Verify the built package."""
    print("\n🔍 Verifying package...")
    
    # Check if dist directory exists and has files
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("❌ dist directory not found")
        return False
    
    files = list(dist_dir.glob('*'))
    if not files:
        print("❌ No files found in dist directory")
        return False
    
    print(f"✅ Found {len(files)} files in dist directory:")
    for file in files:
        print(f"   - {file.name} ({file.stat().st_size / 1024:.1f} KB)")
    
    return True


def main():
    """Main build process."""
    print("🚀 Starting Miragic SDK build process...")
    
    # Check if we're in the right directory
    if not Path('setup.py').exists():
        print("❌ setup.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build the package
    if not build_package():
        print("\n❌ Build failed!")
        sys.exit(1)
    
    # Verify the package
    if not verify_package():
        print("\n❌ Package verification failed!")
        sys.exit(1)
    
    print("\n🎉 Build completed successfully!")
    print("\nNext steps:")
    print("1. Test the package: python -m pip install dist/miragic_sdk-*.whl")
    print("2. Upload to PyPI: python scripts/upload.py")


if __name__ == "__main__":
    main()
