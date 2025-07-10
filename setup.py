#!/usr/bin/env python3
"""
Setup script for Jarvis Voice Assistant
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
    name="jarvis-voice-assistant",
    version="1.0.0",
    author="Jarvis Voice Assistant Team",
    author_email="your-email@example.com",
    description="An AI-powered voice assistant with face authorization and multiple AI integrations",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jarvis-voice-assistant",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
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
            "jarvis=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
    keywords=[
        "voice-assistant",
        "ai",
        "speech-recognition",
        "text-to-speech",
        "face-recognition",
        "personal-assistant",
        "automation",
        "linux",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/jarvis-voice-assistant/issues",
        "Source": "https://github.com/yourusername/jarvis-voice-assistant",
        "Documentation": "https://github.com/yourusername/jarvis-voice-assistant#readme",
    },
) 