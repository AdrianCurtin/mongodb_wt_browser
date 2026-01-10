# Contributing to MongoDB WiredTiger Browser

Thank you for your interest in contributing to MongoDB WiredTiger Browser! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant error messages or logs

### Suggesting Enhancements

We welcome feature requests! Please open an issue with:
- A clear description of the feature
- Use cases and benefits
- Any implementation ideas you may have

### Pull Requests

1. **Fork the repository** and create a new branch for your feature or bugfix
2. **Write clear commit messages** describing your changes
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Submit a pull request** with a clear description

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/mongodb_wt_browser.git
cd mongodb_wt_browser

# Install dependencies
make install-dev
# or
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run the test suite
make test
# or
python test_demo.py
```

### Code Style

We follow Python best practices:
- Use meaningful variable and function names
- Write docstrings for classes and functions
- Keep functions focused and modular
- Follow PEP 8 style guidelines

## Project Structure

```
mongodb_wt_browser/
├── wt_browser.py       # Core WiredTiger browser class
├── cli.py              # Command-line interface
├── examples.py         # Usage examples
├── test_demo.py        # Test suite
├── setup.py            # Package setup
├── requirements.txt    # Production dependencies
├── requirements-dev.txt # Development dependencies
├── README.md           # Main documentation
├── QUICKSTART.md       # Quick start guide
├── LICENSE             # MIT License
└── Makefile            # Build commands
```

## Adding New Features

When adding a new feature:

1. **Maintain backward compatibility** when possible
2. **Add appropriate error handling**
3. **Update documentation** (README.md, QUICKSTART.md)
4. **Add examples** if the feature is user-facing
5. **Test thoroughly** with various scenarios

### Example: Adding a New Export Format

If you want to add a new export format (e.g., XML):

1. Add the export method to `WiredTigerBrowser` class in `wt_browser.py`:
   ```python
   def export_table_to_xml(self, table_name, output_path, limit=None):
       # Implementation
   ```

2. Update the CLI in `cli.py` to support the new format:
   ```python
   @click.option('--format', type=click.Choice(['json', 'csv', 'xml']))
   ```

3. Add tests to `test_demo.py`
4. Update README.md with the new format
5. Add examples to `examples.py`

## Testing Guidelines

- Test with different WiredTiger database configurations
- Include edge cases (empty tables, large tables, etc.)
- Verify error handling works correctly
- Test all CLI commands and options

## Documentation

Good documentation helps everyone:
- Update README.md for major changes
- Update QUICKSTART.md for user-facing features
- Add docstrings to new functions and classes
- Include usage examples

## Code Review Process

All pull requests will be reviewed for:
- Code quality and style
- Test coverage
- Documentation completeness
- Backward compatibility
- Performance implications

## Questions?

If you have questions about contributing:
- Open an issue on GitHub
- Check existing issues and pull requests
- Review the documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in the project. Thank you for making MongoDB WiredTiger Browser better!
