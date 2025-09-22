#!/usr/bin/env python3
"""
Upload script for Miragic SDK package to PyPI.
"""

import os
import sys
import subprocess
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


def check_dist_files():
    """Check if distribution files exist."""
    print("\n🔍 Checking distribution files...")
    
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("❌ dist directory not found. Please run build.py first.")
        return False
    
    files = list(dist_dir.glob('*'))
    if not files:
        print("❌ No files found in dist directory. Please run build.py first.")
        return False
    
    print(f"✅ Found {len(files)} distribution files:")
    for file in files:
        print(f"   - {file.name}")
    
    return True


def upload_to_testpypi():
    """Upload to TestPyPI first."""
    print("\n📤 Uploading to TestPyPI...")
    
    command = "python -m twine upload --repository testpypi dist/*"
    
    if not run_command(command, "Uploading to TestPyPI"):
        return False
    
    print("\n✅ Upload to TestPyPI completed!")
    print("\nYou can test the package with:")
    print("pip install --index-url https://test.pypi.org/simple/ miragic-sdk")
    
    return True


def upload_to_pypi():
    """Upload to PyPI."""
    print("\n📤 Uploading to PyPI...")
    
    command = "python -m twine upload dist/*"
    
    if not run_command(command, "Uploading to PyPI"):
        return False
    
    print("\n✅ Upload to PyPI completed!")
    print("\nPackage is now available at:")
    print("https://pypi.org/project/miragic-sdk/")
    
    return True


def main():
    """Main upload process."""
    print("🚀 Starting Miragic SDK upload process...")
    
    # Check if we're in the right directory
    if not Path('pyproject.toml').exists():
        print("❌ pyproject.toml not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Check distribution files
    if not check_dist_files():
        sys.exit(1)
    
    # Ask user for upload destination
    print("\n📋 Upload options:")
    print("1. TestPyPI (recommended for testing)")
    print("2. PyPI (production release)")
    print("3. Both (TestPyPI first, then PyPI)")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        if not upload_to_testpypi():
            sys.exit(1)
    elif choice == "2":
        if not upload_to_pypi():
            sys.exit(1)
    elif choice == "3":
        if not upload_to_testpypi():
            sys.exit(1)
        print("\n" + "="*50)
        input("Press Enter to continue with PyPI upload...")
        if not upload_to_pypi():
            sys.exit(1)
    else:
        print("❌ Invalid choice. Please run the script again.")
        sys.exit(1)
    
    print("\n🎉 Upload process completed successfully!")


if __name__ == "__main__":
    main()
