#!/usr/bin/env python3
"""
Test script for Jarvis AI Assistant's handle_unknown_request function.
This script tests various types of commands to verify code generation and module installation.
"""

import asyncio
import sys
import os

# Add the current directory to Python path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import handle_unknown_request, is_code_worthy

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

async def test_command(command, test_type="code", debug=False):
    """Test a single command and return the result."""
    print(f"\n{'='*80}")
    print(f"Testing {test_type.upper()} command: {command}")
    print(f"{'='*80}")
    
    try:
        # Test if command is code-worthy
        is_code = is_code_worthy(command)
        print(f"Code-worthy: {is_code}")
        
        if test_type == "non-code" and is_code:
            print("❌ ERROR: Non-code command was classified as code-worthy!")
            return False
        elif test_type == "code" and not is_code:
            print("❌ ERROR: Code command was classified as non-code-worthy!")
            return False
        
        if test_type == "code":
            # Test the actual function
            print("Generating and executing code...")
            
            if debug:
                print("🔍 Debug mode: Will show detailed information")
            
            result = await handle_unknown_request(command, "test_model")
            
            if debug:
                print(f"🔍 Raw result length: {len(result)}")
                print(f"🔍 Result preview: {result[:200]}...")
            
            print(f"Result: {result}")
            
            # More detailed error analysis
            if "error" in result.lower() or "failed" in result.lower():
                print("❌ Command failed or had errors")
                print(f"Error details: {result}")
                return False
            elif "timeout" in result.lower():
                print("⏰ Command timed out")
                return False
            elif "module" in result.lower() and "install" in result.lower():
                print("📦 Module installation issue")
                return False
            elif len(result.strip()) < 10:
                print("⚠️  Very short or empty result")
                return False
            elif "sorry" in result.lower() and "encountered" in result.lower():
                print("❌ Generic error response")
                return False
            else:
                print("✅ Command executed successfully")
                return True
        else:
            print("✅ Non-code command correctly rejected")
            return True
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

async def run_tests(debug=False):
    """Run all tests and provide a summary."""
    print("🧪 Starting Jarvis AI Assistant Tests")
    print("This will test code generation, module installation, and execution")
    
    if debug:
        print("🔍 Debug mode enabled - detailed output will be shown")
    
    results = {
        "code_commands": {"total": 0, "passed": 0, "failed": 0},
        "non_code_commands": {"total": 0, "passed": 0, "failed": 0}
    }
    
    # Test code-worthy commands
    print(f"\n📊 Testing {len(TEST_COMMANDS)} code-worthy commands...")
    for i, command in enumerate(TEST_COMMANDS, 1):
        print(f"\nProgress: {i}/{len(TEST_COMMANDS)}")
        results["code_commands"]["total"] += 1
        
        success = await test_command(command, "code", debug)
        if success:
            results["code_commands"]["passed"] += 1
        else:
            results["code_commands"]["failed"] += 1
            
        # Add a small delay between tests to avoid overwhelming the system
        if i % 5 == 0:
            print("⏸️  Pausing for 2 seconds...")
            await asyncio.sleep(2)
    
    # Test non-code commands
    print(f"\n📊 Testing {len(NON_CODE_COMMANDS)} non-code commands...")
    for i, command in enumerate(NON_CODE_COMMANDS, 1):
        print(f"\nProgress: {i}/{len(NON_CODE_COMMANDS)}")
        results["non_code_commands"]["total"] += 1
        
        success = await test_command(command, "non-code", debug)
        if success:
            results["non_code_commands"]["passed"] += 1
        else:
            results["non_code_commands"]["failed"] += 1
    
    # Print summary
    print(f"\n{'='*80}")
    print("📈 TEST SUMMARY")
    print(f"{'='*80}")
    
    code_stats = results["code_commands"]
    non_code_stats = results["non_code_commands"]
    
    print(f"Code Commands:")
    print(f"  Total: {code_stats['total']}")
    print(f"  Passed: {code_stats['passed']} ({(code_stats['passed']/code_stats['total']*100):.1f}%)")
    print(f"  Failed: {code_stats['failed']} ({(code_stats['failed']/code_stats['total']*100):.1f}%)")
    
    print(f"\nNon-Code Commands:")
    print(f"  Total: {non_code_stats['total']}")
    print(f"  Passed: {non_code_stats['passed']} ({(non_code_stats['passed']/non_code_stats['total']*100):.1f}%)")
    print(f"  Failed: {non_code_stats['failed']} ({(non_code_stats['failed']/non_code_stats['total']*100):.1f}%)")
    
    total_passed = code_stats['passed'] + non_code_stats['passed']
    total_tests = code_stats['total'] + non_code_stats['total']
    
    print(f"\nOverall Results:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {total_passed} ({(total_passed/total_tests*100):.1f}%)")
    print(f"  Failed: {total_tests - total_passed} ({((total_tests - total_passed)/total_tests*100):.1f}%)")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! Jarvis is working perfectly!")
    else:
        print(f"\n⚠️  {total_tests - total_passed} tests failed. Check the output above for details.")
        
        # Provide suggestions for common issues
        if code_stats['failed'] > code_stats['passed']:
            print("\n💡 Suggestions for improving success rate:")
            print("  1. Check if Mistral API key is configured correctly")
            print("  2. Verify internet connection for API calls")
            print("  3. Ensure pip is available for module installation")
            print("  4. Check if Python 3 is available as 'python3'")
            print("  5. Verify write permissions in /tmp directory")
            print("  6. Consider running with --debug flag for detailed output")

