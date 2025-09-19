#!/usr/bin/env python3
"""
Development installation script for Miragic SDK.
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


def install_dev_dependencies():
    """Install development dependencies."""
    commands = [
        ("python -m pip install --upgrade pip", "Upgrading pip"),
        ("python -m pip install -r requirements-dev.txt", "Installing development dependencies"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def install_package_editable():
    """Install the package in editable mode."""
    command = "python -m pip install -e ."
    return run_command(command, "Installing package in editable mode")


def run_tests():
    """Run the test suite."""
    command = "python -m pytest tests/ -v"
    return run_command(command, "Running tests")


def main():
    """Main development setup process."""
    print("🚀 Setting up Miragic SDK for development...")
    
    # Check if we're in the right directory
    if not Path('setup.py').exists():
        print("❌ setup.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Install development dependencies
    if not install_dev_dependencies():
        print("\n❌ Failed to install development dependencies!")
        sys.exit(1)
    
    # Install package in editable mode
    if not install_package_editable():
        print("\n❌ Failed to install package in editable mode!")
        sys.exit(1)
    
    # Run tests if they exist
    if Path('tests').exists():
        if not run_tests():
            print("\n⚠️  Tests failed, but development setup is complete.")
        else:
            print("\n✅ All tests passed!")
    
    print("\n🎉 Development setup completed successfully!")
    print("\nYou can now:")
    print("1. Make changes to the code")
    print("2. Run tests: python -m pytest tests/")
    print("3. Format code: black miragic_sdk/")
    print("4. Lint code: flake8 miragic_sdk/")
    print("5. Build package: python scripts/build.py")


if __name__ == "__main__":
    main()
