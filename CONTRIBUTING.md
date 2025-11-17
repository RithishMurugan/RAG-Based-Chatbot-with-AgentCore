# Contributing to RAG Agent Core

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a virtual environment and install dependencies
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/rag-agentcore.git
cd rag-agentcore

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

## Testing

Before submitting a pull request:

1. Test the main application:
   ```bash
   python app.py
   ```

2. Test knowledge base retrieval:
   ```bash
   python scripts/check_if_ready.py
   ```

3. Test the API endpoints

## Pull Request Process

1. Update the README.md if needed
2. Add comments to complex code
3. Ensure all tests pass
4. Submit a clear description of your changes

## Reporting Issues

When reporting issues, please include:

- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)

## Questions?

Open an issue for questions or discussions about the project.
