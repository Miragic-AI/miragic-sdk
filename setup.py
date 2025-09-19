"""
Setup script for Miragic SDK package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="miragic-sdk",
    version="1.0.0",
    author="Miragic Team",
    author_email="support@miragic.com",
    description="Advanced image processing SDK with background removal, upscaling, and blur effects",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/miragic/miragic-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/miragic/miragic-sdk/issues",
        "Documentation": "https://docs.miragic.com",
        "Homepage": "https://miragic.com",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: Image Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "miragic=miragic_sdk.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="image processing, background removal, upscaling, blur, AI, computer vision",
)
