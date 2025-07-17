#!/usr/bin/env python3
"""
Test script for Jarvis AI Assistant's handle_unknown_request function.
This script tests various types of commands to verify code generation and module installation.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from utils import handle_unknown_request, is_code_worthy
import sys
import os

# Add the current directory to Python path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test commands covering different categories
TEST_COMMANDS = [
    # Data Analysis & Visualization
    "create a bar chart showing sales data for different months",
    "plot a sine wave with different colors",
    "generate a scatter plot of random data points",
    "create a histogram of normally distributed data",
    "draw a pie chart showing market share percentages",
    
    # File Operations
    "read a CSV file and display the first 5 rows",
    "create a text file with sample data",
    "list all files in the current directory",
    "count the number of lines in a file",
    "copy files from one folder to another",
    
    # Web Scraping & API
    "fetch data from a JSON API and display it",
    "scrape a website and extract all links",
    "download an image from a URL",
    "parse HTML content and extract text",
    "make an HTTP request and show the response",
    
    # Mathematical Operations
    "calculate the factorial of a number",
    "solve a quadratic equation",
    "generate prime numbers up to 100",
    "calculate the Fibonacci sequence",
    "perform matrix multiplication",
    
    # System Operations
    "get system information like CPU and memory usage",
    "check disk space usage",
    "list running processes",
    "get current date and time",
    "create a directory and some files in it",
    
    # Data Processing
    "sort a list of numbers in ascending order",
    "find the maximum and minimum values in a dataset",
    "calculate the average of a list of numbers",
    "filter data based on certain criteria",
    "convert data between different formats",
    
    # Image Processing
    "resize an image to specific dimensions",
    "convert an image to grayscale",
    "apply a blur effect to an image",
    "detect edges in an image",
    "create a simple image with shapes",
    
    # Machine Learning (Basic)
    "create a simple linear regression model",
    "generate random data for clustering",
    "calculate correlation between two datasets",
    "perform basic statistical analysis",
    "create a decision tree visualization",
    
    # Network Operations
    "ping a website and show response time",
    "check if a port is open on localhost",
    "get the IP address of a domain",
    "download a file from the internet",
    "create a simple HTTP server",
    
    # Text Processing
    "count words in a text string",
    "find the most common words in text",
    "convert text to uppercase and lowercase",
    "remove punctuation from text",
    "split text into sentences",
    
    # Database Operations
    "create a simple SQLite database",
    "insert data into a database table",
    "query data from a database",
    "export database data to CSV",
    "backup a database file",
    
    # Audio Processing
    "generate a simple sine wave audio",
    "play a beep sound",
    "record audio from microphone",
    "analyze audio frequency spectrum",
    "convert audio file format",
    
    # GUI Applications
    "create a simple GUI window",
    "make a button that shows a message",
    "create a text input field",
    "display a message box",
    "create a simple calculator interface",
    
    # Games & Simulations
    "create a simple number guessing game",
    "simulate a coin flip",
    "generate a random password",
    "create a simple dice rolling simulator",
    "make a basic text adventure game",
    
    # Utilities
    "create a timer that counts down",
    "generate a QR code",
    "encrypt and decrypt text",
    "compress and decompress data",
    "create a log file with timestamps"
]

# Non-code-worthy commands (should be rejected)
NON_CODE_COMMANDS = [
    "how are you today?",
    "tell me a joke",
    "what's the weather like?",
    "what time is it?",
    "who created you?",
    "do you like pizza?",
    "what's your favorite color?",
    "can you sing a song?",
    "tell me about yourself",
    "what's the meaning of life?"
]

@pytest.mark.asyncio
@pytest.mark.parametrize("command", TEST_COMMANDS)
async def test_code_command(command):
    is_code = is_code_worthy(command)
    assert is_code, f"Command should be code-worthy: {command}"
    result = await handle_unknown_request(command, "test_model")
    assert result and len(result.strip()) > 10 and "error" not in result.lower(), f"Failed for: {command} | Result: {result}"

@pytest.mark.asyncio
@pytest.mark.parametrize("command", NON_CODE_COMMANDS)
async def test_non_code_command(command):
    is_code = is_code_worthy(command)
    assert not is_code, f"Non-code command misclassified: {command}"

# Example: test face auth with mock
@patch("faceAuthorization.faceDetection.cv2.VideoCapture")
def test_face_auth_success(mock_video):
    from faceAuthorization.faceDetection import check_authorization
    # Mock the video capture and face recognition
    mock_video.return_value.isOpened.return_value = True
    mock_video.return_value.read.return_value = (True, MagicMock())
    with patch("faceAuthorization.faceDetection.face_recognition.face_encodings", return_value=[MagicMock()]):
        with patch("faceAuthorization.faceDetection.face_recognition.compare_faces", return_value=[True]):
            assert check_authorization("dummy_path") is True

@patch("faceAuthorization.faceDetection.cv2.VideoCapture")
def test_face_auth_fail(mock_video):
    from faceAuthorization.faceDetection import check_authorization
    mock_video.return_value.isOpened.return_value = False
    assert check_authorization("dummy_path") is False

# Add more unit tests for utils as needed, mocking subprocess and network calls 