def test_specific_command():
    """Test a specific command that you can modify."""
    command = "create a simple bar chart with sample data"
    print(f"Testing specific command: {command}")
    
    async def run_specific_test():
        await test_command(command, "code")
    
    asyncio.run(run_specific_test())

def run_diagnostics():
    """Run basic diagnostics to check system requirements."""
    print("🔧 Running system diagnostics...")
    
    issues = []
    
    # Check Python version
    try:
        import sys
        print(f"✓ Python version: {sys.version}")
        if sys.version_info < (3, 7):
            issues.append("Python 3.7+ required")
    except Exception as e:
        issues.append(f"Python version check failed: {e}")
    
    # Check if pip is available
    try:
        import subprocess
        result = subprocess.run(['pip', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ pip available: {result.stdout.strip()}")
        else:
            issues.append("pip not available")
    except Exception as e:
        issues.append(f"pip check failed: {e}")
    
    # Check if python3 is available
    try:
        result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ python3 available: {result.stdout.strip()}")
        else:
            issues.append("python3 not available")
    except Exception as e:
        issues.append(f"python3 check failed: {e}")
    
    # Check /tmp directory permissions
    try:
        import tempfile
        import os
        test_file = os.path.join('/tmp', 'jarvis_test_write')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("✓ /tmp directory writable")
    except Exception as e:
        issues.append(f"/tmp directory not writable: {e}")
    
    # Check if config.py exists
    try:
        import config
        print("✓ config.py found")
    except ImportError:
        issues.append("config.py not found or not importable")
    
    # Check if Mistral API key is configured
    try:
        import config
        if hasattr(config, 'MISTRAL_API_KEY') and config.MISTRAL_API_KEY:
            print("✓ Mistral API key configured")
        else:
            issues.append("Mistral API key not configured")
    except Exception as e:
        issues.append(f"Mistral API key check failed: {e}")
    
    # Check if required modules are available
    required_modules = ['asyncio', 'subprocess', 'os', 'time', 'json', 'requests']
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} available")
        except ImportError:
            issues.append(f"{module} not available")
    
    # Check if secondaryClassifier is available
    try:
        from secondaryClassifier import is_code_worthy
        print("✓ secondaryClassifier available")
    except ImportError as e:
        issues.append(f"secondaryClassifier not available: {e}")
    
    print(f"\nDiagnostic Results:")
    if issues:
        print(f"❌ Found {len(issues)} issues:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ All system requirements met!")
        return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Jarvis AI Assistant")
    parser.add_argument("--specific", action="store_true", 
                       help="Test a specific command (modify test_specific_command function)")
    parser.add_argument("--quick", action="store_true",
                       help="Run only first 5 commands of each type for quick testing")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode for detailed output")
    parser.add_argument("--diagnose", action="store_true",
                       help="Run system diagnostics only")
    
    args = parser.parse_args()
    
    if args.diagnose:
        run_diagnostics()
    elif args.specific:
        test_specific_command()
    else:
        if args.quick:
            # Quick test with fewer commands
            TEST_COMMANDS[:] = TEST_COMMANDS[:5]
            NON_CODE_COMMANDS[:] = NON_CODE_COMMANDS[:5]
            print("🚀 Running quick test with 5 commands each...")
        
        asyncio.run(run_tests(args.debug)) 