# Contributing to Jarvis Voice Assistant

Thank you for your interest in contributing to Jarvis Voice Assistant! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs
- Use the GitHub issue tracker
- Include detailed steps to reproduce the bug
- Provide system information (OS, Python version, etc.)
- Include error messages and logs

### Suggesting Features
- Open a feature request issue
- Describe the feature and its benefits
- Consider implementation complexity
- Check if similar features already exist

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Git
- All system dependencies (see README.md)

### Local Development
```bash
# Clone your fork
git clone https://github.com/yourusername/jarvis-voice-assistant.git
cd jarvis-voice-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .[dev]

# Copy config template
cp config_template.py config.py
# Edit config.py with your API keys
```

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.

# Run linting
flake8 .
black --check .
mypy .
```

## 📝 Code Style

### Python Code
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Reference issues when applicable

Example:
```
Add weather forecast functionality

- Implement 3-day weather forecast
- Add temperature and humidity data
- Update README with new features

Fixes #123
```

### Pull Request Guidelines
- Provide a clear description of changes
- Include tests for new features
- Update documentation if needed
- Ensure all tests pass
- Follow the existing code style

## 🏗️ Project Structure

### Core Files
- `main.py` - Main application entry point
- `intent_classifier.py` - Intent detection and classification
- `utils.py` - Utility functions and API integrations
- `config.py` - Configuration (not in repo)

### Adding New Features

#### 1. Intent Classification
Add new intents to `intent_classifier.py`:
```python
"new_intent": [
    "phrase 1", "phrase 2", "phrase 3"
]
```

#### 2. Intent Handling
Add handling in `main.py`:
```python
elif intent == "new_intent":
    result = handle_new_intent()
    speak(result, selected_voice_model)
```

#### 3. Implementation
Add the function to `utils.py`:
```python
def handle_new_intent():
    """Handle the new intent functionality."""
    # Implementation here
    return "Success message"
```

#### 4. Testing
Create tests in a `tests/` directory:
```python
def test_handle_new_intent():
    result = handle_new_intent()
    assert "Success" in result
```

## 🔧 Development Guidelines

### Error Handling
- Use try-catch blocks for external API calls
- Provide meaningful error messages
- Log errors appropriately
- Graceful degradation when possible

### Performance
- Avoid blocking operations in the main loop
- Use async/await for I/O operations
- Cache expensive operations when possible
- Profile code for bottlenecks

### Security
- Never commit API keys or sensitive data
- Validate user input
- Use secure defaults
- Follow security best practices

### Documentation
- Update README.md for new features
- Add docstrings to new functions
- Include usage examples
- Update configuration templates

## 🧪 Testing

### Unit Tests
- Test individual functions
- Mock external dependencies
- Test edge cases and error conditions
- Maintain good test coverage

### Integration Tests
- Test complete workflows
- Test API integrations
- Test system interactions
- Test user scenarios

### Manual Testing
- Test voice recognition accuracy
- Test TTS quality
- Test face authorization
- Test all major features

## 📋 Issue Templates

### Bug Report Template
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
A clear description of what you expected to happen.

**System Information**
- OS: [e.g. Arch Linux]
- Python Version: [e.g. 3.9.7]
- Jarvis Version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.
```

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
A clear description of any alternative solutions.

**Additional context**
Add any other context or screenshots about the feature request.
```

## 🎯 Areas for Contribution

### High Priority
- Bug fixes and stability improvements
- Performance optimizations
- Better error handling
- Enhanced documentation

### Medium Priority
- New voice commands
- Additional API integrations
- UI improvements
- Testing improvements

### Low Priority
- Cosmetic changes
- Minor optimizations
- Additional voice models
- Platform-specific features

## 📞 Getting Help

- Check existing issues and discussions
- Join our community chat (if available)
- Review the documentation
- Ask questions in issues

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to Jarvis Voice Assistant! 🚀 